"""
Application Settings

Central configuration for the
AI Analytics Copilot.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from typing import Literal

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """
    Application configuration.
    """

    # =====================================================
    # Ollama
    # =====================================================

    OLLAMA_MODEL: str = "qwen2.5:7b"

    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"

    # =====================================================
    # Logging
    # =====================================================

    LOG_LEVEL: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    LOG_DIR: str = "logs"

    # =====================================================
    # FastAPI
    # =====================================================

    APP_NAME: str = "AI Analytics Copilot"

    APP_VERSION: str = "1.0.0"

    APP_DESCRIPTION: str = (
        "An AI-powered analytics platform capable of "
        "dataset analysis, visualization, machine learning "
        "recommendations, and conversational data exploration."
    )

    API_PREFIX: str = "/api/v1"

    # =====================================================
    # Environment
    # =====================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()