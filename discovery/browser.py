import os
import sys
import asyncio
from loguru import logger
from playwright.async_api import async_playwright

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROFILE_DIR = os.path.join(ROOT_DIR, "discovery", ".browser_profile")

async def fetch_page_with_browser(url: str, scroll_down: bool = True, timeout_ms: int = 50000) -> dict:
    os.makedirs(PROFILE_DIR, exist_ok=True)
    
    async with async_playwright() as p:
        # Запускаємо через реальний профіль у видимому вікні, щоб Cloudflare не блокував запити
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--window-size=1280,800"
            ],
            viewport={"width": 1280, "height": 800}
        )

        page = await context.new_page()

        try:
            logger.info(f"[Browser] Відкриття: {url}")
            await page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
            
            # Чекаємо 4 секунди на завантаження React / Next.js
            await asyncio.sleep(4)

            title = await page.title()
            if any(cf in title.lower() for cf in ["just a moment", "трохи зачекайте", "cloudflare"]):
                logger.warning("[Browser] Чекаємо авто-проходження перевірки Cloudflare...")
                await asyncio.sleep(6)

            if scroll_down:
                for _ in range(4):
                    await page.evaluate("window.scrollBy(0, 1200)")
                    await asyncio.sleep(1.2)

            html = await page.content()
            final_title = await page.title()
            await context.close()
            return {"html": html, "title": final_title}

        except Exception as e:
            logger.error(f"[Browser] Помилка на {url}: {e}")
            try:
                await context.close()
            except Exception:
                pass
            return {"html": "", "title": ""}
