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

async def run_cryptorank_deep(limit: int = 25):
    await init_db()
    logger.info("🚀 Запуск цільового скрапінгу CryptoRank Drop Hunting...")
    
    url = "https://cryptorank.io/drophunting"
    res = await fetch_page_with_browser(url, scroll_down=True)
    html = res.get("html", "")
    
    if not html:
        logger.error("Не вдалося завантажити сторінку CryptoRank.")
        return

    soup = BeautifulSoup(html, "lxml")
    project_links = []
    
    for a in soup.find_all("a", href=True):
        href = a["href"].split("?")[0].split("#")[0]
        # Беремо виключно сторінки активностей
        if "-activity" in href or ("/drophunting/" in href and len(href.strip("/").split("/")) > 4):
            clean_url = href if href.startswith("http") else f"https://cryptorank.io{href}"
            clean_url = clean_url.rstrip("/") + "/"
            
            # Ігноруємо службові сторінки
            if not any(x in clean_url for x in ["/tag/", "/category/", "/funds/", "/exchanges/"]):
                if clean_url not in project_links and clean_url != "https://cryptorank.io/drophunting/":
                    project_links.append(clean_url)

    logger.info(f"Знайдено посилань на активності: {len(project_links)}")
    
    # Фільтруємо ті, що вже є в базі
    new_links = []
    async with async_session_maker() as session:
        for purl in project_links:
            q = select(DropProject).where(DropProject.source_url == purl)
            exists = (await session.execute(q)).scalar_one_or_none()
            if not exists:
                new_links.append(purl)
            else:
                logger.debug(f"Вже є в базі: {exists.title}")

    logger.success(f"Нових проєктів для обробки ШІ: {len(new_links)} (беремо до {limit})")
    
    added_count = 0
    for target_url in new_links[:limit]:
        title = target_url.strip("/").split("/")[-1].replace("-activity", "").replace("-", " ").title()
        item = {
            "title": f"[CryptoRank] {title}",
            "url": target_url,
            "text": ""
        }
        added = await process_item(item, "CryptoRank Drops")
        if added:
            added_count += 1
        await asyncio.sleep(1)

    logger.success(f"Обробку завершено! Додано нових карток: {added_count}")

if __name__ == "__main__":
    asyncio.run(run_cryptorank_deep(limit=25))
