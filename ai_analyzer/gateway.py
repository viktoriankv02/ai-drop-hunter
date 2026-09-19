import re
import json
import httpx
import litellm
from loguru import logger
from core.config import settings

class AIGateway:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            litellm.gemini_api_key = settings.GEMINI_API_KEY
        self.ollama_url = "http://127.0.0.1:11434/api/chat"
        self.local_model = "qwen3:4b-instruct"

    async def _call_ollama(self, prompt: str, system_prompt: str, json_format: bool = False) -> str:
        """Пряме звернення до локального сервера Ollama на диску D"""
        logger.info(f"[Ollama-Local] Обробка локальною моделлю {self.local_model}...")
        payload = {
            "model": self.local_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_ctx": 4096
            }
        }
        if json_format:
            payload["format"] = "json"

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(self.ollama_url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("message", {}).get("content", "")
            else:
                raise RuntimeError(f"Ollama повернула статус {resp.status_code}: {resp.text}")

    async def complete(
        self, 
        prompt: str, 
        system_prompt: str = "", 
        model: str = None, 
        response_format: dict = None
    ) -> str:
        # 1. Спроба виконати через Gemini 3.6-flash
        try:
            kwargs = {
                "model": "gemini/gemini-3.6-flash",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "timeout": 20
            }
            if response_format:
                kwargs["response_format"] = response_format

            resp = await litellm.acompletion(**kwargs)
            content = resp.choices[0].message.content
            if content:
                return content
        except Exception as e:
            logger.warning(f"Хмарний Gemini недоступний ({e}). Перемикання на локальну {self.local_model}...")

        # 2. Безвідмовний резерв: локальна модель Qwen
        is_json = bool(response_format and response_format.get("type") == "json_object")
        return await self._call_ollama(prompt, system_prompt, json_format=is_json)

ai_gateway = AIGateway()
