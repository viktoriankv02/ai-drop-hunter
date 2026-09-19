import asyncio
import re
import litellm
from loguru import logger
from core.config import settings

class AIGateway:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            litellm.gemini_api_key = settings.GEMINI_API_KEY
        if settings.ANTHROPIC_API_KEY:
            litellm.anthropic_api_key = settings.ANTHROPIC_API_KEY
        if settings.OPENAI_API_KEY:
            litellm.openai_api_key = settings.OPENAI_API_KEY
        if settings.DEEPSEEK_API_KEY:
            litellm.deepseek_api_key = settings.DEEPSEEK_API_KEY

    async def complete(
        self, 
        prompt: str, 
        system_prompt: str = "", 
        model: str = None, 
        response_format: dict = None,
        max_retries: int = 4
    ) -> str:
        selected_model = model or settings.DEFAULT_AI_MODEL
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": selected_model,
            "messages": messages
        }

        if settings.CUSTOM_AI_GATEWAY_URL:
            kwargs["api_base"] = settings.CUSTOM_AI_GATEWAY_URL
            if settings.CUSTOM_AI_GATEWAY_KEY:
                kwargs["api_key"] = settings.CUSTOM_AI_GATEWAY_KEY

        if response_format:
            kwargs["response_format"] = response_format

        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                response = await litellm.acompletion(**kwargs)
                content = response.choices[0].message.content
                if content:
                    return content
                raise ValueError("Отримано порожню відповідь від моделі.")
            except Exception as e:
                last_error = e
                err_text = str(e)

                if "429" in err_text or "RESOURCE_EXHAUSTED" in err_text:
                    retry_match = re.search(r"retry in (\d+)", err_text)
                    wait_seconds = int(retry_match.group(1)) + 2 if retry_match else 35
                    logger.warning(f"Ліміт запитів 429. Очікування {wait_seconds}с (спроба {attempt}/{max_retries})...")
                    await asyncio.sleep(wait_seconds)
                elif "503" in err_text or "high demand" in err_text.lower():
                    wait_time = attempt * 6
                    logger.warning(f"Сервер 503 (High Demand). Очікування {wait_time}с (спроба {attempt}/{max_retries})...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Помилка API ({selected_model}): {e}")
                    raise e

        raise RuntimeError(f"Не вдалося отримати відповідь після {max_retries} спроб: {last_error}")

ai_gateway = AIGateway()
