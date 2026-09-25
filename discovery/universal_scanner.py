import os
import sys
import json
import asyncio
import re
import httpx
from bs4 import BeautifulSoup
from loguru import logger
import sqlite3
from datetime import datetime, timedelta
from playwright.async_api import async_playwright

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "drop_hunter.db")
SOURCES_FILE = os.path.join(ROOT_DIR, "sources", "resources.json")
PROFILE_DIR = os.path.join(ROOT_DIR, "discovery", ".browser_profile")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7"
}

THREE_MONTHS_AGO = datetime.now() - timedelta(days=90)

def load_sources():
    if not os.path.exists(SOURCES_FILE): return []
    try:
        with open(SOURCES_FILE, "r", encoding="utf-8-sig") as f:
            return [s for s in json.load(f) if s.get("enabled", True)]
    except Exception: return []

def save_project(p: dict) -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM drop_projects WHERE title = ? OR source_url = ?", (p["title"], p["source_url"]))
    if cur.fetchone():
        conn.close()
        return "EXISTS"

    is_testnet = 1 if "testnet" in p.get("stage", "").lower() or p.get("is_testnet") else 0

    cur.execute("""
    INSERT INTO drop_projects (
        title, source_platform, tier, score, raised_amount, backers,
        category, stage, status_reward, is_testnet, estimated_cost_usd,
        summary, source_url, tracking_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, 'Active', 'Підтверджено', ?, 0.0, ?, ?, 'new')
    """, (
        p["title"], p["source_platform"], p.get("tier", "Tier-2"), p.get("score", 85),
        p.get("raised_amount", "Оцінюється"), p.get("backers", "Венчурні фонди"),
        p.get("category", "L1 / L2 / DeFi"), is_testnet, p.get("summary", ""), p["source_url"]
    ))
    proj_id = cur.lastrowid

    tasks = [
        "Підключити гаманець до офіційної платформи",
        "Отримати тестові токени через кран / верифікацію",
        "Виконати обмін (Swap) або взаємодію з контрактом"
    ]
    for idx, t_title in enumerate(tasks):
        cur.execute("""
        INSERT INTO action_tasks (project_id, step_number, title, action_type, network, status, target_url, is_autonomous, description)
        VALUES (?, ?, ?, 'task', 'EVM / Testnet', 'PENDING', ?, 1, '')
        """, (proj_id, idx + 1, t_title, p["source_url"]))

    conn.commit()
    conn.close()
    return "ADDED"

# 1. CRYPTORANK: швидкий DOM-скролер без networkidle
async def scan_cryptorank():
    logger.info("🌐 [CryptoRank] Запуск браузера для вивантаження каталогу (до 200 проєктів)...")
    added, exist = 0, 0
    os.makedirs(PROFILE_DIR, exist_ok=True)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--headless=new", "--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            context = await browser.new_context(user_agent=HEADERS["User-Agent"], viewport={"width": 1920, "height": 1080})
            page = await context.new_page()

            # Завантажуємо тільки DOM без вічного очікування мережі
            logger.info("Відкриття сторінки https://cryptorank.io/drophunting...")
            await page.goto("https://cryptorank.io/drophunting", wait_until="domcontentloaded", timeout=20000)
            await asyncio.sleep(3)

            # Прокрутка вниз для завантаження списку
            for s in range(5):
                await page.evaluate("window.scrollBy(0, 2500)")
                await asyncio.sleep(1.2)

            links = await page.query_selector_all('a[href*="/drophunting/"]')
            logger.info(f"[CryptoRank] На сторінці знайдено {len(links)} посилань")

            seen = set()
            for a in links:
                href = await a.get_attribute("href")
                if not href or href == "/drophunting": continue
                slug = href.strip("/").split("/")[-1].replace("-activity", "")
                if slug in seen or any(x in slug for x in ["funds", "tags", "ico"]): continue
                seen.add(slug)

                text = await a.inner_text()
                title = text.strip().split("\n")[0] if text else slug.replace("-", " ").title()
                if len(title) < 2 or "view all" in title.lower():
                    title = slug.replace("-", " ").title()

                full_url = href if href.startswith("http") else f"https://cryptorank.io{href}"
                tier = "Tier-1" if any(k in title.lower() for k in ["monad", "story", "bera", "nexus", "abstract", "movement", "sonic", "fuel", "sui"]) else "Tier-2"

                proj = {
                    "title": title,
                    "source_platform": "CryptoRank",
                    "tier": tier,
                    "score": 92 if tier == "Tier-1" else 82,
                    "raised_amount": "Раунд фінансування",
                    "backers": "Top VCs" if tier == "Tier-1" else "Венчурні фонди",
                    "category": "L1 / L2 / Testnet",
                    "summary": f"Активний тестнет та кампанія {title} на CryptoRank.",
                    "source_url": full_url,
                    "is_testnet": True
                }

                st = save_project(proj)
                if st == "ADDED":
                    added += 1
                    logger.success(f"✓ [CryptoRank #{added}] Додано: {title}")
                else:
                    exist += 1

            await browser.close()
    except Exception as e:
        logger.error(f"Помилка CryptoRank: {e}")

    logger.info(f"🏁 [CryptoRank] Додано нових: {added} | Вже було в базі: {exist}")

# 2. INCRYPTED: пагінація без блокувань
async def scan_incrypted(client: httpx.AsyncClient):
    logger.info("🌐 [Incrypted] Сканування гайдів...")
    added, exist = 0, 0

    for page_idx in range(1, 4):
        url = f"https://incrypted.com/airdrops/page/{page_idx}/" if page_idx > 1 else "https://incrypted.com/airdrops/"
        try:
            res = await client.get(url, timeout=12)
            if res.status_code != 200: break
            soup = BeautifulSoup(res.text, "lxml")
            
            # Шукаємо всі посилання на гайди
            links = soup.find_all("a", href=True)
            for a in links:
                h = a["href"]
                txt = a.get_text(strip=True)
                if "/airdrop" in h and len(txt) > 5 and not any(x in txt.lower() for x in ["всі", "новини", "читати"]):
                    clean_name = txt.split(":")[0].replace("Як отримати аірдроп від", "").replace("Гайд по тестнету", "").replace("Гайд по", "").strip()
                    if len(clean_name) < 3 or len(clean_name) > 40: continue

                    proj = {
                        "title": clean_name,
                        "source_platform": "Incrypted",
                        "tier": "Tier-2",
                        "score": 84,
                        "raised_amount": "Раунд закрито",
                        "backers": "Венчурні фонди",
                        "category": "Testnet / DeFi",
                        "summary": txt,
                        "source_url": h,
                        "is_testnet": True
                    }
                    st = save_project(proj)
                    if st == "ADDED":
                        added += 1
                        logger.success(f"✓ [Incrypted #{added}] Додано: {clean_name}")
                    else:
                        exist += 1
        except Exception as e:
            logger.debug(f"Incrypted помилка: {e}")
            break

    logger.info(f"🏁 [Incrypted] Додано нових: {added} | Вже було в базі: {exist}")

# 3. AIRDROPS.IO
async def scan_airdrops_io(client: httpx.AsyncClient):
    logger.info("🌐 [Airdrops.io] Сканування Hot та Latest...")
    added, exist = 0, 0
    for u in ["https://airdrops.io/hot/", "https://airdrops.io/"]:
        try:
            res = await client.get(u, timeout=12)
            if res.status_code != 200: continue
            soup = BeautifulSoup(res.text, "lxml")
            for a in soup.find_all("a", href=True):
                h = a["href"]
                t = a.get_text(strip=True)
                if "airdrops.io/" in h and len(t) > 2 and not any(x in t.lower() for x in ["view", "airdrop", "contact", "privacy"]):
                    proj = {
                        "title": t[:35],
                        "source_platform": "Airdrops.io",
                        "tier": "Tier-2",
                        "score": 82,
                        "raised_amount": "Не оголошено",
                        "backers": "Екосистемні гранти",
                        "category": "Testnet",
                        "summary": f"Активність {t} з Airdrops.io",
                        "source_url": h,
                        "is_testnet": True
                    }
                    st = save_project(proj)
                    if st == "ADDED":
                        added += 1
                        logger.success(f"✓ [Airdrops.io #{added}] Додано: {t[:35]}")
                    else:
                        exist += 1
        except Exception: pass

    logger.info(f"🏁 [Airdrops.io] Додано нових: {added} | Вже було в базі: {exist}")

# 4. TELEGRAM: останні 3 місяці
async def scan_telegram(client: httpx.AsyncClient, source: dict):
    name = source.get("name", "TG")
    url = source.get("url", "")
    added = 0
    try:
        res = await client.get(url, timeout=10)
        if res.status_code != 200: return
        soup = BeautifulSoup(res.text, "lxml")
        messages = soup.find_all("div", class_="tgme_widget_message_wrap")

        for msg in reversed(messages):
            time_el = msg.find("time")
            if time_el and time_el.has_attr("datetime"):
                try:
                    dt = datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00")).replace(tzinfo=None)
                    if dt < THREE_MONTHS_AGO: continue
                except Exception: pass

            text_el = msg.find("div", class_="tgme_widget_message_text")
            if not text_el: continue
            full_txt = text_el.get_text("\n", strip=True)
            if len(full_txt) < 45 or any(s in full_txt.lower() for s in ["реклама", "розіграш", "канал продається"]):
                continue

            bold = text_el.find(["b", "strong"])
            title = bold.get_text(strip=True) if bold else full_txt.split("\n")[0]
            title = re.sub(r"[#🔥⚡🚀🎁👉💎]", "", title).strip()
            if len(title) > 35: title = title[:35].strip() + "..."
            if len(title) < 3 or "web3 drop" in title.lower(): continue

            links = text_el.find_all("a", href=True)
            target = ""
            for a in links:
                if "t.me" not in a["href"] and not a["href"].startswith("tg://"):
                    target = a["href"]; break
            if not target and links: target = links[0]["href"]
            if not target: continue

            proj = {
                "title": title,
                "source_platform": name,
                "tier": "Tier-1" if any(w in full_txt.lower() for w in ["paradigm", "a16z", "tier-1"]) else "Tier-2",
                "score": 85,
                "raised_amount": "Деталі в пості",
                "backers": "Венчурні фонди",
                "category": "Airdrop / Testnet",
                "summary": full_txt[:260] + "...",
                "source_url": target,
                "is_testnet": True
            }
            if save_project(proj) == "ADDED":
                added += 1
                logger.success(f"✓ [{name} #{added}] Додано: {title}")
    except Exception: pass

async def main():
    logger.info("🚀 Запуск повного збору: сайти без обмежень, Telegram - 3 місяці...")
    # 1. CryptoRank
    await scan_cryptorank()

    # 2. Incrypted + Airdrops.io + Telegram
    sources = load_sources()
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
        await scan_incrypted(client)
        await scan_airdrops_io(client)

        for s in sources:
            if s.get("type") == "telegram" or "t.me" in s.get("url", ""):
                await scan_telegram(client, s)
                await asyncio.sleep(0.4)

    logger.success("✓ Збір завершено! Усі нові проєкти додані до бази.")

if __name__ == "__main__":
    asyncio.run(main())