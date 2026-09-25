import os
import sys
import json
import asyncio
import httpx
from bs4 import BeautifulSoup
from loguru import logger
import sqlite3

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "drop_hunter.db")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

async def inspect_project_updates(client: httpx.AsyncClient, project: dict):
    pid = project["id"]
    title = project["title"]
    logger.info(f"🔎 [Daily Sentinel] Перевірка оновлень для #{pid} {title}...")

    # Шукаємо свіжі згадки та оголошення
    search_url = f"https://html.duckduckgo.com/html/?q={title}+testnet+new+task+announcement+update"
    news_items = []

    try:
        res = await client.get(search_url, timeout=12)
        soup = BeautifulSoup(res.text, "lxml")
        results = soup.find_all("div", class_="result__body")
        for r in results[:2]:
            snippet = r.find("a", class_="result__snippet")
            if snippet:
                txt = snippet.get_text(strip=True)
                if any(w in txt.lower() for w in ["phase", "snapshot", "new", "airdrop", "faucet", "claim", "mainnet", "quest"]):
                    news_items.append(txt)
    except Exception as e:
        logger.warning(f"Збій пошуку оновлень для {title}: {e}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if news_items:
        intel_text = " • ".join(news_items[:2])
        # Записуємо в історію оновлень проєкту
        cur.execute("""
        INSERT INTO project_daily_intel (project_id, intel_type, title, details, action_required)
        VALUES (?, 'UPDATE', 'Знайдено нові згадки / завдання', ?, 1)
        """, (pid, intel_text[:350]))
        logger.success(f"✓ [{title}] Виявлено потенційні оновлення кампанії!")
    else:
        cur.execute("""
        INSERT INTO project_daily_intel (project_id, intel_type, title, details, action_required)
        VALUES (?, 'CHECK', 'Регулярний аудит проведено', 'Нових критичних фаз або закриття кампанії за останні 24 год не зафіксовано.', 0)
        """, (pid,))
        logger.info(f"[{title}] Стан стабільний, нових завдань не додано.")

    conn.commit()
    conn.close()

async def run_daily_sentinel():
    logger.info("🛡️ [Daily Sentinel] Запуск щоденного обходу проєктів 'В роботі'...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, title, source_url FROM drop_projects WHERE tracking_status = 'tracking'")
    tracked = [dict(r) for r in cur.fetchall()]
    conn.close()

    if not tracked:
        logger.info("Немає проєктів у статусі 'В роботі' для моніторингу.")
        return

    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
        for p in tracked:
            await inspect_project_updates(client, p)
            await asyncio.sleep(2)

    logger.success("✓ Щоденний моніторинг усіх активних проєктів завершено!")

if __name__ == "__main__":
    asyncio.run(run_daily_sentinel())