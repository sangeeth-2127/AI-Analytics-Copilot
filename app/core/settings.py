"""
Application Settings

Centralized configuration for the AI Analytics Copilot.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.
    """

    # ======================================================
    # OpenAI
    # ======================================================

    OPENAI_API_KEY: str = ""

    OPENAI_MODEL: str = "gpt-4.1-mini"

    # ======================================================
    # Gemini
    # ======================================================

    GEMINI_API_KEY: str = ""

    GEMINI_MODEL: str = "gemini-2.5-flash"

    # ======================================================
    # Ollama
    # ======================================================

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    OLLAMA_MODEL: str = "llama3.1"

    # ======================================================
    # Agent
    # ======================================================

    DEFAULT_PROVIDER: str = "gemini"

    MAX_TOKENS: int = 1200

    TEMPERATURE: float = 0.2

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.
    """
    return Settings()


settings = get_settings()