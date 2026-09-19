import json
from playwright.async_api import async_playwright
from loguru import logger

async def fetch_page_with_browser(url: str, scroll_down: bool = False) -> dict:
    """Завантажує сторінку через Chromium з маскуванням під звичайного користувача"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            viewport={"width": 1440, "height": 900},
            locale="uk-UA"
        )
        page = await context.new_page()

        # Приховуємо прапорець автоматизації браузера від Cloudflare
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        logger.info(f"[browser] Відкриття сторінки: {url}")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(3500)

            title = await page.title()
            logger.info(f"[browser] Заголовок сторінки: {title}")

            if scroll_down:
                for _ in range(2):
                    await page.evaluate("window.scrollBy(0, 1000)")
                    await page.wait_for_timeout(1500)

            next_data = await page.evaluate("() => window.__NEXT_DATA__ || null")
            html = await page.content()

            await browser.close()
            return {
                "next_data": next_data,
                "html": html
            }
        except Exception as e:
            logger.error(f"[browser] Помилка завантаження {url}: {e}")
            await browser.close()
            return {"next_data": None, "html": ""}
