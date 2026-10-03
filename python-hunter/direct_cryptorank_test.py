import os
import sys
import asyncio
from bs4 import BeautifulSoup
from loguru import logger
from sqlalchemy import select

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.database import init_db, async_session_maker, DropProject
from discovery.browser import fetch_page_with_browser
from discovery.universal_scanner import process_item

async def run():
    await init_db()
    logger.info("📡 Підключення до CryptoRank Drop Hunting...")
    
    res = await fetch_page_with_browser("https://cryptorank.io/drophunting", scroll_down=True)
    html = res.get("html", "")
    
    if not html or "cryptorank" not in res.get("title", "").lower():
        logger.error(f"Не вдалося завантажити таблицю. Заголовок: {res.get('title')}")
        return

    soup = BeautifulSoup(html, "lxml")
    
    # Збір посилань на сторінки активностей
    raw_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].split("?")[0].split("#")[0]
        if "-activity" in href or ("/drophunting/" in href and len(href.strip("/").split("/")) > 4):
            clean = href if href.startswith("http") else f"https://cryptorank.io{href}"
            clean = clean.rstrip("/") + "/"
            if not any(bad in clean for bad in ["/funds/", "/exchanges/", "/tags/", "/ico/"]):
                if clean not in raw_links and clean != "https://cryptorank.io/drophunting/":
                    raw_links.append(clean)

    logger.info(f"Знайдено посилань на активності CryptoRank: {len(raw_links)}")

    if not raw_links:
        logger.warning("Таблиця ще провантажується або змінила селектори. Перевірте вікно браузера.")
        return

    # Фільтрація вже наявних у базі
    to_process = []
    async with async_session_maker() as session:
        for url in raw_links:
            q = select(DropProject).where(DropProject.source_url == url)
            exists = (await session.execute(q)).scalar_one_or_none()
            if not exists:
                to_process.append(url)

    logger.success(f"Нових проєктів, яких ще немає в базі: {len(to_process)}")

    added = 0
    # Беремо перші 10 нових для швидкої перевірки
    for target_url in to_process[:10]:
        slug = target_url.strip("/").split("/")[-1].replace("-activity", "").replace("-", " ").title()
        item = {
            "title": f"[CryptoRank] {slug}",
            "url": target_url,
            "text": ""
        }
        ok = await process_item(item, "CryptoRank Drops")
        if ok:
            added += 1
        await asyncio.sleep(1)

    logger.success(f"Завершено! Успішно додано до бази нових проєктів: {added}")

if __name__ == "__main__":
    asyncio.run(run())
