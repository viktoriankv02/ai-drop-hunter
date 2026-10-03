import os
import sys
import asyncio
from playwright.async_api import async_playwright
from loguru import logger

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROFILE_DIR = os.path.join(ROOT_DIR, "discovery", ".browser_profile")

async def fetch_page_with_browser(url: str, scroll_down: bool = False, wait_seconds: int = 4) -> dict:
    """Завантажує сторінку у фоновому режимі (headless) без відкриття вікон на екрані"""
    html = ""
    try:
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                headless=True,  # Тихий фоновий режим
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--mute-audio"
                ],
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.debug(f"[Фон] Сканування: {url}")
            await page.goto(url, timeout=45000, wait_until="domcontentloaded")
            
            if scroll_down:
                await page.evaluate("window.scrollBy(0, 1500)")
                await asyncio.sleep(2)
            else:
                await asyncio.sleep(wait_seconds)
            
            html = await page.content()
            await context.close()
    except Exception as e:
        logger.warning(f"Помилка фонового завантаження ({url}): {e}")
    
    return {"html": html}
