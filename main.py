import asyncio
from loguru import logger
from core.database import init_db, async_session_maker, DropProject, ActionTask, TaskStatus
from ai_analyzer.scoring import analyze_drop_announcement

async def main():
    logger.info("1. Ініціалізація бази SQLite...")
    await init_db()
    logger.success("База даних готова.")

    sample_announcement = """
    Monad Testnet Airdrop Campaign is Live on Galxe!
    Monad raises $225M led by Paradigm. The reward for testnet participation is confirmed.
    Actions required:
    1. Daily Check-in on Galxe to claim points.
    2. Claim Sepolia test tokens from faucet.
    3. Deploy a sample Counter contract on Monad Testnet.
    No real money required.
    """
    sample_url = "https://app.galxe.com/quest/monad-testnet"

    logger.info("2. Запуск аналізу через ШІ...")
    try:
        result = await analyze_drop_announcement(sample_announcement, sample_url)
        logger.success(f"Аналіз завершено: {result.project_name} | {result.tier} | Оцінка: {result.score}/100")
        logger.info(f"Знайдено завдань: {len(result.tasks)}")

        async with async_session_maker() as session:
            project = DropProject(
                title=result.project_name,
                source_url=sample_url,
                source_platform="galxe",
                tier=result.tier,
                score=result.score,
                is_testnet=result.is_testnet_only,
                estimated_cost_usd=result.estimated_gas_cost_usd,
                summary=result.summary,
                raw_content=sample_announcement
            )
            session.add(project)
            await session.flush()

            for task_data in result.tasks:
                task = ActionTask(
                    project_id=project.id,
                    action_type=task_data.action_type,
                    network=task_data.network,
                    is_autonomous=task_data.is_autonomous,
                    status=TaskStatus.APPROVED if task_data.is_autonomous else TaskStatus.PENDING,
                    payload=task_data.description
                )
                session.add(task)
            
            await session.commit()
            logger.success("Дані записано в drop_hunter.db!")

    except Exception as e:
        logger.error(f"Помилка виклику ШІ: {e}")
        logger.warning("Перевірте, чи прописано валідний GEMINI_API_KEY у файлі .env")

if __name__ == "__main__":
    asyncio.run(main())
