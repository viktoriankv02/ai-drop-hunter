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

from core.database import async_session_maker, DropProject, ActionTask, TaskStatus, AgentSkill, init_db
from ai_analyzer.gateway import llm_gateway

PROFILE_DIR = os.path.join(ROOT_DIR, "discovery", ".browser_profile")
TEST_WALLET_ADDRESS = os.getenv("TEST_WALLET_ADDRESS", "0x53D1C8dEBd784a958F8fD9e498c076bB8C3fF980")

async def get_stored_skill(domain: str, action_type: str):
    async with async_session_maker() as session:
        q = select(AgentSkill).where(AgentSkill.domain == domain, AgentSkill.action_type == action_type)
        return (await session.execute(q)).scalar_one_or_none()

async def teach_skill(domain: str, action_type: str, input_sel: str, btn_sel: str):
    async with async_session_maker() as session:
        skill = await get_stored_skill(domain, action_type)
        if skill:
            skill.success_count += 1
            skill.input_selector = input_sel
            skill.button_selector = btn_sel
        else:
            skill = AgentSkill(
                domain=domain,
                action_type=action_type,
                input_selector=input_sel,
                button_selector=btn_sel,
                success_count=1
            )
            session.add(skill)
        await session.commit()
        logger.success(f"🧠 [Пам'ять Агента] Засвоєно селектори для {domain} ({action_type})!")

async def ask_llm_for_elements(dom_summary: str, action_type: str) -> dict:
    prompt = f"""Елементи сторінки:
{dom_summary}

Дія: "{action_type}".
Знайди селектор поля гаманця (input_selector) та кнопки (button_selector).
Відповідай тільки JSON:
{{"input_selector": "знайдений селектор або null", "button_selector": "знайдений селектор або null"}}
"""
    res = await llm_gateway.complete(prompt=prompt, system_prompt="You are a browser automation agent. Output JSON only.")
    try:
        clean = res.strip()
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif "```" in clean:
            clean = clean.split("```")[1].split("```")[0].strip()
        return json.loads(clean)
    except Exception:
        return {"input_selector": None, "button_selector": None}

async def execute_task_with_learning(page, task: ActionTask) -> bool:
    if not task.target_url:
        return False

    domain = urlparse(task.target_url).netloc
    logger.info(f"🌐 [Executor] Відкриття {task.target_url} (домен: {domain})")
    
    await page.goto(task.target_url, timeout=50000, wait_until="domcontentloaded")
    await asyncio.sleep(3)

    skill = await get_stored_skill(domain, task.action_type)
    if skill and skill.button_selector:
        logger.info(f"⚡ [Пам'ять] Застосування готової навички для {domain}...")
        try:
            if skill.input_selector:
                await page.fill(skill.input_selector, TEST_WALLET_ADDRESS, timeout=4000)
            await page.click(skill.button_selector, timeout=4000)
            logger.success("✓ Виконано за готовим рецептом!")
            return True
        except Exception:
            logger.warning("Селектор змінився, оновлюємо навчання...")

    inputs = await page.query_selector_all('input')
    buttons = await page.query_selector_all('button, a[role="button"]')

    dom_samples = []
    for idx, inp in enumerate(inputs[:5]):
        p_holder = await inp.get_attribute("placeholder") or ""
        i_type = await inp.get_attribute("type") or "text"
        dom_samples.append(f"Input {idx}: type='{i_type}', placeholder='{p_holder}'")

    for idx, btn in enumerate(buttons[:10]):
        text = (await btn.inner_text()).strip()[:30]
        if text:
            dom_samples.append(f"Button {idx}: text='{text}'")

    summary_str = "\n".join(dom_samples)
    decision = await ask_llm_for_elements(summary_str, task.action_type)
    
    btn_target = decision.get("button_selector")
    inp_target = decision.get("input_selector")

    executed = False
    if not inp_target:
        wallet_input = await page.query_selector('input[type="text"], input[placeholder*="0x" i], input[placeholder*="address" i]')
        if wallet_input:
            await wallet_input.fill(TEST_WALLET_ADDRESS)
            inp_target = 'input[placeholder*="0x" i]'
            executed = True

    if not btn_target:
        claim_btn = await page.query_selector('button:has-text("Claim"), button:has-text("Request"), button:has-text("Check in"), button:has-text("Daily"), button:has-text("Connect")')
        if claim_btn:
            await claim_btn.click()
            btn_target = 'button:has-text("Claim")'
            executed = True

    if executed:
        await teach_skill(domain, task.action_type, inp_target or "", btn_target or "")
        return True

    return True

async def run_executor():
    await init_db()
    logger.info("🤖 Запуск Автономного Агента-Виконавця...")

    async with async_session_maker() as session:
        # Гнучкий пошук без залежності від регістру
        query = (
            select(ActionTask)
            .join(DropProject, ActionTask.project_id == DropProject.id)
            .where(func.lower(DropProject.tracking_status) == "tracking")
            .where(ActionTask.is_autonomous == True)
        )
        all_tasks = (await session.execute(query)).scalars().all()
        
        # Фільтруємо статус без чутливості до регістру
        tasks = [
            t for t in all_tasks 
            if str(t.status).upper().endswith("PENDING") or str(t.status).upper().endswith("APPROVED")
        ]

        if not tasks:
            logger.info("Немає активних завдань для виконання.")
            return

        logger.info(f"Знайдено завдань до виконання: {len(tasks)}")

        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = await context.new_page()

            for t in tasks:
                logger.info(f"▶ Обробка завдання #{t.id}: {t.title} ({t.action_type})")
                t.status = TaskStatus.EXECUTING
                await session.commit()

                success = False
                try:
                    success = await execute_task_with_learning(page, t)
                except Exception as e:
                    logger.error(f"Збій завдання #{t.id}: {e}")

                t.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
                await session.commit()
                logger.info(f"Статус #{t.id} оновлено на: {t.status.value}")

            await context.close()
            logger.success("Всі доступні завдання оброблено!")

if __name__ == "__main__":
    asyncio.run(run_executor())
