import pytest
from fastapi.testclient import TestClient
from web_tma.backend.server import create_app
from core.workspace import Workspace

@pytest.fixture
def client(tmp_path):
    store=Workspace(tmp_path/"api.sqlite")
    app=create_app(store,background=False)
    with TestClient(app) as c:
        token=c.get("/api/session").json()["token"]
        c.headers.update({"Origin":"http://testserver","X-Hunter-Session":token})
        yield c

def test_mutation_requires_session_and_origin(client):
    token=client.headers.pop("X-Hunter-Session")
    assert client.post("/api/discovery/run",json={}).status_code==403
    client.headers["X-Hunter-Session"]=token
    assert client.post("/api/discovery/run",json={},headers={"Origin":"https://evil.example"}).status_code==403
    assert client.post("/api/discovery/run",json={}).status_code==200

def test_source_controls_and_no_ghost_channels(client):
    sources=client.get("/api/sources").json()
    assert len(sources)==6 and sources[0]["name"]=="CryptoRank"
    res=client.post("/api/sources",json={"name":"My channel","url":"@mychannel","type":"telegram"})
    assert res.status_code==200
    sid=res.json()["id"]
    assert client.post(f"/api/sources/{sid}/toggle",json={}).status_code==200
    assert client.delete(f"/api/sources/{sid}").status_code==200
    assert len(client.get("/api/sources").json())==6

def test_interest_enqueues_once_and_does_not_execute(client):
    p=client.post("/api/projects/manual",json={"title":"Example","source_url":"https://cryptorank.io/ru/drophunting/example-activity1"}).json()
    pid=p["project_id"]
    for _ in range(2):
        assert client.post(f"/api/projects/{pid}/status",json={"status":"tracking"}).status_code==200
    jobs=client.get("/api/jobs").json()
    assert len(jobs)==1 and jobs[0]["state"]=="queued"
    assert client.get(f"/api/projects/{pid}").json()["tasks"]==[]
    assert not client.get("/api/session").json()["autonomous_execution"]

def test_crypto_browser_material_and_secret_panel_rejection(client):
    text="Official instructions for this campaign are described here. "*5
    assert client.post("/api/materials/import",json={"name":"Panel","source":"https://cryptorank.io/ru/public-api/dashboard","text":text}).status_code==400
    res=client.post("/api/materials/import",json={"name":"Example","source":"https://cryptorank.io/ru/drophunting/example-activity1","text":text})
    assert res.status_code==200
    assert client.get("/api/jobs").json()[0]["kind"]=="analyze"

def test_history_count_is_not_500(client):
    h=client.get("/api/research/history").json()
    assert h["target_projects"]==500 and h["fully_reviewed"]==0
    assert h["partial_cases"]==7

def test_job_retry_is_idempotent_and_keeps_target_names(client):
    pid=client.post("/api/projects/manual",json={"title":"Named project","source_url":"https://airdrops.io/named/"}).json()["project_id"]
    jid=client.post(f"/api/projects/{pid}/research",json={}).json()["job_id"]
    store=client.app.state.store
    store.finish_job(jid,error="Temporarily unavailable")
    first=client.post(f"/api/jobs/{jid}/retry",json={}).json()["job_id"]
    second=client.post(f"/api/jobs/{jid}/retry",json={}).json()["job_id"]
    assert first==second and first!=jid
    jobs=client.get("/api/jobs").json()
    assert jobs[0]["state"]=="queued"
    assert jobs[0]["target_name"]=="Named project"
    assert jobs[0]["project_id"]==pid


def test_retry_does_not_reenable_paused_source(client):
    store=client.app.state.store
    jid=store.enqueue("discover",1)
    store.finish_job(jid,error="HTTP 403")
    client.post("/api/sources/1/toggle",json={})
    assert client.post(f"/api/jobs/{jid}/retry",json={}).status_code==400
    assert not client.get("/api/sources").json()[0]["enabled"]
