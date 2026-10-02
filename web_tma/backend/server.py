"""Local single-user API. Public deployment requires an authentication layer."""
import asyncio, json, os, secrets, sqlite3
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Literal
from urllib.parse import urlsplit
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from core.workspace import Workspace, ROOT, utcnow
from core.source_policy import canonical_url
from core.historical_research import load_history
from discovery.coordinator import Coordinator
from market_intelligence.forecaster import get_klines_data, generate_ai_token_forecast, MarketUnavailable

class SourceInput(BaseModel):
    name: str=Field(min_length=2,max_length=120)
    url: str=Field(min_length=5,max_length=1500)
    type: Literal["website","telegram"]="website"
class ProjectInput(BaseModel):
    title: str=Field(min_length=2,max_length=200)
    source_url: str=Field(max_length=1500)
    source_platform: str=Field(default="Власне джерело",max_length=100)
    summary: str=Field(default="",max_length=6000)
class StatusInput(BaseModel):
    status: Literal["new","tracking","ignored","archived"]
class TaskInput(BaseModel):
    done: bool
class FeedbackInput(BaseModel):
    text: str=Field(min_length=3,max_length=1500)
class BrowserMaterialInput(BaseModel):
    name: str=Field(min_length=2,max_length=200)
    source: str=Field(max_length=1500)
    text: str=Field(min_length=100,max_length=60000)

class MaterialInput(BaseModel):
    text: str=Field(min_length=100,max_length=60000)
    url: str=Field(max_length=1500)

def create_app(store=None,background=True,legacy=None):
    store=store or Workspace()
    token=secrets.token_urlsafe(32)
    coordinator=Coordinator(store)
    @asynccontextmanager
    async def lifespan(app):
        store.initialize(legacy=legacy)
        tasks=[]
        if background:
            tasks=[asyncio.create_task(coordinator.run()),asyncio.create_task(coordinator.schedule())]
        try: yield
        finally:
            coordinator.stop.set()
            for task in tasks: task.cancel()
            await asyncio.gather(*tasks,return_exceptions=True)
    app=FastAPI(title="AI Crypto Hub & Hunter",lifespan=lifespan)
    app.state.store=store
    @app.middleware("http")
    async def local_access(request:Request,call_next):
        host=request.url.hostname
        if host not in ("127.0.0.1","localhost","testserver"):
            return JSONResponse({"detail":"Локальний режим"},status_code=403)
        if request.method not in ("GET","HEAD","OPTIONS"):
            if request.headers.get("origin")!=str(request.base_url).rstrip("/"):
                return JSONResponse({"detail":"Невідоме походження запиту"},status_code=403)
            if not secrets.compare_digest(request.headers.get("x-hunter-session",""),token):
                return JSONResponse({"detail":"Оновіть сторінку: сесія змінилась"},status_code=403)
        return await call_next(request)
    @app.exception_handler(ValueError)
    async def invalid(request,error): return JSONResponse({"detail":str(error)},status_code=400)
    @app.exception_handler(sqlite3.IntegrityError)
    async def duplicate(request,error): return JSONResponse({"detail":"Такий запис уже є або порушено зв’язок даних"},status_code=409)
    @app.exception_handler(MarketUnavailable)
    async def unavailable(request,error): return JSONResponse({"detail":str(error)},status_code=503)
    @app.get("/api/session")
    def session(): return {"token":token,"mode":"local","autonomous_execution":False}
    @app.get("/api/stats")
    def stats():
        projects=store.rows("SELECT status,count(*) AS n FROM projects WHERE check_status!=\'excluded_catalog_navigation\' GROUP BY status")
        counts={p["status"]:p["n"] for p in projects}
        sources=store.sources()
        return {"tracking":counts.get("tracking",0),"new":counts.get("new",0),
                "total":sum(counts.values()),"sources":sum(s["enabled"] for s in sources),
                "migration_issues":store.rows("SELECT count(*) n FROM migration_issues")[0]["n"],
                "jobs":store.rows("SELECT state,count(*) n FROM jobs GROUP BY state")}
    @app.get("/api/migration/issues")
    def migration_issues(): return store.rows("SELECT id,entity,legacy_id,reason FROM migration_issues ORDER BY id")
    @app.get("/api/sources")
    def sources(): return [{**s,"type":s["kind"]} for s in store.sources()]
    @app.post("/api/sources")
    def add_source(body:SourceInput): return {"id":store.add_source(body.name,body.url,body.type)}
    @app.delete("/api/sources/{sid}")
    def delete_source(sid:int): store.source_change(sid,True); return {"ok":True}
    @app.post("/api/sources/{sid}/toggle")
    def toggle_source(sid:int): store.source_change(sid); return {"ok":True}
    @app.post("/api/sources/{sid}/scan")
    def scan_source(sid:int):
        if not any(s["id"]==sid and s["enabled"] for s in store.sources()): raise ValueError("Джерело вимкнено або відсутнє")
        return {"job_id":store.enqueue("discover",sid)}
    @app.post("/api/discovery/run")
    def discovery():
        return {"job_ids":[store.enqueue("discover",s["id"]) for s in store.sources()
                           if s["enabled"] and s["purpose"]=="discovery" and s["adapter"]!="manual"]}
    @app.get("/api/activity-screening")
    def activity_counts():
        restricted=bool(store.rows("SELECT 1 FROM meta WHERE key='active_source_scope'"))
        result={"test_only":0,"needs_review":0,"excluded":0}
        for row in store.rows("""SELECT COALESCE(a.decision,'needs_review') AS decision,COUNT(*) AS n
            FROM projects p LEFT JOIN activity_screening a ON a.project_id=p.id WHERE p.status='new' AND (?=0 OR p.source_url LIKE 'https://cryptorank.io/%' OR p.source_url LIKE 'https://incrypted.com/%') GROUP BY 1""",(int(restricted),)):
            result[row["decision"]]=row["n"]
        return result
    @app.get("/api/projects")
    def projects(status:str="new",q:str="",limit:int=60,offset:int=0,screen:str="all"):
        if status not in ("new","tracking","ignored","archived","all"): raise ValueError("Невідомий статус")
        restricted=bool(store.rows("SELECT 1 FROM meta WHERE key='active_source_scope'"))
        if screen not in ("all","test_only","needs_review","excluded"): raise ValueError("Невідомий фільтр активності")
        limit=max(1,min(100,limit));offset=max(0,offset)
        rows=store.rows("""SELECT id,title,source_url,source_platform,status,summary,last_checked,last_success,check_status,
                           (legacy_json IS NOT NULL) AS legacy,
                           (SELECT decision FROM activity_screening a WHERE a.project_id=projects.id) AS activity_decision,
                           (SELECT reason FROM activity_screening a WHERE a.project_id=projects.id) AS activity_reason FROM projects
                           WHERE (?='all' OR status=?) AND (title LIKE ? OR source_platform LIKE ?)
                           AND (?=0 OR projects.status!='new' OR source_url LIKE 'https://cryptorank.io/%' OR source_url LIKE 'https://incrypted.com/%' OR source_platform='Власне джерело')
                           AND (?='all' OR COALESCE((SELECT decision FROM activity_screening a WHERE a.project_id=projects.id),'needs_review')=?)
                           ORDER BY EXISTS(SELECT 1 FROM reports r WHERE r.project_id=projects.id) DESC,
                           CASE WHEN source_platform LIKE '%CryptoRank%' THEN 0
                                         WHEN source_platform LIKE '%Incrypted%' THEN 1 ELSE 2 END,id DESC LIMIT ? OFFSET ?""",
                        (status,status,"%"+q[:120]+"%","%"+q[:120]+"%",int(restricted),screen,screen,limit,offset))
        profiles={x["project_id"]:json.loads(x["body_json"]) for x in store.rows("SELECT project_id,body_json FROM project_overviews")}
        for row in rows:
            row["overview"]=profiles.get(row["id"])
            row["preparation"]=store.preparation(row['id'])
        return rows
    @app.get("/api/projects/{pid}")
    def project(pid:int): return store.detail(pid)
    @app.post("/api/projects/manual")
    def manual(body:ProjectInput):
        pid,added=store.add_project(body.title,body.source_url,body.source_platform,body.summary)
        return {"project_id":pid,"added":added}
    @app.post("/api/projects/{pid}/status")
    def status(pid:int,body:StatusInput):
        store.set_status(pid,body.status)
        job=store.enqueue("research",pid) if body.status=="tracking" else None
        return {"ok":True,"job_id":job}
    @app.post("/api/projects/{pid}/research")
    def research(pid:int):
        store.project(pid)
        return {"job_id":store.enqueue("research",pid)}
    @app.post("/api/projects/{pid}/material")
    def import_material(pid:int,body:MaterialInput):
        p=store.project(pid)
        url=canonical_url(body.url)
        if url!=canonical_url(p["source_url"]):
            raise ValueError("Для цього імпорту вкажіть URL картки проєкту. Додаткові джерела підключатимуться окремо.")
        import re
        links=[]
        for candidate in re.findall(r"https://[^\s<>\"']+",body.text):
            try: links.append({"url":canonical_url(candidate),"label":""})
            except ValueError: pass
        sid,changed=store.save_snapshot(pid,url,{"text":body.text,"links":links[:150],"url":url,
                       "truncated":False,"characters_available":len(body.text)},via="user_paste")
        return {"snapshot_id":sid,"changed":changed,"job_id":store.enqueue("analyze",sid)}
    @app.post("/api/materials/import")
    def browser_material(body:BrowserMaterialInput):
        import re
        source=canonical_url(body.source)
        parsed=urlsplit(source)
        if parsed.hostname!="cryptorank.io" or not re.fullmatch(r"/(?:ru/)?drophunting/[a-z0-9-]+-activity[0-9]*/?",parsed.path):
            raise ValueError("Потрібна картка CryptoRank Drophunting, не API-панель")
        if not any(s["enabled"] and s["adapter"]=="cryptorank" for s in store.sources()):
            raise ValueError("CryptoRank вимкнений у списку джерел")
        if any(x in body.text.lower() for x in ("verify you are human","just a moment","cf-chl-","трохи зачекайте")):
            raise ValueError("Це сторінка перевірки браузера, а не матеріал")
        pid,_=store.add_project(body.name,source,"CryptoRank")
        return import_material(pid,MaterialInput(text=body.text,url=source))

    @app.post("/api/tasks/{tid}/completion")
    def complete(tid:int,body:TaskInput): store.complete_task(tid,body.done); return {"ok":True}
    @app.post("/api/projects/{pid}/feedback")
    def feedback(pid:int,body:FeedbackInput):
        store.project(pid)
        with store.db() as c:
            c.execute("INSERT INTO feedback(project_id,text,created_at) VALUES (?,?,?)",(pid,body.text,utcnow()))
        return {"ok":True,"learning":"Корекцію буде включено в наступний аналіз; ваги моделі не змінюються."}
    @app.get("/api/jobs")
    def jobs():
        return store.rows("""SELECT j.*,CASE WHEN j.kind='discover' THEN s.name
                       ELSE p.title END AS target_name,
                       CASE WHEN j.kind='discover' THEN NULL ELSE p.id END AS project_id
                       FROM jobs j
                       LEFT JOIN sources s ON j.kind='discover' AND j.target_id=s.id
                       LEFT JOIN snapshots sn ON j.kind='analyze' AND j.target_id=sn.id
                       LEFT JOIN projects p ON (j.kind='research' AND j.target_id=p.id)
                                            OR (j.kind='analyze' AND sn.project_id=p.id)
                       ORDER BY CASE j.state WHEN 'running' THEN 0 WHEN 'queued' THEN 1 ELSE 2 END,
                                CASE WHEN j.state='queued' THEN CASE j.kind WHEN 'discover' THEN 0 WHEN 'analyze' THEN 1 ELSE 2 END ELSE 0 END,
                                CASE WHEN j.state='queued' THEN j.id ELSE -j.id END LIMIT 100""")
    @app.post("/api/jobs/{jid}/retry")
    def retry_job(jid:int):
        rows=store.rows("SELECT * FROM jobs WHERE id=?",(jid,))
        if not rows: raise ValueError("Роботу не знайдено")
        job=rows[0]
        if job["state"] not in ("failed","succeeded"):
            return {"job_id":job["id"]}
        if job["kind"]=="discover":
            if not any(s["id"]==job["target_id"] and s["enabled"] for s in store.sources()):
                raise ValueError("Спочатку ввімкни джерело")
        elif job["kind"]=="research":
            store.project(job["target_id"])
        elif not store.rows("SELECT id FROM snapshots WHERE id=?",(job["target_id"],)):
            raise ValueError("Збережений матеріал відсутній")
        return {"job_id":store.enqueue(job["kind"],job["target_id"])}

    @app.get("/api/research/history")
    def history():
        return load_history()
    @app.get("/api/market/chart")
    async def chart(symbol:str="BTC",period:str="24h"): return await get_klines_data(symbol,period)
    @app.post("/api/market/forecast")
    async def forecast(symbol:str="BTC",horizon:str="24h"):
        result=await generate_ai_token_forecast(symbol,horizon)
        with store.db() as c:
            fid=c.execute("INSERT INTO forecasts(symbol,horizon,issued_at,target_at,body_json) VALUES (?,?,?,?,?)",
                          (result["symbol"],horizon,result["issued_at"],result["target_at"],json.dumps(result,ensure_ascii=False))).lastrowid
        return {**result,"id":fid}
    @app.get("/api/market/forecasts")
    def forecasts():
        return [{"id":r["id"],**json.loads(r["body_json"]),"outcome":json.loads(r["outcome_json"]) if r["outcome_json"] else None}
                for r in store.rows("SELECT * FROM forecasts ORDER BY id DESC LIMIT 30")]
    app.mount("/static",StaticFiles(directory=ROOT/"web_tma"/"frontend"),name="static")
    @app.get("/")
    def index(): return FileResponse(ROOT/"web_tma"/"frontend"/"index.html")
    return app

app=create_app(legacy=ROOT/"drop_hunter.db",background=os.getenv("HUNTER_BACKGROUND","1")=="1")
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=4318)
