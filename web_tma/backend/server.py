import os
import sys
import json
import sqlite3
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from market_intelligence.scanner import run_market_scanner
from market_intelligence.forecaster import get_klines_data, generate_ai_token_forecast

DB_PATH = os.path.join(ROOT_DIR, "drop_hunter.db")
SOURCES_PATH = os.path.join(ROOT_DIR, "sources", "resources.json")

app = FastAPI(title="AI Crypto Hub & Hunter")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def read_sources():
    if not os.path.exists(SOURCES_PATH): return []
    try:
        with open(SOURCES_PATH, "r", encoding="utf-8-sig") as f: return json.load(f)
    except Exception: return []

@app.get("/api/stats")
async def get_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM drop_projects WHERE tracking_status = 'tracking'")
    tr = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM drop_projects WHERE tracking_status = 'new'")
    nw = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM drop_projects")
    tot = cur.fetchone()[0]
    conn.close()

    srcs = read_sources()
    act = sum(1 for s in srcs if s.get("enabled", True))
    return {"tracking": tr, "new": nw, "total": tot, "sources": f"{act}/{len(srcs)}"}

@app.get("/api/sources")
async def get_sources():
    return read_sources()

@app.post("/api/sources/{source_id}/toggle")
async def toggle_source(source_id: int):
    srcs = read_sources()
    for s in srcs:
        if s.get("id") == source_id:
            s["enabled"] = not s.get("enabled", True)
            break
    with open(SOURCES_PATH, "w", encoding="utf-8") as f:
        json.dump(srcs, f, ensure_ascii=False, indent=2)
    return {"success": True}

@app.get("/api/projects")
async def get_projects(status: str = "new"):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, source_platform, tier, score, raised_amount, 
               backers, category, stage, status_reward, is_testnet, 
               estimated_cost_usd, summary, source_url, tracking_status,
               sybil_rules, deep_strategy
        FROM drop_projects
        WHERE tracking_status = ?
        ORDER BY score DESC, id DESC
    """, (status,))
    projects = [dict(row) for row in cur.fetchall()]

    for p in projects:
        cur.execute("""
            SELECT id, step_number, title, action_type, status, target_url, is_autonomous
            FROM action_tasks
            WHERE project_id = ?
            ORDER BY step_number ASC, id ASC
        """, (p["id"],))
        p["tasks"] = [dict(t) for t in cur.fetchall()]

        cur.execute("SELECT title, details, created_at FROM project_daily_intel WHERE project_id = ? ORDER BY id DESC LIMIT 1", (p["id"],))
        intel = cur.fetchone()
        p["latest_intel"] = dict(intel) if intel else None

    conn.close()
    return projects

class StatusUpdate(BaseModel):
    status: str

# ВИПРАВЛЕНО: повноцінний async def без падінь у threadpool
@app.post("/api/projects/{project_id}/status")
async def update_project_status(project_id: int, payload: StatusUpdate):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE drop_projects SET tracking_status = ? WHERE id = ?", (payload.status, project_id))
        if payload.status == "tracking":
            cur.execute("UPDATE action_tasks SET status = 'PENDING', is_autonomous = 1 WHERE project_id = ?", (project_id,))
        conn.commit()
        conn.close()

        # Фоновий аналіз викликаємо безпечно
        if payload.status == "tracking":
            try:
                from ai_analyzer.deep_researcher import conduct_deep_research
                asyncio.create_task(conduct_deep_research(project_id))
            except Exception as e:
                print(f"[Warn] Deep research bypass: {e}")

        return {"success": True, "id": project_id, "status": payload.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ManualProject(BaseModel):
    title: str
    source_platform: Optional[str] = "Власне джерело"
    source_url: str
    category: Optional[str] = "Web3 / Testnet"
    summary: Optional[str] = ""
    tasks: Optional[str] = ""

@app.post("/api/projects/manual")
async def add_manual_project(payload: ManualProject):
    if not payload.title.strip() or not payload.source_url.strip():
        raise HTTPException(status_code=400, detail="Назва та посилання обов'язкові")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO drop_projects (
        title, source_platform, tier, score, raised_amount, backers,
        category, stage, status_reward, is_testnet, estimated_cost_usd,
        summary, source_url, tracking_status
    ) VALUES (?, ?, 'Tier-1', 92, 'Під наглядом', 'Обрано вручну', ?, 'Active', 'Очікується', 1, 0.0, ?, ?, 'new')
    """, (payload.title.strip(), payload.source_platform.strip(), payload.category.strip(), payload.summary.strip(), payload.source_url.strip()))
    proj_id = cur.lastrowid

    raw_tasks = [t.strip() for t in payload.tasks.split("\n") if t.strip()] or ["Підключити гаманець", "Отримати тестові токени", "Зробити свап"]
    for idx, t_title in enumerate(raw_tasks):
        cur.execute("""
        INSERT INTO action_tasks (project_id, step_number, title, action_type, network, status, target_url, is_autonomous, description)
        VALUES (?, ?, ?, 'task', 'EVM / Testnet', 'PENDING', ?, 1, '')
        """, (proj_id, idx + 1, t_title, payload.source_url.strip()))

    conn.commit()
    conn.close()
    return {"success": True, "project_id": proj_id}

@app.get("/api/signals")
async def get_market_signals():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM market_signals ORDER BY id DESC LIMIT 50")
    signals = [dict(row) for row in cur.fetchall()]
    conn.close()
    return signals

@app.post("/api/signals/scan")
async def trigger_market_scan():
    asyncio.create_task(run_market_scanner())
    return {"message": "Сканування запущено"}

@app.get("/api/market/chart")
async def get_chart(symbol: str = "BTC", period: str = "24h"):
    res = await get_klines_data(symbol, period)
    if "error" in res: raise HTTPException(status_code=400, detail=res["error"])
    return res

@app.get("/api/market/forecast")
async def get_forecast(symbol: str = "BTC", horizon: str = "24h"):
    res = await generate_ai_token_forecast(symbol, horizon)
    if "error" in res: raise HTTPException(status_code=400, detail=res["error"])
    return res

FRONTEND_DIR = os.path.join(ROOT_DIR, "web_tma", "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
async def index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web_tma.backend.server:app", host="0.0.0.0", port=8000, reload=True)