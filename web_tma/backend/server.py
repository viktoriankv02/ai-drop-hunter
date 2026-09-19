import os
import sys
import json
import asyncio
import subprocess
import traceback
from contextlib import asynccontextmanager

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import uvicorn
from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from core.database import init_db, async_session_maker, DropProject
from discovery.universal_scanner import load_sources, save_sources

_scanner_process = None

def start_scanner_subprocess() -> bool:
    global _scanner_process
    if _scanner_process is not None and _scanner_process.poll() is None:
        logger.warning("[Scanner] Сканування вже виконується у фоні.")
        return False

    scanner_path = os.path.join(ROOT_DIR, "discovery", "universal_scanner.py")
    _scanner_process = subprocess.Popen([sys.executable, scanner_path], cwd=ROOT_DIR)
    logger.success("[Scanner] Фоновий процес збору запущено.")
    return True

async def daily_scanner_loop():
    await asyncio.sleep(8)
    while True:
        logger.info("[Scheduler] Щоденний авто-пошук нових дропів...")
        try:
            start_scanner_subprocess()
        except Exception as e:
            logger.error(f"[Scheduler] Помилка: {e}")
        await asyncio.sleep(86400)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    scheduler_task = asyncio.create_task(daily_scanner_loop())
    yield
    scheduler_task.cancel()

app = FastAPI(title="AI Drop Hunter TMA", lifespan=lifespan)
templates_dir = os.path.join(ROOT_DIR, "web_tma", "templates")
templates = Jinja2Templates(directory=templates_dir)
templates.env.cache = None

class StatusUpdateModel(BaseModel):
    status: str

class NewResourceModel(BaseModel):
    name: str
    url: str
    type: str = "website"

@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    try:
        async with async_session_maker() as session:
            query = select(DropProject).options(selectinload(DropProject.tasks)).order_by(DropProject.score.desc())
            projects = (await session.execute(query)).scalars().all()

        sources = load_sources()
        active_sources_count = sum(1 for s in sources if s.get("enabled", True))

        stats = {
            "total": len(projects),
            "new": sum(1 for p in projects if getattr(p, "tracking_status", "new") == "new"),
            "tracking": sum(1 for p in projects if getattr(p, "tracking_status", "new") == "tracking"),
            "archived": sum(1 for p in projects if getattr(p, "tracking_status", "new") == "archived"),
            "tasks": sum(len(p.tasks) for p in projects if p.tasks),
            "active_sources": active_sources_count,
            "total_sources": len(sources)
        }

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"projects": projects, "sources": sources, "stats": stats}
        )
    except Exception as e:
        err_msg = traceback.format_exc()
        logger.error(f"Помилка рендерингу дашборду: {err_msg}")
        return HTMLResponse(
            f"<html><body style='font-family:sans-serif;padding:30px;background:#0b0e14;color:#f87171;'>"
            f"<h2 style='color:#ef4444;'>Помилка сервера: {e}</h2>"
            f"<pre style='background:#151921;color:#e2e8f0;padding:15px;border-radius:10px;'>{err_msg}</pre>"
            f"</body></html>",
            status_code=500
        )

@app.post("/api/projects/{project_id}/status")
async def update_project_status(project_id: int, body: StatusUpdateModel):
    async with async_session_maker() as session:
        await session.execute(
            update(DropProject)
            .where(DropProject.id == project_id)
            .values(tracking_status=body.status)
        )
        await session.commit()
    logger.info(f"Проєкт #{project_id} отримав статус: {body.status}")
    return {"status": "ok", "project_id": project_id, "new_status": body.status}

@app.post("/api/resources")
async def add_resource(item: NewResourceModel):
    sources = load_sources()
    new_id = max([s.get("id", 0) for s in sources], default=0) + 1
    
    clean_val = item.url.strip()
    r_type = item.type

    if r_type == "telegram" or clean_val.startswith("@") or "t.me" in clean_val:
        r_type = "telegram"
        channel = clean_val.replace("https://t.me/s/", "").replace("http://t.me/s/", "")
        channel = channel.replace("https://t.me/", "").replace("http://t.me/", "").replace("t.me/", "")
        channel = channel.lstrip("@").strip("/")
        clean_url = f"https://t.me/s/{channel}"
    elif r_type == "twitter" or "x.com" in clean_val or "twitter.com" in clean_val:
        user = clean_val.replace("https://x.com/", "").replace("https://twitter.com/", "").lstrip("@").strip("/")
        clean_url = f"https://x.com/{user}"
    else:
        clean_url = clean_val if clean_val.startswith("http") else f"https://{clean_val}"

    new_entry = {
        "id": new_id,
        "name": item.name.strip(),
        "url": clean_url,
        "type": r_type,
        "enabled": True
    }
    sources.append(new_entry)
    save_sources(sources)
    return {"status": "ok", "resource": new_entry}

# Ендпоінт для вмикання / вимикання ресурсу
@app.post("/api/resources/{resource_id}/toggle")
async def toggle_resource(resource_id: int):
    sources = load_sources()
    found = False
    new_state = False
    for s in sources:
        if s.get("id") == resource_id:
            s["enabled"] = not s.get("enabled", True)
            new_state = s["enabled"]
            found = True
            break
    if found:
        save_sources(sources)
        logger.info(f"Ресурс #{resource_id} перемкнуто: {'Увімкнено' if new_state else 'Вимкнено'}")
    return {"status": "ok", "enabled": new_state}

@app.delete("/api/resources/{resource_id}")
async def delete_resource(resource_id: int):
    sources = load_sources()
    sources = [s for s in sources if s.get("id") != resource_id]
    save_sources(sources)
    return {"status": "ok"}

@app.post("/api/scan-now")
async def trigger_scan():
    started = start_scanner_subprocess()
    return {"status": "started" if started else "already_running"}

if __name__ == "__main__":
    uvicorn.run("web_tma.backend.server:app", host="0.0.0.0", port=8000, reload=True)
