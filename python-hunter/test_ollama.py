import asyncio
from ai_analyzer.gateway import ai_gateway
from loguru import logger

async def test_local():
    logger.info("Перевірка генерації через локальну qwen3:4b-instruct...")
    try:
        res = await ai_gateway.complete(
            prompt="Коротко в 1 речення: що таке тестнет у крипті?",
            model="ollama/qwen3:4b-instruct"
        )
        logger.success(f"Відповідь моделі:\n{res.strip()}")
    except Exception as e:
        logger.error(f"Помилка виклику Ollama: {e}")

if __name__ == "__main__":
    asyncio.run(test_local())
