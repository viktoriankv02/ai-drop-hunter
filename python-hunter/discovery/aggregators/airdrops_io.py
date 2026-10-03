from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from loguru import logger
from discovery.browser import fetch_page_with_browser

class AirdropsIoScraper:
    def __init__(self):
        self.platform_name = "airdrops_io"
        self.base_url = "https://airdrops.io/speculative/"

    async def get_candidate_urls(self) -> List[Dict[str, str]]:
        logger.info(f"[{self.platform_name}] Сканування каталогу: {self.base_url}")
        data = await fetch_page_with_browser(self.base_url, scroll_down=False)
        html = data.get("html", "")
        if not html:
            return []

        soup = BeautifulSoup(html, "lxml")
        results = []
        seen = set()

        for a_tag in soup.select("article a, div.airdrop-content a, h3 a"):
            href = a_tag.get("href", "")
            if not href or not href.startswith("https://airdrops.io/") or href == self.base_url:
                continue
            
            # Відсіюємо системні сторінки
            if any(x in href for x in ["/category/", "/speculative/", "/tag/", "/contact/", "/about/"]):
                continue

            clean_url = href.rstrip("/") + "/"
            if clean_url not in seen:
                seen.add(clean_url)
                title = a_tag.get_text(strip=True) or clean_url.split("/")[-2].replace("-", " ").title()
                results.append({
                    "title": title,
                    "url": clean_url,
                    "platform": self.platform_name
                })

        logger.success(f"[{self.platform_name}] Знайдено {len(results)} проєктів-кандидатів.")
        return results

    async def fetch_details(self, url: str) -> str:
        logger.info(f"[{self.platform_name}] Збір гайду: {url}")
        data = await fetch_page_with_browser(url, scroll_down=False)
        html = data.get("html", "")
        if not html:
            return ""

        soup = BeautifulSoup(html, "lxml")
        content_block = soup.select_one("div.entry-content, article") or soup
        for tag in content_block(["script", "style", "nav", "footer", "aside"]):
            tag.decompose()

        return content_block.get_text(separator="\n", strip=True)[:7000]
