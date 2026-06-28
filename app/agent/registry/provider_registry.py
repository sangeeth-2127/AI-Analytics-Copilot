"""
Provider Registry

Registers LLM providers.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.agent.providers.base_provider import BaseProvider
from app.agent.providers.openai_provider import OpenAIProvider


class ProviderRegistry:
    """
    Registry responsible for building
    LLM providers.
    """

    def __init__(self) -> None:
        self._provider: BaseProvider | None = None

    def build(self) -> BaseProvider:
        """
        Return the configured provider.
        """

        if self._provider is None:
            self._provider = OpenAIProvider()

        return self._provider


provider_registry = ProviderRegistry()