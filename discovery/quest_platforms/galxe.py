import httpx
from typing import List, Dict, Any
from loguru import logger
from discovery.base import BaseScraper

class GalxeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            platform_name="galxe",
            base_url="https://graphigo.prd.galaxy.eco/query"
        )
        self.headers.update({
            "Content-Type": "application/json",
            "Origin": "https://app.galxe.com",
            "Referer": "https://app.galxe.com/"
        })

    async def parse_latest(self) -> List[Dict[str, Any]]:
        logger.info("[galxe] Запит актуальних квестів через GraphQL API...")

        # Додано обов'язковий суфікс "!" до типу ListCampaignInput!
        graphql_query = """
        query ExploreCampaigns($input: ListCampaignInput!) {
          campaigns(input: $input) {
            list {
              id
              name
              info
              chain
              status
            }
          }
        }
        """

        payload = {
            "operationName": "ExploreCampaigns",
            "variables": {
                "input": {
                    "first": 5
                }
            },
            "query": graphql_query
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=20.0) as client:
            try:
                response = await client.post(self.base_url, json=payload)
                if response.status_code != 200:
                    logger.error(f"[galxe] Код відповіді {response.status_code}. Деталі: {response.text}")
                    return []
                data = response.json()
            except Exception as e:
                logger.error(f"[galxe] Помилка мережевого з'єднання: {e}")
                return []

        if "errors" in data:
            logger.error(f"[galxe] GraphQL помилка: {data['errors']}")
            return []

        campaigns = data.get("data", {}).get("campaigns", {}).get("list", [])
        results = []

        for item in campaigns:
            campaign_id = item.get("id")
            name = item.get("name", "").strip()
            chain = item.get("chain", "EVM")
            raw_info = item.get("info", "") or f"Galxe Quest: {name}"

            target_url = f"https://app.galxe.com/quest/{campaign_id}"

            results.append({
                "source_platform": self.platform_name,
                "title": name,
                "url": target_url,
                "chain": chain,
                "raw_text": f"Campaign: {name}\nPlatform: Galxe\nChain: {chain}\nDetails: {raw_info[:500]}"
            })

        logger.success(f"[galxe] Успішно завантажено {len(results)} квестів.")
        return results
