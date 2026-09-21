import asyncio
import os
from playwright.async_api import async_playwright

PROFILE_DIR = os.path.join(os.getcwd(), "discovery", ".browser_profile")

async def unlock_cryptorank():
    print("=" * 60)
    print("ВІДКРИТТЯ CRYPTORANK У ВИДИМОМУ ВІКНІ")
    print("Якщо з'явиться віконце Cloudflare ('Підтвердіть, що ви людина') — просто клікніть його.")
    print("Сесія автоматично збережеться для всіх майбутніх сканувань.")
    print("=" * 60)

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,  # ВИДИМЕ ВІКНО
            channel="chrome", # використовує системний Chrome або Chromium
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"],
            viewport=None
        )
        page = await context.new_page()
        await page.goto("https://cryptorank.io/drophunting", wait_until="domcontentloaded")
        
        print("Очікування 20 секунд для завантаження та проходження перевірки...")
        for i in range(20, 0, -5):
            print(f"Залишилося: {i} сек...")
            await asyncio.sleep(5)

        title = await page.title()
        print(f"\n✓ Успішно! Заголовок сторінки: '{title}'")
        print("Cookies та сесія збережені в папку .browser_profile.")
        await context.close()

if __name__ == "__main__":
    asyncio.run(unlock_cryptorank())
