from abc import ABC, abstractmethod
from typing import List, Dict, Any
import httpx
from loguru import logger

class BaseScraper(ABC):
    def __init__(self, platform_name: str, base_url: str):
        self.platform_name = platform_name
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        }

    async def fetch_page(self, url: str) -> str:
        async with httpx.AsyncClient(headers=self.headers, timeout=20.0, follow_redirects=True) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.text
            except Exception as e:
                logger.error(f"[{self.platform_name}] Помилка завантаження {url}: {e}")
                return ""

    @abstractmethod
    async def parse_latest(self) -> List[Dict[str, Any]]:
        pass
