import os
import sys
import asyncio
import sqlite3
from loguru import logger

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "drop_hunter.db")

async def analyze_wallet_readiness():
    """Інспектує проєкти в статусі tracking та формує звіт готовності проти Sybil-фільтрів"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT p.id, p.title, p.stage, p.score, 
           COUNT(t.id) as total_tasks,
           SUM(CASE WHEN t.status = 'COMPLETED' THEN 1 ELSE 0 END) as done_tasks
    FROM drop_projects p
    LEFT JOIN action_tasks t ON p.id = t.project_id
    WHERE p.tracking_status = 'tracking'
    GROUP BY p.id
    """)
    projects = cur.fetchall()

    if not projects:
        logger.info("ℹ️ Немає проєктів у статусі '⭐ В роботі'. Додайте кілька карток у дашборді!")
        conn.close()
        return

    logger.info("=" * 70)
    logger.info("🧠 [Smart Advisor] Аудит гаманця проти критеріїв знімків (Snapshots):")
    logger.info("=" * 70)

    for pid, title, stage, score, total, done in projects:
        done = done or 0
        total = total or 1
        pct = int((done / total) * 100)

        # Розрахунок статусу захисту від мітки Sybil
        sybil_status = "🛡️ НАДІЙНО" if pct >= 80 else ("⚠️ РИЗИК ЗРІЗУ" if pct >= 40 else "🚨 НЕ КВАЛІФІКОВАНО")
        
        logger.info(f"📌 Проєкт: {title} | Бал потенціалу: {score}/100")
        logger.info(f"   Прогрес завдань: {done}/{total} ({pct}%) -> Статус кваліфікації: {sybil_status}")
        
        # Визначаємо критичний наступний крок
        cur.execute("""
        SELECT title, action_type, target_url 
        FROM action_tasks 
        WHERE project_id = ? AND status != 'COMPLETED'
        ORDER BY step_number ASC LIMIT 1
        """, (pid,))
        next_task = cur.fetchone()

        if next_task:
            logger.warning(f"   👉 Наступна критична дія: [{next_task[1].upper()}] {next_task[0]}")
            logger.info(f"      URL: {next_task[2]}")
        else:
            logger.success(f"   ✓ Усі обов'язкові ончейн-критерії закрито! Утримуйте баланс до TGE.")
        logger.info("-" * 70)

    conn.close()

if __name__ == "__main__":
    asyncio.run(analyze_wallet_readiness())
