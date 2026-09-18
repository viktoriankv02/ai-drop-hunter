import json
from pydantic import BaseModel, Field
from typing import List
from ai_analyzer.gateway import ai_gateway
from core.database import ProjectTier

class TaskDefinition(BaseModel):
    action_type: str = Field(description="Тип: checkin, swap, bridge, deploy_contract, faucet, twitter_post, discord_join")
    network: str = Field(description="Мережа: sepolia, base, linea, monad_testnet, mainnet тощо")
    is_autonomous: bool = Field(description="Чи є дія безпечною для автономного виконання в Testnet")
    description: str = Field(description="Опис кроку")

class DropAnalysisResult(BaseModel):
    project_name: str
    tier: ProjectTier
    score: int = Field(description="Оцінка від 0 до 100")
    is_testnet_only: bool
    estimated_gas_cost_usd: float
    confirmed_reward: bool
    summary: str
    tasks: List[TaskDefinition]

SYSTEM_PROMPT = """Ти — аналітик Web3 дропів та квестів.
Оціни сирий текст активності та розбий на завдання.

Вимоги до класифікації:
- Tier-1: Топові інвестори (Paradigm, a16z, Dragonfly), підтверджені нагороди.
- Безпека: Testnet та безкоштовні квести мають найвищий пріоритет.
- Scam: Підозрілі посилання, сумнівні контракти.

Повертай ТІЛЬКИ чистий JSON:
{
  "project_name": "Назва",
  "tier": "Tier-1",
  "score": 85,
  "is_testnet_only": true,
  "estimated_gas_cost_usd": 0.0,
  "confirmed_reward": true,
  "summary": "Короткий висновок",
  "tasks": [
    {
      "action_type": "faucet",
      "network": "sepolia",
      "is_autonomous": true,
      "description": "Отримати тестові токени"
    }
  ]
}
"""

async def analyze_drop_announcement(raw_text: str, source_url: str) -> DropAnalysisResult:
    user_prompt = f"Джерело: {source_url}\n\nТекст анонсу:\n{raw_text}"
    response_text = await ai_gateway.complete(
        prompt=user_prompt,
        system_prompt=SYSTEM_PROMPT,
        response_format={"type": "json_object"}
    )
    data = json.loads(response_text)
    return DropAnalysisResult(**data)
