from bs4 import BeautifulSoup
from typing import List, Dict, Any
from urllib.parse import urlparse
from loguru import logger
from discovery.base import BaseScraper

class IncryptedScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            platform_name="incrypted",
            base_url="https://incrypted.com/ua/airdrops/"
        )
        self.ignore_exact = {
            "ended", "popular", "upcoming", "category", "guide", "airdrops"
        }

    async def parse_latest(self) -> List[Dict[str, Any]]:
        logger.info(f"[{self.platform_name}] Сканування каталогу дропів...")
        html = await self.fetch_page(self.base_url)
        if not html:
            return []

        soup = BeautifulSoup(html, "lxml")
        results = []
        seen_urls = set()

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if "/ua/airdrops/" not in href or href == self.base_url:
                continue

            parsed = urlparse(href)
            path_parts = [p for p in parsed.path.strip("/").split("/") if p]

            if parsed.query or not path_parts:
                continue

            slug = path_parts[-1]

            # Відсіюємо всі рубрики: activity-*, page-*, службові посилання
            if (
                slug.startswith("activity-") 
                or slug.startswith("page") 
                or slug in self.ignore_exact 
                or len(path_parts) < 3
            ):
                continue

            clean_url = f"https://incrypted.com/ua/airdrops/{slug}/"
            if clean_url in seen_urls:
                continue
            seen_urls.add(clean_url)

            # Назва з тексту або атрибуту title
            title = a_tag.get_text(separator=" ", strip=True) or a_tag.get("title", slug)
            if len(title) < 3:
                title = slug.replace("-", " ").capitalize()

            results.append({
                "source_platform": self.platform_name,
                "title": title[:100],
                "url": clean_url,
                "slug": slug
            })

        logger.success(f"[{self.platform_name}] Знайдено цільових проєктів: {len(results)}")
        return results

    async def fetch_project_details(self, url: str) -> str:
        """Завантажує повний зміст гайду дропу для якісного ШІ-аналізу"""
        html = await self.fetch_page(url)
        if not html:
            return ""
        soup = BeautifulSoup(html, "lxml")
        content_block = soup.select_one("article, div.entry-content, main")
        if content_block:
            # Видаляємо скрипти та стилі
            for tag in content_block(["script", "style", "nav", "footer"]):
                tag.decompose()
            return content_block.get_text(separator="\n", strip=True)[:4000]
        return soup.get_text(separator="\n", strip=True)[:2000]
