import re
import json
from pydantic import BaseModel, Field
from typing import List, Optional
from loguru import logger
from ai_analyzer.gateway import ai_gateway
from core.database import ProjectTier

class TaskDefinition(BaseModel):
    step_number: int = Field(default=1)
    title: str = Field(default="Завдання")
    action_type: str = Field(default="other")
    network: str = Field(default="Off-Chain")
    is_autonomous: bool = Field(default=False)
    target_url: Optional[str] = Field(default=None)
    description: str = Field(default="")

class DropDetailedAnalysis(BaseModel):
    project_name: str = Field(default="Web3 Project")
    tier: ProjectTier = Field(default=ProjectTier.TIER_2)
    score: int = Field(default=70)
    category: str = Field(default="DeFi")
    stage: str = Field(default="Testnet")
    raised_amount: str = Field(default="Не оголошено")
    backers: str = Field(default="")
    status_reward: str = Field(default="Потенційно")
    is_testnet_only: bool = Field(default=True)
    estimated_gas_cost_usd: float = Field(default=0.0)
    summary: str = Field(default="")
    guide_markdown: str = Field(default="")
    tasks: List[TaskDefinition] = Field(default_factory=list)

SYSTEM_PROMPT = """Ти — Web3 аналітик ретродропів. Твоє завдання — проаналізувати текст про криптопроєкт та повернути валідний JSON за шаблоном:
{
  "project_name": "Назва",
  "tier": "Tier-2",
  "score": 75,
  "category": "Layer 1",
  "stage": "Testnet",
  "raised_amount": "$10M",
  "backers": "Фонди",
  "status_reward": "Потенційно",
  "is_testnet_only": true,
  "estimated_gas_cost_usd": 0.0,
  "summary": "Короткий огляд",
  "guide_markdown": "Покроковий план",
  "tasks": [
    {
      "step_number": 1,
      "title": "Підключення гаманця",
      "action_type": "profile",
      "network": "Testnet",
      "is_autonomous": false,
      "target_url": "",
      "description": "Перейти на платформу та підключити гаманець"
    }
  ]
}
tier має бути: Tier-1, Tier-2, Tier-3, Unverified або Scam.
Повертай виключно валідний JSON.
"""

def extract_json(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    if "```json" in cleaned:
        cleaned = re.sub(r"^```json\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    elif "```" in cleaned:
        cleaned = re.sub(r"^```\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    
    match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(1)

    return json.loads(cleaned)

async def analyze_cryptorank_project(raw_data: str, url: str) -> DropDetailedAnalysis:
    prompt = f"URL проєкту: {url}\n\nЗміст інформації:\n{raw_data[:4000]}"
    response_text = await ai_gateway.complete(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        response_format={"type": "json_object"}
    )
    
    try:
        data = extract_json(response_text)
    except Exception:
        data = {
            "project_name": url.split("/")[-2].replace("-", " ").title(),
            "tier": "Tier-2",
            "score": 65,
            "summary": raw_data[:300]
        }

    valid_tiers = [e.value for e in ProjectTier]
    if data.get("tier") not in valid_tiers:
        data["tier"] = ProjectTier.TIER_2.value

    return DropDetailedAnalysis(**data)
