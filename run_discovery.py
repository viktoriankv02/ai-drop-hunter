import asyncio
from loguru import logger
from sqlalchemy import select
from core.database import init_db, async_session_maker, DropProject, ActionTask, TaskStatus
from discovery.quest_platforms.galxe import GalxeScraper
from ai_analyzer.scoring import analyze_drop_announcement

async def run_pipeline():
    await init_db()
    scraper = GalxeScraper()
    items = await scraper.parse_latest()

    if not items:
        logger.warning("Квестів на Galxe не виявлено або API недоступний.")
        return

    async with async_session_maker() as session:
        # Аналізуємо перший знайдений трендовий квест
        item = items[0]
        query = select(DropProject).where(DropProject.source_url == item["url"])
        existing = (await session.execute(query)).scalar_one_or_none()
        if existing:
            logger.info(f"Квест вже збережено в базі: {item['title']}")
            return

        logger.info(f"Аналіз квесту через ШІ: {item['title']}")
        try:
            analysis = await analyze_drop_announcement(item["raw_text"], item["url"])

            project = DropProject(
                title=analysis.project_name,
                source_url=item["url"],
                source_platform=item["source_platform"],
                tier=analysis.tier,
                score=analysis.score,
                is_testnet=analysis.is_testnet_only,
                estimated_cost_usd=analysis.estimated_gas_cost_usd,
                summary=analysis.summary,
                raw_content=item["raw_text"]
            )
            session.add(project)
            await session.flush()

            for task in analysis.tasks:
                action = ActionTask(
                    project_id=project.id,
                    action_type=task.action_type,
                    network=task.network,
                    is_autonomous=task.is_autonomous,
                    status=TaskStatus.APPROVED if task.is_autonomous else TaskStatus.PENDING,
                    payload=task.description
                )
                session.add(action)

            await session.commit()
            logger.success(f"Збережено: {analysis.project_name} | {analysis.tier} | Балів: {analysis.score}")

        except Exception as e:
            logger.error(f"Помилка обробки {item['url']}: {e}")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
