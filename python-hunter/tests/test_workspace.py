import json, sqlite3
import pytest
from core.workspace import Workspace

@pytest.fixture
def store(tmp_path):
    s=Workspace(tmp_path/"workspace.sqlite");s.initialize();return s

def test_registry_is_explicit_and_priority_ordered(store):
    sources=store.sources()
    assert [s["name"] for s in sources[:2]]==["CryptoRank","Incrypted"]
    assert not [s for s in sources if s["kind"]=="telegram"]
    sid=store.add_source("My channel","@MyChannel","telegram")
    assert [s for s in store.sources() if s["id"]==sid][0]["url"]=="https://t.me/s/mychannel"
    store.source_change(sid)
    assert not [s for s in store.sources() if s["id"]==sid][0]["enabled"]
    store.source_change(sid,True)
    assert len(store.sources())==6

def test_tracking_preserves_completion_and_new_tasks_require_review(store):
    pid,_=store.add_project("Example","https://cryptorank.io/ru/drophunting/example-activity1","CryptoRank")
    body={"text":"Do a task with official instructions and evidence.","url":"https://example.com","links":[]}
    sid,changed=store.save_snapshot(pid,body["url"],body)
    report={"tasks":[{"title":"Read docs","url":"https://example.com","quote":body["text"]}]}
    store.save_report(pid,sid,report,"test")
    tid=store.detail(pid)["tasks"][0]["id"]
    store.complete_task(tid,True)
    store.set_status(pid,"tracking")
    store.save_report(pid,sid,report,"test")
    assert len(store.detail(pid)["tasks"])==1
    assert store.detail(pid)["tasks"][0]["status"]=="user_reported"
    sid2,changed=store.save_snapshot(pid,body["url"],{**body,"text":body["text"]+" Updated."})
    assert changed and sid2!=sid
    assert store.detail(pid)["report"]["stale"]
    assert store.detail(pid)["tasks"][0]["status"]=="user_reported"

def test_snapshot_idempotency_and_job_recovery(store):
    pid,_=store.add_project("Test","https://airdrops.io/test/","Airdrops.io")
    one=store.enqueue("research",pid);assert one==store.enqueue("research",pid)
    assert store.claim_job()["id"]==one
    assert store.claim_job() is None
    store.recover_jobs()
    assert store.claim_job()["id"]==one
    store.finish_job(one,error="offline")
    assert store.enqueue("research",pid)!=one
    sid,changed=store.save_snapshot(pid,"https://airdrops.io/test/",{"text":"abc"})
    assert changed
    assert store.save_snapshot(pid,"https://airdrops.io/test/",{"text":"abc"})==(sid,False)

def test_legacy_original_is_untouched_and_status_not_trusted(tmp_path):
    legacy=tmp_path/"legacy.db"
    c=sqlite3.connect(legacy)
    c.executescript("""CREATE TABLE drop_projects(id INTEGER,title TEXT,source_url TEXT,source_platform TEXT,
        tracking_status TEXT,summary TEXT,score INTEGER);
        CREATE TABLE action_tasks(id INTEGER,project_id INTEGER,title TEXT,target_url TEXT,status TEXT);
        INSERT INTO drop_projects VALUES (1,'Old','https://example.com/','legacy','tracking','old',92);
        INSERT INTO action_tasks VALUES (2,1,'Claim','https://example.com/','COMPLETED');""")
    c.commit();c.close()
    before=legacy.read_bytes()
    s=Workspace(tmp_path/"new.db");s.initialize(legacy);s.initialize(legacy)
    assert legacy.read_bytes()==before
    assert len(s.rows("SELECT * FROM projects"))==1
    t=s.rows("SELECT * FROM tasks")[0]
    assert t["status"]=="legacy_unverified"
    assert json.loads(t["legacy_json"])["status"]=="COMPLETED"
    assert s.project(1)["status"]=="tracking"

def test_failed_check_is_not_no_change(store):
    pid,_=store.add_project("Test","https://airdrops.io/test/","Airdrops.io")
    store.set_status(pid,"tracking")
    assert len(store.due_projects())==1
    store.check_failed(pid,"403")
    p=store.project(pid)
    assert p["check_status"]=="failed" and p["last_success"] is None
    assert not store.due_projects()


def test_orphaned_tasks_are_preserved_for_recovery(tmp_path):
    legacy=tmp_path/"legacy.db"
    c=sqlite3.connect(legacy)
    c.executescript("""CREATE TABLE drop_projects(id INTEGER,title TEXT,source_url TEXT,source_platform TEXT);
    CREATE TABLE action_tasks(id INTEGER,project_id INTEGER,title TEXT,target_url TEXT);
    INSERT INTO action_tasks VALUES (5,999,\'Lost task\',\'https://example.com\');""")
    c.commit();c.close()
    s=Workspace(tmp_path/"new.db");s.initialize(legacy)
    issue=s.rows("SELECT * FROM migration_issues")[0]
    assert issue["legacy_id"]==5
    assert json.loads(issue["original_json"])["title"]=="Lost task"
    assert not s.rows("SELECT * FROM tasks")

def test_adapter_upgrade_preserves_disabled_source_and_deleted_sources(store):
    with store.db() as c:
        c.execute("DELETE FROM meta WHERE key='airdropalert_adapter_v2'")
        c.execute("UPDATE sources SET url='https://airdropalert.com/',adapter='manual',enabled=0 WHERE name='AirdropAlert'")
    store.initialize()
    source=next(s for s in store.sources() if s["name"]=="AirdropAlert")
    assert source["adapter"]=="airdropalert" and not source["enabled"]
    store.source_change(source["id"],True)
    store.initialize()
    assert not any(s["name"]=="AirdropAlert" for s in store.sources())
