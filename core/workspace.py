"""Versioned local workspace; never opens the shipped legacy DB for writes."""
import os, json, sqlite3, hashlib
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from core.source_policy import DEFAULT_SOURCES, ADAPTERS, canonical_url, telegram_url
from core.revisions import compare_materials
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = Path(os.environ.get("HUNTER_DB", str(ROOT / "data" / "workspace.sqlite")))
def utcnow():
    return datetime.now(timezone.utc).isoformat()
def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

class Workspace:
    def __init__(self, path=DEFAULT_DB):
        self.path = Path(path)
    @contextmanager
    def db(self):
        conn = sqlite3.connect(self.path, timeout=20)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        finally:
            conn.close()
    def initialize(self, legacy=None):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.db() as c:
            c.executescript("""
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS sources(
                id INTEGER PRIMARY KEY, name TEXT NOT NULL, url TEXT UNIQUE NOT NULL,
                kind TEXT NOT NULL, purpose TEXT NOT NULL, priority INTEGER NOT NULL,
                adapter TEXT NOT NULL, enabled INTEGER NOT NULL, added_by TEXT NOT NULL,
                last_check TEXT, last_status TEXT, last_error TEXT, created_at TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS projects(
                id INTEGER PRIMARY KEY, title TEXT NOT NULL, source_url TEXT UNIQUE NOT NULL,
                source_platform TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'new',
                summary TEXT NOT NULL DEFAULT '', legacy_json TEXT, created_at TEXT NOT NULL,
                last_checked TEXT, last_success TEXT, check_status TEXT NOT NULL DEFAULT 'unreviewed');
            CREATE TABLE IF NOT EXISTS snapshots(
                id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL REFERENCES projects(id),
                url TEXT NOT NULL, content_hash TEXT NOT NULL, body_json TEXT NOT NULL,
                fetched_at TEXT NOT NULL, via TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS analysis_parts(cache_key TEXT PRIMARY KEY,body_json TEXT NOT NULL,created_at TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS reports(
                id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL REFERENCES projects(id),
                snapshot_id INTEGER NOT NULL REFERENCES snapshots(id),
                body_json TEXT NOT NULL, model TEXT NOT NULL, created_at TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL REFERENCES projects(id),
                fingerprint TEXT NOT NULL, title TEXT NOT NULL, target_url TEXT,
                status TEXT NOT NULL DEFAULT 'needs_review', evidence_json TEXT,
                legacy_json TEXT, created_at TEXT NOT NULL, UNIQUE(project_id,fingerprint));
            CREATE TABLE IF NOT EXISTS events(
                id INTEGER PRIMARY KEY, project_id INTEGER REFERENCES projects(id),
                kind TEXT NOT NULL, details TEXT NOT NULL, created_at TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS jobs(
                id INTEGER PRIMARY KEY, kind TEXT NOT NULL, target_id INTEGER NOT NULL,
                state TEXT NOT NULL DEFAULT 'queued', phase TEXT NOT NULL DEFAULT 'waiting',
                result_json TEXT, error TEXT, created_at TEXT NOT NULL, finished_at TEXT);
            CREATE UNIQUE INDEX IF NOT EXISTS jobs_active ON jobs(kind,target_id)
                WHERE state IN ('queued','running');
            CREATE TABLE IF NOT EXISTS migration_issues(
                id INTEGER PRIMARY KEY, entity TEXT NOT NULL, legacy_id INTEGER NOT NULL,
                reason TEXT NOT NULL, original_json TEXT NOT NULL, UNIQUE(entity,legacy_id));
            CREATE TABLE IF NOT EXISTS feedback(
                id INTEGER PRIMARY KEY, project_id INTEGER REFERENCES projects(id),
                text TEXT NOT NULL, created_at TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS forecasts(
                id INTEGER PRIMARY KEY, symbol TEXT NOT NULL, horizon TEXT NOT NULL,
                issued_at TEXT NOT NULL, target_at TEXT NOT NULL, body_json TEXT NOT NULL,
                outcome_json TEXT);
            """)
            if not c.execute("SELECT 1 FROM meta WHERE key='source_policy_v1'").fetchone():
                for name,url,priority,purpose,adapter in DEFAULT_SOURCES:
                    c.execute("""INSERT OR IGNORE INTO sources
                    (name,url,kind,purpose,priority,adapter,enabled,added_by,created_at)
                    VALUES (?,?,'website',?,?,?,1,'user_requirements',?)""",
                    (name,url,purpose,priority,adapter,utcnow()))
                c.execute("INSERT INTO meta VALUES ('source_policy_v1','1')")
            if not c.execute("SELECT 1 FROM meta WHERE key='airdropalert_adapter_v2'").fetchone():
                c.execute("""UPDATE sources SET url='https://airdropalert.com/farm/',adapter='airdropalert',
                             last_check=NULL,last_status=NULL,last_error=NULL
                             WHERE url='https://airdropalert.com/' AND adapter='manual'
                             AND added_by='user_requirements' AND NOT EXISTS
                             (SELECT 1 FROM sources WHERE url='https://airdropalert.com/farm/')""")
                c.execute("INSERT INTO meta VALUES ('airdropalert_adapter_v2','1')")
            if not c.execute("SELECT 1 FROM meta WHERE key='legacy_import_v1'").fetchone():
                if legacy and Path(legacy).is_file():
                    old = sqlite3.connect(Path(legacy).resolve().as_uri()+"?mode=ro", uri=True)
                    old.row_factory = sqlite3.Row
                    try:
                        for row in old.execute("SELECT * FROM drop_projects"):
                            p = dict(row)
                            status = p.get("tracking_status", "new")
                            if status not in ("new","tracking","ignored","archived"): status = "new"
                            c.execute("""INSERT OR IGNORE INTO projects
                            (id,title,source_url,source_platform,status,summary,legacy_json,created_at)
                            VALUES (?,?,?,?,?,?,?,?)""", (p["id"],p["title"],p["source_url"],
                            p.get("source_platform") or "legacy", status, p.get("summary") or "",
                            json.dumps(p,ensure_ascii=False),utcnow()))
                        for row in old.execute("SELECT * FROM action_tasks"):
                            t = dict(row)
                            if not c.execute("SELECT 1 FROM projects WHERE id=?",(t["project_id"],)).fetchone():
                                c.execute("INSERT OR IGNORE INTO migration_issues(entity,legacy_id,reason,original_json) VALUES (?,?,?,?)",
                                          ("action_task",t["id"],"missing_project",json.dumps(t,ensure_ascii=False)))
                                continue
                            c.execute("""INSERT OR IGNORE INTO tasks
                            (project_id,fingerprint,title,target_url,status,legacy_json,created_at)
                            VALUES (?,?,?,?,'legacy_unverified',?,?)""",
                            (t["project_id"],"legacy:"+str(t["id"]),t["title"],t.get("target_url"),
                             json.dumps(t,ensure_ascii=False),utcnow()))
                    finally: old.close()
                c.execute("INSERT INTO meta VALUES ('legacy_import_v1','1')")
    def rows(self, sql, args=()):
        with self.db() as c: return [dict(r) for r in c.execute(sql,args)]
    def sources(self):
        return self.rows("SELECT * FROM sources ORDER BY priority DESC,id")
    def add_source(self, name, url, kind):
        url = telegram_url(url) if kind == "telegram" else canonical_url(url)
        host = urlsplit(url).hostname
        if host == "t.me" and kind != "telegram":
            raise ValueError("Telegram-канал потрібно додати як Telegram.")
        adapter = ADAPTERS.get(host,"manual")
        with self.db() as c:
            cur = c.execute("""INSERT INTO sources
            (name,url,kind,purpose,priority,adapter,enabled,added_by,created_at)
            VALUES (?,?,?,'discovery',?,?,1,'user',?)""",
            (name,url,kind,10 if kind=="telegram" else 40,adapter,utcnow()))
            return cur.lastrowid
    def source_change(self, sid, delete=False):
        with self.db() as c:
            cur = c.execute("DELETE FROM sources WHERE id=?" if delete else
                            "UPDATE sources SET enabled=1-enabled WHERE id=?", (sid,))
            if not cur.rowcount: raise ValueError("Джерело не знайдено")
    def add_project(self, title, url, source, summary=""):
        url = canonical_url(url)
        with self.db() as c:
            cur = c.execute("""INSERT OR IGNORE INTO projects
                (title,source_url,source_platform,summary,created_at) VALUES (?,?,?,?,?)""",
                (title[:200],url,source,summary[:6000],utcnow()))
            return (cur.lastrowid if cur.rowcount else
                    c.execute("SELECT id FROM projects WHERE source_url=?",(url,)).fetchone()[0]), bool(cur.rowcount)
    def project(self, pid):
        rows = self.rows("SELECT * FROM projects WHERE id=?", (pid,))
        if not rows: raise ValueError("Проєкт не знайдено")
        return rows[0]
    def set_status(self, pid, status):
        if status not in ("new","tracking","ignored","archived"): raise ValueError("Невідомий статус")
        self.project(pid)
        with self.db() as c:
            c.execute("UPDATE projects SET status=? WHERE id=?",(status,pid))
            self._event(c,pid,"status",status)
        # Deliberately does not touch task completion or execution permissions.
    def _event(self,c,pid,kind,details):
        c.execute("INSERT INTO events(project_id,kind,details,created_at) VALUES (?,?,?,?)",
                  (pid,kind,details,utcnow()))
    def enqueue(self, kind, target):
        if kind not in ("discover","research","analyze"): raise ValueError("Невідомий тип роботи")
        with self.db() as c:
            c.execute("INSERT OR IGNORE INTO jobs(kind,target_id,created_at) VALUES (?,?,?)",
                      (kind,target,utcnow()))
            return c.execute("SELECT id FROM jobs WHERE kind=? AND target_id=? AND state IN ('queued','running')",
                             (kind,target)).fetchone()[0]
    def due_projects(self):
        cutoff=(datetime.now(timezone.utc)-timedelta(days=1)).isoformat()
        return self.rows("""SELECT * FROM projects WHERE status='tracking'
            AND (last_checked IS NULL OR last_checked<?) ORDER BY last_checked,id""",(cutoff,))
    def claim_job(self):
        with self.db() as c:
            c.execute("BEGIN IMMEDIATE")
            row=c.execute("SELECT * FROM jobs WHERE state='queued' ORDER BY CASE kind WHEN 'discover' THEN 0 WHEN 'analyze' THEN 1 ELSE 2 END,id LIMIT 1").fetchone()
            if not row: return None
            c.execute("UPDATE jobs SET state='running',phase='reading' WHERE id=?",(row["id"],))
            return dict(row)
    def finish_job(self,jid,result=None,error=None):
        with self.db() as c:
            c.execute("""UPDATE jobs SET state=?,phase='finished',result_json=?,error=?,finished_at=?
                         WHERE id=?""",("failed" if error else "succeeded",json.dumps(result,ensure_ascii=False),
                                         error,utcnow(),jid))
    def recover_jobs(self):
        with self.db() as c:
            c.execute("UPDATE jobs SET state='queued',phase='resumed' WHERE state='running'")
    def cached_analysis(self,key):
        rows=self.rows("SELECT body_json FROM analysis_parts WHERE cache_key=?",(key,))
        return json.loads(rows[0]["body_json"]) if rows else None
    def cache_analysis(self,key,value):
        with self.db() as c:
            c.execute("INSERT OR REPLACE INTO analysis_parts VALUES (?,?,?)",(key,json.dumps(value,ensure_ascii=False),utcnow()))
    def check_failed(self,pid,error):
        with self.db() as c:
            c.execute("UPDATE projects SET last_checked=?,check_status='failed' WHERE id=?",(utcnow(),pid))
            self._event(c,pid,"check_failed",error)
    def save_snapshot(self,pid,url,body,via="web"):
        self.project(pid)
        encoded=json.dumps(body,sort_keys=True,ensure_ascii=False)
        sha=digest(encoded)
        with self.db() as c:
            prev=c.execute("SELECT * FROM snapshots WHERE project_id=? AND url=? ORDER BY id DESC LIMIT 1",
                           (pid,url)).fetchone()
            changed=not prev or prev["content_hash"]!=sha
            if changed:
                sid=c.execute("""INSERT INTO snapshots(project_id,url,content_hash,body_json,fetched_at,via)
                    VALUES (?,?,?,?,?,?)""",(pid,url,sha,encoded,utcnow(),via)).lastrowid
                self._event(c,pid,"source_changed" if prev else "source_loaded",
                            json.dumps({"snapshot_id":sid,"previous_id":prev["id"] if prev else None},ensure_ascii=False))
            else: sid=prev["id"]
            c.execute("UPDATE projects SET last_checked=?,last_success=?,check_status=? WHERE id=?",
                      (utcnow(),utcnow(),"changed" if changed else "unchanged",pid))
            return sid,changed
    def save_report(self,pid,sid,body,model):
        with self.db() as c:
            if not c.execute("SELECT 1 FROM snapshots WHERE id=? AND project_id=?",(sid,pid)).fetchone():
                raise ValueError("Матеріал належить іншому проєкту")
            rid=c.execute("INSERT INTO reports(project_id,snapshot_id,body_json,model,created_at) VALUES (?,?,?,?,?)",
                          (pid,sid,json.dumps(body,ensure_ascii=False),model,utcnow())).lastrowid
            for task in body.get("tasks",[]):
                fingerprint=digest(task["title"].strip().lower()+"|"+(task.get("url") or ""))
                existing=c.execute("SELECT id,evidence_json FROM tasks WHERE project_id=? AND fingerprint=?",(pid,fingerprint)).fetchone()
                evidence=json.dumps({"report_id":rid,"snapshot_id":sid,"quote":task["quote"],"source_url":task.get("source_url")},ensure_ascii=False)
                if existing:
                    old=json.loads(existing["evidence_json"] or "{}")
                    if old.get("quote")!=task["quote"]:
                        self._event(c,pid,"task_evidence_changed",json.dumps({"task_id":existing["id"],"previous":old,"new":json.loads(evidence)},ensure_ascii=False))
                    c.execute("UPDATE tasks SET evidence_json=? WHERE id=?",(evidence,existing["id"]))
                    continue
                c.execute("""INSERT OR IGNORE INTO tasks(project_id,fingerprint,title,target_url,evidence_json,created_at)
                    VALUES (?,?,?,?,?,?)""",(pid,fingerprint,task["title"],task.get("url"),
                    json.dumps({"report_id":rid,"snapshot_id":sid,"quote":task["quote"],"source_url":task.get("source_url")},ensure_ascii=False),utcnow()))
            self._event(c,pid,"analysis_ready",str(rid))
            return rid
    def complete_task(self,tid,done):
        with self.db() as c:
            task=c.execute("SELECT * FROM tasks WHERE id=?",(tid,)).fetchone()
            if not task: raise ValueError("Завдання не знайдено")
            state="user_reported" if done else "needs_review"
            c.execute("UPDATE tasks SET status=? WHERE id=?",(state,tid))
            self._event(c,task["project_id"],"task_user_report",json.dumps({"id":tid,"status":state}))
    def detail(self,pid):
        p=self.project(pid)
        p["legacy_warning"]=bool(p.pop("legacy_json",None))
        p["tasks"]=self.rows("SELECT id,title,target_url,status,evidence_json FROM tasks WHERE project_id=? ORDER BY id",(pid,))
        p["events"]=self.rows("SELECT * FROM events WHERE project_id=? ORDER BY id DESC LIMIT 30",(pid,))
        p["snapshots"]=self.rows("SELECT id,url,fetched_at,via,content_hash FROM snapshots WHERE project_id=? ORDER BY id DESC LIMIT 20",(pid,))
        reports=self.rows("SELECT * FROM reports WHERE project_id=? ORDER BY id DESC LIMIT 1",(pid,))
        notes=self.rows("SELECT body_json FROM snapshots WHERE project_id=? AND via='reviewed_research_note' ORDER BY id DESC LIMIT 1",(pid,))
        p["reviewed_note"]=json.loads(notes[0]["body_json"]).get("research_note") if notes else None
        p["report"]=None
        if reports:
            p["report"]={**reports[0],"body":json.loads(reports[0]["body_json"])}
            p["report"].pop("body_json")
            p["report"]["stale"]=bool(p["snapshots"] and reports[0]["snapshot_id"]!=p["snapshots"][0]["id"])
        latest_by_url = {}
        for snapshot in p["snapshots"]:
            latest_by_url.setdefault(snapshot["url"], snapshot["id"])
        for task in p["tasks"]:
            evidence = json.loads(task["evidence_json"] or "{}")
            cited = self.rows("SELECT id,url FROM snapshots WHERE id=? AND project_id=?",
                              (evidence.get("snapshot_id"), pid))
            task["evidence_state"] = ("current" if latest_by_url.get(cited[0]["url"]) == cited[0]["id"]
                                      else "source_changed") if cited else "unverified"
        p["source_changes"] = None
        if p["snapshots"]:
            latest = p["snapshots"][0]
            pair = self.rows("SELECT id,body_json,fetched_at FROM snapshots WHERE project_id=? AND url=? ORDER BY id DESC LIMIT 2",
                             (pid, latest["url"]))
            if len(pair) == 2:
                p["source_changes"] = {
                    **compare_materials(json.loads(pair[1]["body_json"]), json.loads(pair[0]["body_json"])),
                    "previous_id": pair[1]["id"], "current_id": pair[0]["id"],
                    "previous_at": pair[1]["fetched_at"], "current_at": pair[0]["fetched_at"]}
        return p
