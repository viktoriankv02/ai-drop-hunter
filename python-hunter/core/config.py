import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Drop Hunter Hub"
    DATABASE_URL: str = "sqlite+aiosqlite:///./drop_hunter.db"
    
    # Хмарні та локальні моделі
    DEFAULT_AI_MODEL: str = os.getenv("DEFAULT_AI_MODEL", "gemini/gemini-2.5-flash")
    FALLBACK_AI_MODEL: str = "gemini/gemini-2.0-flash"
    LOCAL_AI_MODEL: str = "ollama/qwen3:4b-instruct"
    OLLAMA_API_BASE: str = os.getenv("OLLAMA_API_BASE", "http://127.0.0.1:11434")
    
    # Пріоритет: чи використовувати локальну модель як основну (True/False)
    PREFER_LOCAL_LLM: bool = False
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
