from abc import ABC, abstractmethod
from typing import List, Dict, Any
from curl_cffi.requests import AsyncSession
from loguru import logger

class BaseScraper(ABC):
    def __init__(self, platform_name: str, base_url: str):
        self.platform_name = platform_name
        self.base_url = base_url

    async def fetch_page(self, url: str) -> str:
        # impersonate="chrome124" емулює TLS-відбиток реального Chrome
        async with AsyncSession(impersonate="chrome124", timeout=25.0) as session:
            try:
                headers = {
                    "Accept-Language": "en-US,en;q=0.9,uk;q=0.8",
                    "Referer": "https://cryptorank.io/",
                    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Windows"',
                }
                response = await session.get(url, headers=headers)
                if response.status_code == 200:
                    return response.text
                logger.error(f"[{self.platform_name}] Статус {response.status_code} для {url}")
                return ""
            except Exception as e:
                logger.error(f"[{self.platform_name}] Помилка з'єднання з {url}: {e}")
                return ""

    @abstractmethod
    async def parse_latest(self) -> List[Dict[str, Any]]:
        pass
