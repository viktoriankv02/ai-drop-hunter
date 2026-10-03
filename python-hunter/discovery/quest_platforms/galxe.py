import httpx
from typing import List, Dict, Any
from loguru import logger

class GalxeScraper:
    def __init__(self):
        self.platform_name = "galxe"
        self.base_url = "https://graphigo.prd.galaxy.eco/query"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Origin": "https://app.galxe.com",
            "Referer": "https://app.galxe.com/"
        }

    async def get_candidate_urls(self) -> List[Dict[str, str]]:
        logger.info(f"[{self.platform_name}] Запит актуальних трендових квестів...")
        graphql_query = """
        query ExploreCampaigns($input: ListCampaignInput!) {
          campaigns(input: $input) {
            list {
              id
              name
              info
              chain
            }
          }
        }
        """
        payload = {
            "operationName": "ExploreCampaigns",
            "variables": {"input": {"first": 15}},
            "query": graphql_query
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=20.0) as client:
            try:
                response = await client.post(self.base_url, json=payload)
                if response.status_code != 200:
                    return []
                data = response.json()
            except Exception as e:
                logger.error(f"[{self.platform_name}] Помилка з'єднання: {e}")
                return []

        campaigns = data.get("data", {}).get("campaigns", {}).get("list", [])
        results = []
        for item in campaigns:
            cid = item.get("id")
            name = item.get("name", "").strip()
            if cid and name:
                results.append({
                    "title": name,
                    "url": f"https://app.galxe.com/quest/{cid}",
                    "platform": self.platform_name,
                    "details": f"Platform: Galxe\nName: {name}\nChain: {item.get('chain', 'EVM')}\nDescription: {item.get('info', '')}"
                })
        return results

    async def fetch_details(self, item: Dict[str, str]) -> str:
        return item.get("details", item.get("title", ""))
