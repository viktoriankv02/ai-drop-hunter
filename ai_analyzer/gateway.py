import asyncio
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
        max_retries: int = 3
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

        for attempt in range(1, max_retries + 1):
            try:
                response = await litellm.acompletion(**kwargs)
                return response.choices[0].message.content
            except Exception as e:
                err_text = str(e)
                if ("503" in err_text or "high demand" in err_text.lower() or "429" in err_text) and attempt < max_retries:
                    wait_time = attempt * 3
                    logger.warning(f"Сервер ШІ тимчасово зайнятий (спроба {attempt}/{max_retries}). Очікування {wait_time}с...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Критична помилка AI ({selected_model}): {e}")
                    raise e

ai_gateway = AIGateway()
