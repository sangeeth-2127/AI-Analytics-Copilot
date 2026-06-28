"""
Base Provider

Defines the contract for all Large Language Model (LLM)
providers used by the AI Analytics Agent.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.agent.models import (
    LLMRequest,
    LLMResponse,
)


class BaseProvider(ABC):
    """
    Abstract base class for all LLM providers.

    Every provider must implement the generate()
    method.
    """

    def __init__(
        self,
        name: str,
        model_name: str,
    ) -> None:
        self._name = name
        self._model_name = model_name

    @property
    def name(self) -> str:
        """
        Provider name.
        """

        return self._name

    @property
    def model_name(self) -> str:
        """
        Underlying model name.
        """

        return self._model_name

    @abstractmethod
    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate a response from the language model.

        Args:
            request:
                LLM request.

        Returns:
            LLMResponse
        """
        raise NotImplementedError

    def health_check(self) -> bool:
        """
        Check whether the provider is available.

        Override this method if the provider
        supports connectivity checks.
        """

        return True

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"model='{self.model_name}')"
        )