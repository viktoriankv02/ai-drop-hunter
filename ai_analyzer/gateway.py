import os
import json
import httpx
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b-instruct")

async def _call_ollama(prompt: str, system_prompt: str = "") -> str:
    """Швидкий виклик без блокування рушія граматики"""
    logger.info(f"[Ollama-Local] Обробка {OLLAMA_MODEL}...")
    try:
        async with httpx.AsyncClient(timeout=45.0) as client:
            payload = {
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 350,
                    "top_p": 0.9
                }
            }
            res = await client.post(f"{OLLAMA_URL}/api/generate", json=payload)
            if res.status_code == 200:
                return res.json().get("response", "{}")
            else:
                logger.error(f"[Ollama] Помилка: {res.status_code}")
                return "{}"
    except Exception as e:
        logger.error(f"[Ollama] Збій запиту: {e}")
        return "{}"

async def complete(prompt: str, system_prompt: str = "") -> str:
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            import litellm
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            res = await litellm.acompletion(
                model="gemini/gemini-2.5-flash",
                messages=messages,
                api_key=gemini_key,
                timeout=20
            )
            return res.choices[0].message.content
        except Exception:
            pass

    return await _call_ollama(prompt, system_prompt)

class LLMGateway:
    async def complete(self, prompt: str, system_prompt: str = "") -> str:
        return await complete(prompt, system_prompt)

llm_gateway = LLMGateway()
