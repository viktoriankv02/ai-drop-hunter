import asyncio
import json
import sys
from loguru import logger
from sqlalchemy import select
from core.database import init_db, async_session_maker, DropProject, ActionTask, TaskStatus
from discovery.aggregators.cryptorank import CryptoRankScraper
from discovery.quest_platforms.galxe import GalxeScraper
from discovery.aggregators.airdrops_io import AirdropsIoScraper
from ai_analyzer.scoring import analyze_cryptorank_project

async def run_round_robin_scan(total_target: int = 6):
    """
    Сканує платформи по черзі:
    1 проект з Сайту А -> 1 проект з Сайту Б -> 1 проект з Сайту В -> повернення до А
    """
    await init_db()
    logger.info(f"Запуск циклічного диспетчера. Ціль: {total_target} нових проєктів.")

    # Ініціалізація джерел
    cryptorank = CryptoRankScraper()
    galxe = GalxeScraper()
    airdrops = AirdropsIoScraper()

    platforms = [
        {"name": "CryptoRank", "client": cryptorank, "type": "browser_seed"},
        {"name": "Galxe", "client": galxe, "type": "api"},
        {"name": "Airdrops.io", "client": airdrops, "type": "browser_html"}
    ]

    added_total = 0
    current_platform_idx = 0
    consecutive_empty = 0

    async with async_session_maker() as session:
        while added_total < total_target:
            if consecutive_empty >= len(platforms) * 2:
                logger.warning("Усі джерела тимчасово вичерпали нові проєкти.")
                break

            current = platforms[current_platform_idx]
            p_name = current["name"]
            client = current["client"]
            p_type = current["type"]

            logger.info(f"\n---> [Черга: {p_name}] Пошук нового проєкту...")

            # Отримання списку кандидатів
            candidate_item = None
            try:
                if p_type == "browser_seed":
                    candidates = await client.parse_catalog(limit=15)
                elif p_type == "api":
                    candidates = await client.get_candidate_urls()
                elif p_type == "browser_html":
                    candidates = await client.get_candidate_urls()
                else:
                    candidates = []
            except Exception as e:
                logger.error(f"Помилка отримання каталогу від {p_name}: {e}")
                candidates = []

            # Пошук першого проєкту, якого ще немає в базі
            for item in candidates:
                url = item["url"]
                query = select(DropProject).where(DropProject.source_url == url)
                existing = (await session.execute(query)).scalar_one_or_none()
                if not existing:
                    candidate_item = item
                    break

            if not candidate_item:
                logger.warning(f"[{p_name}] Немає нових проєктів для обробки. Перехід до наступного сайту.")
                consecutive_empty += 1
                current_platform_idx = (current_platform_idx + 1) % len(platforms)
                continue

            consecutive_empty = 0
            target_url = candidate_item["url"]
            title = candidate_item["title"]
            logger.info(f"[{p_name}] Знайдено новий проєкт: {title} ({target_url})")

            # Отримання повного гайду / опису
            try:
                if p_type == "browser_seed":
                    page_data = await client.parse_project_page(target_url)
                    content = json.dumps(page_data["raw_json"], ensure_ascii=False) if (page_data and "raw_json" in page_data) else (page_data.get("raw_text", "") if page_data else title)
                elif p_type == "api":
                    content = await client.fetch_details(candidate_item)
                else:
                    content = await client.fetch_details(target_url)
                
                if not content:
                    content = title

                # ШІ-аналіз через Gemini
                logger.info(f"ШІ-аналітик структурує дані для: {title}...")
                analysis = await analyze_cryptorank_project(content, target_url)

                project = DropProject(
                    title=analysis.project_name,
                    source_url=target_url,
                    source_platform=p_name.lower().replace(".", "_"),
                    tier=analysis.tier,
                    score=analysis.score,
                    raised_amount=analysis.raised_amount,
                    backers=analysis.backers,
                    category=analysis.category,
                    stage=analysis.stage,
                    status_reward=analysis.status_reward,
                    is_testnet=analysis.is_testnet_only,
                    estimated_cost_usd=analysis.estimated_gas_cost_usd,
                    summary=analysis.summary,
                    guide_markdown=analysis.guide_markdown,
                    raw_content=content[:2000]
                )
                session.add(project)
                await session.flush()

                for t in analysis.tasks:
                    task = ActionTask(
                        project_id=project.id,
                        step_number=t.step_number,
                        title=t.title,
                        action_type=t.action_type,
                        network=t.network,
                        is_autonomous=t.is_autonomous,
                        target_url=t.target_url,
                        description=t.description,
                        status=TaskStatus.APPROVED if t.is_autonomous else TaskStatus.PENDING
                    )
                    session.add(task)

                await session.commit()
                added_total += 1
                logger.success(f"✓ [{p_name}] Успішно збережено: {analysis.project_name} | {analysis.tier} | {analysis.score}/100 | Прогрес: {added_total}/{total_target}")

                # Пауза для ліміту 5 RPM перед наступним сайтом
                logger.info("Пауза 13с перед переходом до наступного ресурсу...")
                await asyncio.sleep(13)

            except Exception as e:
                logger.error(f"Помилка при обробці {target_url}: {e}")

            # Перехід до наступного сайту по колу
            current_platform_idx = (current_platform_idx + 1) % len(platforms)

    logger.success(f"\nЦикл завершено! Загалом додано нових проєктів: {added_total}")

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    asyncio.run(run_round_robin_scan(total_target=count))
