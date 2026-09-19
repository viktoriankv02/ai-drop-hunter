import os
import sys
import json
import asyncio
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from loguru import logger
from sqlalchemy import select

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.database import init_db, async_session_maker, DropProject, ActionTask, TaskStatus, ProjectTier
from discovery.browser import fetch_page_with_browser
from ai_analyzer.scoring import analyze_cryptorank_project

SOURCES_FILE = os.path.join(ROOT_DIR, "sources", "resources.json")

def load_sources():
    if not os.path.exists(SOURCES_FILE):
        return []
    try:
        with open(SOURCES_FILE, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Помилка читання resources.json: {e}")
        return []

def save_sources(sources_list):
    os.makedirs(os.path.dirname(SOURCES_FILE), exist_ok=True)
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources_list, f, ensure_ascii=False, indent=2)

def parse_post_datetime(time_tag) -> datetime:
    """Витягує точну дату та час публікації з HTML-тегу Telegram"""
    if not time_tag or not time_tag.has_attr("datetime"):
        return None
    raw_dt = time_tag["datetime"]
    try:
        # Формат Telegram: 2026-09-19T18:24:00+00:00
        return datetime.fromisoformat(raw_dt.replace("Z", "+00:00"))
    except Exception:
        return None

async def extract_items_from_source(resource: dict, days_back: int = 30) -> list:
    url = resource.get("url")
    r_type = resource.get("type", "website")
    name = resource.get("name", "Джерело")
    
    # Розрахунок часового порогу (місяць тому від поточного моменту)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
    
    target_url = url
    if "t.me/" in url and "/s/" not in url:
        channel = url.split("t.me/")[-1].strip("/")
        target_url = f"https://t.me/s/{channel}"

    logger.info(f"[{name}] Сканування за період від {cutoff_date.strftime('%d.%m.%Y')}: {target_url}")
    page_data = await fetch_page_with_browser(target_url, scroll_down=True)
    html = page_data.get("html", "")
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    collected = []
    seen_urls = set()

    # 1. Обробка Telegram-каналів з жорстким контролем дати публікації
    if r_type == "telegram" or "t.me/s/" in target_url:
        posts = soup.select("div.tgme_widget_message_wrap")
        
        # Переглядаємо пости від найновіших до старіших
        for post in reversed(posts):
            text_el = post.select_one("div.tgme_widget_message_text")
            link_el = post.select_one("a.tgme_widget_message_date")
            time_el = post.select_one("time[datetime]")
            
            post_url = link_el["href"] if link_el and link_el.has_attr("href") else target_url
            if not text_el:
                continue

            # Перевірка дати
            post_dt = parse_post_datetime(time_el)
            if post_dt and post_dt < cutoff_date:
                # Зупиняємо збір, оскільки дійшли до постів старіших за 30 днів
                logger.info(f"[{name}] Дійшли до старіших публікацій ({post_dt.strftime('%d.%m.%Y')}). Зупинка збору каналу.")
                break

            raw_text = text_el.get_text(separator="\n", strip=True)
            if len(raw_text) > 80:
                dt_str = post_dt.strftime("%d.%m.%Y") if post_dt else "Свіже"
                collected.append({
                    "title": f"[{dt_str}] " + raw_text[:50].replace("\n", " "),
                    "url": post_url,
                    "text": raw_text
                })

    # 2. Обробка агрегаторів (CryptoRank, Airdrops.io, Dropsearn)
    else:
        for a in soup.find_all("a", href=True):
            href = a["href"].split("?")[0].split("#")[0]
            is_project_link = (
                ("-activity" in href and "/drophunting/" in href) or
                ("airdrops.io/" in href and not any(x in href for x in ["/speculative/", "/category/", "/tag/", "/contact/"])) or
                ("dropsearn.com/airdrops/" in href and href.strip("/") != "https://dropsearn.com/airdrops")
            )
            if is_project_link:
                clean_url = href if href.startswith("http") else f"https://cryptorank.io{href}"
                clean_url = clean_url.rstrip("/") + "/"
                if clean_url not in seen_urls:
                    seen_urls.add(clean_url)
                    text = a.get_text(strip=True) or clean_url.split("/")[-2]
                    collected.append({
                        "title": text,
                        "url": clean_url,
                        "text": ""
                    })
            # Для сайтів беремо актуальні проєкти першої лінії
            if len(collected) >= 8:
                break

    return collected

async def process_item(item: dict, platform_name: str) -> bool:
    target_url = item["url"]

    async with async_session_maker() as session:
        query = select(DropProject).where(DropProject.source_url == target_url)
        existing = (await session.execute(query)).scalar_one_or_none()
        if existing and existing.tracking_status != "tracking":
            return False

    raw_content = item.get("text", "")
    if not raw_content:
        detail_data = await fetch_page_with_browser(target_url, scroll_down=False)
        html = detail_data.get("html", "")
        if html:
            dsoup = BeautifulSoup(html, "lxml")
            main = dsoup.find("main") or dsoup.find("body") or dsoup
            for tag in main(["script", "style", "nav", "footer"]):
                tag.decompose()
            raw_content = main.get_text(separator="\n", strip=True)[:6000]

    if len(raw_content) < 60:
        return False

    logger.info(f"ШІ розбирає дані: {item['title']}...")
    try:
        analysis = await analyze_cryptorank_project(raw_content, target_url)

        if analysis.score < 20 or analysis.tier == ProjectTier.SCAM:
            logger.warning(f"Відсіяно (бал {analysis.score} < 20 або Scam): {analysis.project_name}")
            return False

        async with async_session_maker() as session:
            query = select(DropProject).where(DropProject.source_url == target_url)
            current = (await session.execute(query)).scalar_one_or_none()

            if not current:
                project = DropProject(
                    title=analysis.project_name,
                    source_url=target_url,
                    source_platform=platform_name,
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
                    raw_content=raw_content[:1500],
                    tracking_status="new"
                )
                session.add(project)
                await session.flush()

                for t in analysis.tasks:
                    session.add(ActionTask(
                        project_id=project.id,
                        step_number=t.step_number,
                        title=t.title,
                        action_type=t.action_type,
                        network=t.network,
                        is_autonomous=t.is_autonomous,
                        target_url=t.target_url,
                        description=t.description,
                        status=TaskStatus.APPROVED if t.is_autonomous else TaskStatus.PENDING
                    ))

                await session.commit()
                logger.success(f"✓ Додано: {analysis.project_name} (Бал: {analysis.score}/100)")
                return True
            else:
                current.summary = analysis.summary
                current.guide_markdown = analysis.guide_markdown
                await session.commit()
                logger.success(f"✓ Оновлено: {current.title}")
                return True

    except Exception as e:
        logger.error(f"Помилка обробки {target_url}: {e}")
        return False

async def run_all_sources(days_back: int = 30):
    await init_db()
    sources = load_sources()
    active_sources = [s for s in sources if s.get("enabled", True)]
    logger.info(f"Запуск обходу. Активних джерел: {len(active_sources)} | Вікно: останні {days_back} днів")

    total_added = 0
    for s in active_sources:
        items = await extract_items_from_source(s, days_back=days_back)
        for it in items:
            added = await process_item(it, s.get("name"))
            if added:
                total_added += 1

    logger.success(f"Обхід завершено. Усього додано нових проєктів за місяць: {total_added}")

if __name__ == "__main__":
    asyncio.run(run_all_sources(days_back=30))
