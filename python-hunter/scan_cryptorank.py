import asyncio
import json
import sys
from loguru import logger
from sqlalchemy import select
from core.database import init_db, async_session_maker, DropProject, ActionTask, TaskStatus
from discovery.aggregators.cryptorank import CryptoRankScraper
from ai_analyzer.scoring import analyze_cryptorank_project

async def run_scan(target_new_projects: int = 10):
    await init_db()
    scraper = CryptoRankScraper()
    
    # Запитуємо до 20 проєктів із каталогу
    catalog_items = await scraper.parse_catalog(limit=25)
    if not catalog_items:
        logger.error("Не вдалося завантажити каталог CryptoRank.")
        return

    added_count = 0
    async with async_session_maker() as session:
        for idx, item in enumerate(catalog_items):
            if added_count >= target_new_projects:
                break

            target_url = item["url"]
            
            # Перевірка на дублікат у базі
            query = select(DropProject).where(DropProject.source_url == target_url)
            existing = (await session.execute(query)).scalar_one_or_none()
            if existing:
                logger.info(f"[{idx+1}/{len(catalog_items)}] Вже в базі: {existing.title} (пропуск)")
                continue

            logger.info(f"[{idx+1}/{len(catalog_items)}] Завантаження гайду для: {item['title']}...")
            page_data = await scraper.parse_project_page(target_url)
            if not page_data:
                logger.warning(f"Не вдалося завантажити сторінку для {target_url}")
                continue

            content = json.dumps(page_data["raw_json"], ensure_ascii=False) if "raw_json" in page_data else page_data["raw_text"]

            logger.info(f"Аналіз ШІ ({item['title']})...")
            try:
                analysis = await analyze_cryptorank_project(content, target_url)
                
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
                added_count += 1
                logger.success(f"✓ Додано: {analysis.project_name} | {analysis.tier} | {analysis.score}/100 | Завдань: {len(analysis.tasks)} (Всього додано: {added_count}/{target_new_projects})")

                # Пауза 13с для дотримання ліміту 5 запитів/хв
                logger.info("Пауза 13с для дотримання квоти API...")
                await asyncio.sleep(13)

            except Exception as e:
                logger.error(f"Помилка обробки {target_url}: {e}")

    logger.success(f"Роботу завершено! Успішно додано нових проєктів: {added_count}")

if __name__ == "__main__":
    # За замовчуванням додаємо 8 нових проєктів
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    asyncio.run(run_scan(target_new_projects=count))
