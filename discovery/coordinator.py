import asyncio, json, os
from datetime import datetime, timezone, timedelta
from urllib.parse import urlsplit
from core.workspace import utcnow
from discovery.cryptorank_api import fetch_map
from core.source_policy import source_allows_url, canonical_url
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
            if s["adapter"]=="cryptorank" and os.getenv("CRYPTORANK_API_KEY"):
                candidates=await fetch_map()
                data={"history_complete":False,"route":"official_api_map","tasks_included":False,
                      "scope":"Повний отриманий API-каталог назв; статуси, завдання і mainnet ще не перевірені."}
            else:
                html,url=await read_html(s["url"],{host})
            if s["adapter"]=="cryptorank" and os.getenv("CRYPTORANK_API_KEY"):
                pass
            elif s["kind"]=="telegram":
                if s["added_by"]!="user": raise SourceUnavailable("Канал не доданий користувачем")
                previous=datetime.fromisoformat(s["last_check"]) if s["last_check"] else None
                data=telegram_messages(html,datetime.now(timezone.utc),previous)
                candidates=data["messages"]
            else:
                candidates=catalog(html,url,s["adapter"])
                data={"history_complete":False,"scope":"Посилання з однієї доступної сторінки; пагінація ще не реалізована."}
            if not candidates: raise SourceUnavailable("Не знайдено карток у доступному HTML. Це не означає відсутність проєктів.")
            added=0
            limit=len(candidates) if data.get("route")=="official_api_map" else 200
            for item in candidates[:limit]:
                # Do not invent rating, costs or participation tasks from a catalogue title.
                _,fresh=self.store.add_project(item["title"],item["url"],s["name"],item.get("text",""))
                added+=fresh
                if fresh and data.get("route")=="official_api_map":
                    with self.store.db() as c:
                        c.execute("UPDATE projects SET check_status='catalog_only' WHERE id=?",(_,))
            outcome={"found":len(candidates),"added":added,"duplicates":min(len(candidates),limit)-added,
                     "limited":len(candidates)>limit,**{k:v for k,v in data.items() if k!="messages"}}
            with self.store.db() as c:
                c.execute("UPDATE sources SET last_check=?,last_status='partial',last_error=NULL WHERE id=?",(utcnow(),sid))
            return outcome
        except Exception as error:
            with self.store.db() as c:
                c.execute("UPDATE sources SET last_check=?,last_status='failed',last_error=? WHERE id=?",(utcnow(),str(error)[:600],sid))
            raise
    async def read_project(self,p):
        """Fallback only to reviewed official URLs, never arbitrary links suggested by a model."""
        try:
            html,url=await read_html(p["source_url"],{urlsplit(p["source_url"]).hostname})
            return material(html,url),"web"
        except SourceUnavailable as primary_error:
            notes=self.store.rows("SELECT body_json FROM snapshots WHERE project_id=? AND via='reviewed_research_note' ORDER BY id DESC LIMIT 1",(p["id"],))
            if not notes: raise
            note=json.loads(notes[0]["body_json"]).get("research_note",{})
            sources=[x for x in note.get("sources",[]) if x.get("access")=="official_document"][:3]
            documents=[];errors=[]
            for source in sources:
                try:
                    url=canonical_url(source["url"])
                    html,resolved=await read_html(url,{urlsplit(url).hostname})
                    doc=material(html,resolved)
                    doc["purpose"]=source.get("purpose","unclassified")
                    documents.append(doc)
                except Exception as error:
                    errors.append(str(error)[:200])
            if not documents:
                raise SourceUnavailable(str(primary_error)+" Офіційні документи також недоступні.")
            text="\n\n".join("Джерело: "+d["url"]+"\n"+d["text"] for d in documents)
            links=[{"url":d["url"],"label":"Офіційна документація"} for d in documents]
            links.extend(link for d in documents for link in d["links"])
            return {"url":p["source_url"],"text":text,"links":links[:150],
                    "truncated":True,"characters_available":len(text),
                    "documents":documents,"source_errors":errors,
                    "provenance":"Агрегатор недоступний. Прочитано раніше перевірені офіційні документи; загальне досьє неповне."},"official_documents_fallback"

    @staticmethod
    def attach_provenance(result,body):
        if body.get("provenance"):
            result["provenance"]=body["provenance"]
            result.setdefault("unknowns",[]).extend(body.get("source_errors",[]))
            for item in result.get("facts",[])+result.get("tasks",[]):
                matches=[d["url"] for d in body.get("documents",[]) if item.get("quote") and item["quote"] in d["text"]]
                if len(matches)==1: item["source_url"]=matches[0]
            reward_sources={d["url"] for d in body.get("documents",[]) if d.get("purpose")=="reward_rules"}
            tasks=result.get("tasks",[])
            result["reference_actions"]=[t for t in tasks if t.get("source_url") not in reward_sources]
            result["tasks"]=[t for t in tasks if t.get("source_url") in reward_sources]
            if result["reference_actions"]:
                result.setdefault("unknowns",[]).append("Інструкції платформи не підтверджують завдання кампанії; їх винесено в довідку.")

    async def research(self,pid):
        p=self.store.project(pid)
        host=urlsplit(p["source_url"]).hostname
        permitted=[s for s in self.store.sources() if source_allows_url(s,p["source_url"])]
        if not permitted: raise SourceUnavailable("Джерело не ввімкнене в дозволеному списку")
        if all(s["adapter"]=="manual" for s in permitted):
            raise SourceUnavailable("Автоматичне читання цього джерела ще не реалізовано")
        body,via=await self.read_project(p)
        url=p["source_url"]
        sid,changed=self.store.save_snapshot(pid,url,body,via=via)
        previous=self.store.rows("SELECT body_json,created_at FROM reports WHERE project_id=? AND snapshot_id=? ORDER BY id DESC LIMIT 1",(pid,sid))
        new_feedback=self.store.rows("SELECT 1 FROM feedback WHERE project_id=? AND created_at>? LIMIT 1",(pid,previous[0]["created_at"] if previous else ""))
        if not changed and previous and json.loads(previous[0]["body_json"]).get("coverage",{}).get("complete") and not new_feedback:
            return {"snapshot_id":sid,"changed":False,"analysis":"unchanged"}
        corrections=self.store.rows("SELECT text FROM feedback WHERE project_id=? ORDER BY id DESC LIMIT 5",(pid,))
        result=await analyze(body,[r["text"] for r in reversed(corrections)],self.progress,self.store.cached_analysis,self.store.cache_analysis)
        self.attach_provenance(result,body)
        self.store.save_report(pid,sid,result,OLLAMA_MODEL)
        return {"snapshot_id":sid,"changed":changed,"analysis":result["status"],"coverage":result["coverage"]}
    async def analyze_snapshot(self,sid):
        rows=self.store.rows("SELECT * FROM snapshots WHERE id=?",(sid,))
        if not rows: raise ValueError("Матеріал не знайдено")
        snapshot=rows[0]
        project=self.store.project(snapshot["project_id"])
        if not any(source_allows_url(source,project["source_url"]) for source in self.store.sources()):
            raise SourceUnavailable("Джерело вимкнене: аналіз призупинено.")
        body=json.loads(snapshot["body_json"])
        corrections=self.store.rows("SELECT text FROM feedback WHERE project_id=? ORDER BY id DESC LIMIT 5",(snapshot["project_id"],))
        result=await analyze(body,[r["text"] for r in reversed(corrections)],self.progress,self.store.cached_analysis,self.store.cache_analysis)
        self.attach_provenance(result,body)
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
            enabled_sources=self.store.sources()
            for project in self.store.due_projects():
                if any(source_allows_url(source,project["source_url"]) for source in enabled_sources):
                    self.store.enqueue("research",project["id"])
            try: await asyncio.wait_for(self.stop.wait(),timeout=60)
            except TimeoutError: pass
