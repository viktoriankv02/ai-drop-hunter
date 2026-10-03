import json
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from loguru import logger
from discovery.browser import fetch_page_with_browser

class CryptoRankScraper:
    def __init__(self):
        self.platform_name = "cryptorank"
        self.catalog_url = "https://cryptorank.io/drophunting"
        
        # Топові активні ретродропи та тестнети з розділу дропхантингу CryptoRank
        self.trending_seeds = [
            {"title": "Monad", "url": "https://cryptorank.io/drophunting/monad-activity110/"},
            {"title": "Berachain", "url": "https://cryptorank.io/drophunting/berachain-activity114/"},
            {"title": "Story Protocol", "url": "https://cryptorank.io/drophunting/story-protocol-activity402/"},
            {"title": "Movement Labs", "url": "https://cryptorank.io/drophunting/movement-activity415/"},
            {"title": "Babylon Chain", "url": "https://cryptorank.io/drophunting/babylon-activity290/"},
            {"title": "Sonic (Fantom)", "url": "https://cryptorank.io/drophunting/sonic-activity855/"},
            {"title": "Sahara AI", "url": "https://cryptorank.io/drophunting/sahara-ai-activity812/"},
            {"title": "Plume Network", "url": "https://cryptorank.io/drophunting/plume-activity654/"},
            {"title": "Abstract Chain", "url": "https://cryptorank.io/drophunting/abstract-chain-activity348/"},
            {"title": "Concrete", "url": "https://cryptorank.io/drophunting/concrete-activity1011/"},
            {"title": "Rift Finance", "url": "https://cryptorank.io/drophunting/rift-activity992/"},
            {"title": "ORO", "url": "https://cryptorank.io/drophunting/oro-activity1005/"},
            {"title": "Monday Trade", "url": "https://cryptorank.io/drophunting/monday-trade-activity1082/"},
            {"title": "aPriori", "url": "https://cryptorank.io/drophunting/apriori-activity316/"},
            {"title": "Open Airdrop", "url": "https://cryptorank.io/drophunting/open-activity602/"}
        ]

    async def parse_catalog(self, limit: int = 15) -> List[Dict[str, str]]:
        logger.info(f"[cryptorank] Сканування каталогу дропів...")
        page_data = await fetch_page_with_browser(self.catalog_url, scroll_down=True)
        
        results = []
        seen = set()

        # Збір із відрендереної сторінки
        html = page_data.get("html", "")
        if html:
            soup = BeautifulSoup(html, "lxml")
            for a in soup.find_all("a", href=True):
                href = a["href"].split("?")[0].split("#")[0]
                if "-activity" in href:
                    clean_url = href if href.startswith("http") else f"https://cryptorank.io{href}"
                    if not clean_url.endswith("/"):
                        clean_url += "/"
                    if clean_url not in seen:
                        seen.add(clean_url)
                        text = a.get_text(separator=" ", strip=True)
                        results.append({
                            "title": text if len(text) > 2 else clean_url.split("/")[-2],
                            "url": clean_url
                        })

        # Додавання проєктів зі списку seed-ів
        for item in self.trending_seeds:
            if item["url"] not in seen:
                seen.add(item["url"])
                results.append(item)

        logger.success(f"[cryptorank] Доступно проєктів для обробки: {len(results)}")
        return results[:limit]

    async def parse_project_page(self, project_url: str) -> Optional[Dict[str, Any]]:
        logger.info(f"[cryptorank] Завантаження сторінки: {project_url}")
        page_data = await fetch_page_with_browser(project_url, scroll_down=False)

        next_data = page_data.get("next_data")
        if next_data:
            try:
                page_props = next_data.get("props", {}).get("pageProps", {})
                activity = page_props.get("activity") or page_props.get("initialData", {})
                if activity:
                    return {
                        "raw_json": activity,
                        "url": project_url,
                        "source": "next_data"
                    }
            except Exception as e:
                logger.warning(f"Помилка розбору Next.js JSON: {e}")

        html = page_data.get("html", "")
        if not html:
            return None

        soup = BeautifulSoup(html, "lxml")
        main_content = soup.find("main") or soup.find("body") or soup
        for tag in main_content(["script", "style", "nav", "footer", "svg"]):
            tag.decompose()

        return {
            "raw_text": main_content.get_text(separator="\n", strip=True)[:8000],
            "url": project_url,
            "source": "html_dom"
        }
