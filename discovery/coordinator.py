import asyncio, json
from datetime import datetime, timezone, timedelta
from urllib.parse import urlsplit
from core.workspace import utcnow
from core.source_policy import source_allows_url
from discovery.evidence import read_html, material, catalog, telegram_messages, SourceUnavailable
from ai_analyzer.grounded import analyze
from ai_analyzer.gateway import OLLAMA_MODEL

class Coordinator:
    def __init__(self,store):
        self.store=store
        self.stop=asyncio.Event()
        self.current_job=None
    def progress(self,index,total):
        if self.current_job:
            with self.store.db() as c:
                c.execute("UPDATE jobs SET phase=? WHERE id=?",
                          (f"Ollama: частина {index}/{total}; локальна CPU-модель",self.current_job))
    async def discover(self,sid):
        sources=[s for s in self.store.sources() if s["id"]==sid and s["enabled"]]
        if not sources: raise SourceUnavailable("Джерело вимкнено або видалено")
        s=sources[0]
        if s["adapter"]=="manual":
            raise SourceUnavailable("Для цього джерела ще потрібен окремий адаптер; автоматичний збір не реалізовано.")
        host=urlsplit(s["url"]).hostname
        try:
            html,url=await read_html(s["url"],{host})
            if s["kind"]=="telegram":
                if s["added_by"]!="user": raise SourceUnavailable("Канал не доданий користувачем")
                previous=datetime.fromisoformat(s["last_check"]) if s["last_check"] else None
                data=telegram_messages(html,datetime.now(timezone.utc),previous)
                candidates=data["messages"]
            else:
                candidates=catalog(html,url,s["adapter"])
                data={"history_complete":False,"scope":"Посилання з однієї доступної сторінки; пагінація ще не реалізована."}
            if not candidates: raise SourceUnavailable("Не знайдено карток у доступному HTML. Це не означає відсутність проєктів.")
            added=0
            for item in candidates[:200]:
                # Do not invent rating, costs or participation tasks from a catalogue title.
                _,fresh=self.store.add_project(item["title"],item["url"],s["name"],item.get("text",""))
                added+=fresh
            outcome={"found":len(candidates),"added":added,"duplicates":min(len(candidates),200)-added,
                     "limited":len(candidates)>200,**{k:v for k,v in data.items() if k!="messages"}}
            with self.store.db() as c:
                c.execute("UPDATE sources SET last_check=?,last_status='partial',last_error=NULL WHERE id=?",(utcnow(),sid))
            return outcome
        except Exception as error:
            with self.store.db() as c:
                c.execute("UPDATE sources SET last_check=?,last_status='failed',last_error=? WHERE id=?",(utcnow(),str(error)[:600],sid))
            raise
    async def research(self,pid):
        p=self.store.project(pid)
        host=urlsplit(p["source_url"]).hostname
        permitted=[s for s in self.store.sources() if source_allows_url(s,p["source_url"])]
        if not permitted: raise SourceUnavailable("Джерело не ввімкнене в дозволеному списку")
        if all(s["adapter"]=="manual" for s in permitted):
            raise SourceUnavailable("Автоматичне читання цього джерела ще не реалізовано")
        html,url=await read_html(p["source_url"],{host})
        body=material(html,url)
        sid,changed=self.store.save_snapshot(pid,url,body)
        previous=self.store.rows("SELECT body_json,created_at FROM reports WHERE project_id=? AND snapshot_id=? ORDER BY id DESC LIMIT 1",(pid,sid))
        new_feedback=self.store.rows("SELECT 1 FROM feedback WHERE project_id=? AND created_at>? LIMIT 1",(pid,previous[0]["created_at"] if previous else ""))
        if not changed and previous and json.loads(previous[0]["body_json"]).get("coverage",{}).get("complete") and not new_feedback:
            return {"snapshot_id":sid,"changed":False,"analysis":"unchanged"}
        corrections=self.store.rows("SELECT text FROM feedback WHERE project_id=? ORDER BY id DESC LIMIT 5",(pid,))
        result=await analyze(body,[r["text"] for r in reversed(corrections)],self.progress,self.store.cached_analysis,self.store.cache_analysis)
        self.store.save_report(pid,sid,result,OLLAMA_MODEL)
        return {"snapshot_id":sid,"changed":changed,"analysis":result["status"],"coverage":result["coverage"]}
    async def analyze_snapshot(self,sid):
        rows=self.store.rows("SELECT * FROM snapshots WHERE id=?",(sid,))
        if not rows: raise ValueError("Матеріал не знайдено")
        snapshot=rows[0]
        body=json.loads(snapshot["body_json"])
        corrections=self.store.rows("SELECT text FROM feedback WHERE project_id=? ORDER BY id DESC LIMIT 5",(snapshot["project_id"],))
        result=await analyze(body,[r["text"] for r in reversed(corrections)],self.progress,self.store.cached_analysis,self.store.cache_analysis)
        self.store.save_report(snapshot["project_id"],sid,result,OLLAMA_MODEL)
        return {"snapshot_id":sid,"analysis":result["status"],"coverage":result["coverage"]}
    async def run(self):
        self.store.recover_jobs()
        while not self.stop.is_set():
            job=self.store.claim_job()
            if not job:
                try: await asyncio.wait_for(self.stop.wait(),timeout=2)
                except TimeoutError: pass
                continue
            self.current_job=job["id"]
            try:
                if job["kind"]=="discover": result=await self.discover(job["target_id"])
                elif job["kind"]=="analyze": result=await self.analyze_snapshot(job["target_id"])
                else: result=await self.research(job["target_id"])
                self.store.finish_job(job["id"],result=result)
            except asyncio.CancelledError:
                # Leave the running record for recovery on next startup.
                raise
            except Exception as error:
                message=str(error)[:700]
                if job["kind"]=="research": self.store.check_failed(job["target_id"],message)
                self.store.finish_job(job["id"],error=message)
    async def schedule(self):
        while not self.stop.is_set():
            cutoff=(datetime.now(timezone.utc)-timedelta(days=1)).isoformat()
            for source in self.store.sources():
                if source["enabled"] and source["purpose"]=="discovery" and source["adapter"]!="manual" and (not source["last_check"] or source["last_check"]<cutoff):
                    self.store.enqueue("discover",source["id"])
            for project in self.store.due_projects():
                self.store.enqueue("research",project["id"])
            try: await asyncio.wait_for(self.stop.wait(),timeout=60)
            except TimeoutError: pass
