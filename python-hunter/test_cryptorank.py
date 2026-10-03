import asyncio
import json
from loguru import logger
from sqlalchemy import select
from core.database import init_db, async_session_maker, DropProject, ActionTask, TaskStatus
from discovery.aggregators.cryptorank import CryptoRankScraper
from ai_analyzer.scoring import analyze_cryptorank_project

async def main():
    await init_db()
    scraper = CryptoRankScraper()
    
    target_url = "https://cryptorank.io/ru/drophunting/arc-chain-activity911/"
    logger.info(f"Завантаження проєкту: {target_url}")

    data = await scraper.parse_project_page(target_url)
    if not data:
        logger.error("Не вдалося завантажити сторінку через браузер.")
        return

    content = json.dumps(data["raw_json"], ensure_ascii=False) if "raw_json" in data else data["raw_text"]
    
    logger.info("ШІ структурує гілки активності (Arc House, Мейнет, Тестнет), дедлайни та завдання...")
    analysis = await analyze_cryptorank_project(content, target_url)

    logger.success(f"Проєкт: {analysis.project_name}")
    logger.info(f"Категорія: {analysis.category} | Стадія: {analysis.stage}")
    logger.info(f"Інвестиції: {analysis.raised_amount} | Фонди: {analysis.backers}")
    logger.info(f"Рівень: {analysis.tier} | Оцінка: {analysis.score}/100 | Винагорода: {analysis.status_reward}")
    logger.info(f"Згенеровано детальних завдань: {len(analysis.tasks)}")

    async with async_session_maker() as session:
        # Очищуємо попередній дублікат перед записом
        existing = (await session.execute(select(DropProject).where(DropProject.source_url == target_url))).scalar_one_or_none()
        if existing:
            await session.delete(existing)
            await session.commit()

        project = DropProject(
            title=analysis.project_name,
            source_url=target_url,
            source_platform="cryptorank",
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
        logger.success("Дані по Arc Chain успішно записано у базу drop_hunter.db!")

if __name__ == "__main__":
    asyncio.run(main())
