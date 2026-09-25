import os
import sys
import json
import asyncio
from urllib.parse import urlparse
from loguru import logger
from sqlalchemy import select, func
from playwright.async_api import async_playwright

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.database import async_session_maker, DropProject, ActionTask, TaskStatus, init_db
from execution.web3_signer import web3_signer

PROFILE_DIR = os.path.join(ROOT_DIR, "discovery", ".browser_profile")
TEST_WALLET_ADDRESS = web3_signer.account.address if web3_signer.account else "0x53D1C8dEBd784a958F8fD9e498c076bB8C3fF980"

WEB3_PROVIDER_MOCK = f"""
if (!window.ethereum) {{
    window.ethereum = {{
        isMetaMask: true,
        selectedAddress: '{TEST_WALLET_ADDRESS}',
        request: async function(req) {{
            if (req.method === 'eth_requestAccounts' || req.method === 'eth_accounts') {{
                return ['{TEST_WALLET_ADDRESS}'];
            }}
            if (req.method === 'eth_chainId') return '0xaa36a7';
            if (req.method === 'net_version') return '11155111';
            if (req.method === 'personal_sign') return '0x0000mockedsignature';
            return null;
        }},
        on: function(event, callback) {{}}
    }};
}}
"""

async def auto_connect_web3(page) -> bool:
    btn = await page.query_selector('button:has-text("Connect"), button:has-text("Connect Wallet"), a:has-text("Connect")')
    if btn:
        await btn.click()
        await asyncio.sleep(2)
        mm = await page.query_selector('button:has-text("MetaMask"), div:has-text("MetaMask")')
        if mm:
            await mm.click()
            await asyncio.sleep(2)
        return True
    return False

async def execute_task(page, task: ActionTask) -> bool:
    if not task.target_url:
        return False

    logger.info(f"🌐 [Executor (Фон)] Обробка {task.target_url}")
    await page.goto(task.target_url, timeout=50000, wait_until="domcontentloaded")
    await asyncio.sleep(3)

    await auto_connect_web3(page)

    if task.action_type in ["faucet", "checkin", "other"]:
        wallet_input = await page.query_selector('input[type="text"], input[placeholder*="0x" i], input[placeholder*="address" i]')
        if wallet_input:
            await wallet_input.fill(TEST_WALLET_ADDRESS)
            await asyncio.sleep(1)

        claim_btn = await page.query_selector('button:has-text("Claim"), button:has-text("Request"), button:has-text("Check in"), button:has-text("Verify")')
        if claim_btn:
            await claim_btn.click()
            logger.success("✓ Виконано дію/клейм у фоні!")
            await asyncio.sleep(3)
            return True

    return True

async def run_executor():
    await init_db()
    logger.info("🤖 Запуск Агента-Виконавця у ФОНОВОМУ режимі (без вікон)...")

    async with async_session_maker() as session:
        query = (
            select(ActionTask)
            .join(DropProject, ActionTask.project_id == DropProject.id)
            .where(func.lower(DropProject.tracking_status) == "tracking")
            .where(ActionTask.is_autonomous == True)
        )
        all_tasks = (await session.execute(query)).scalars().all()
        tasks = [t for t in all_tasks if str(t.status).upper().endswith("PENDING") or str(t.status).upper().endswith("APPROVED")]

        if not tasks:
            logger.info("Немає нових завдань у черзі.")
            return

        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                headless=True,  # Вікно браузера не з'являтиметься
                args=["--disable-blink-features=AutomationControlled", "--mute-audio"]
            )
            page = await context.new_page()
            await page.add_init_script(WEB3_PROVIDER_MOCK)

            for t in tasks:
                logger.info(f"▶ Фонова обробка #{t.id}: {t.title}")
                t.status = TaskStatus.EXECUTING
                await session.commit()

                success = False
                try:
                    success = await execute_task(page, t)
                except Exception as e:
                    logger.error(f"Помилка #{t.id}: {e}")

                t.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
                await session.commit()

            await context.close()
            logger.success("Усі завдання опрацьовано у фоні!")

if __name__ == "__main__":
    asyncio.run(run_executor())
