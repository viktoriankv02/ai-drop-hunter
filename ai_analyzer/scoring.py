import json
import re
from loguru import logger
from pydantic import BaseModel
from typing import List, Optional
from core.database import ProjectTier
from ai_analyzer.gateway import llm_gateway

class ExtractedTask(BaseModel):
    step_number: int = 1
    title: str = "Виконати активність"
    action_type: str = "other"
    network: str = "Off-Chain"
    is_autonomous: bool = False
    target_url: Optional[str] = None
    description: str = ""

class ProjectAnalysis(BaseModel):
    is_actionable_drop: bool = True
    project_name: str = "Crypto Project"
    tier: ProjectTier = ProjectTier.TIER_2
    score: int = 65
    raised_amount: str = "Не оголошено"
    backers: str = ""
    category: str = "DeFi"
    stage: str = "Testnet"
    status_reward: str = "Потенційно"
    is_testnet_only: bool = True
    estimated_gas_cost_usd: float = 0.0
    summary: str = ""
    guide_markdown: str = ""
    tasks: List[ExtractedTask] = []

def extract_fallback_name(source_url: str) -> str:
    slug = source_url.strip("/").split("/")[-1].replace("-activity", "").replace("-", " ")
    # Видаляємо цифри з кінця slug
    slug = re.sub(r'\d+$', '', slug).strip()
    return slug.title() or "Web3 Drop"

async def analyze_cryptorank_project(raw_text: str, source_url: str) -> ProjectAnalysis:
    default_name = extract_fallback_name(source_url)
    clean_text = re.sub(r'\s+', ' ', raw_text)[:900].strip()

    # Шукаємо суму зборів прямо в тексті регулярним виразом
    raised_match = re.search(r'\$(\d+(?:\.\d+)?\s*[MKmk])', clean_text)
    found_raised = raised_match.group(0).upper() if raised_match else "Не оголошено"

    prompt = f"""Витягни дані проєкту у форматі JSON без коментарів.
Текст: "{clean_text}"

Формат відповіді:
{{
  "is_actionable_drop": true,
  "project_name": "{default_name}",
  "tier": "Tier-2",
  "score": 70,
  "raised_amount": "{found_raised}",
  "backers": "Фонди",
  "category": "DeFi / L2",
  "stage": "Testnet",
  "summary": "Короткий опис",
  "tasks": [
    {{"step_number": 1, "title": "Перейти на платформу та підключити гаманець", "action_type": "checkin", "is_autonomous": true}}
  ]
}}"""

    response_text = await llm_gateway.complete(prompt=prompt, system_prompt="Answer only valid JSON.")

    try:
        clean_json = response_text.strip()
        if "```json" in clean_json:
            clean_json = clean_json.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_json:
            clean_json = clean_json.split("```")[1].split("```")[0].strip()

        data = json.loads(clean_json)
        if not data.get("project_name") or data.get("project_name") in ["Crypto Project", "Unknown"]:
            data["project_name"] = default_name
        data["is_actionable_drop"] = True
        return ProjectAnalysis(**data)
    except Exception as e:
        logger.warning(f"ШІ затримався ({e}). Використовуємо страхувальні дані: {default_name}")
        return ProjectAnalysis(
            is_actionable_drop=True,
            project_name=default_name,
            score=65,
            raised_amount=found_raised,
            summary=clean_text[:220],
            tasks=[
                ExtractedTask(
                    step_number=1,
                    title=f"Дослідити гайд активності {default_name}",
                    action_type="checkin",
                    is_autonomous=True,
                    target_url=source_url
                )
            ]
        )
