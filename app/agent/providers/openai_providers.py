"""
OpenAI Provider

Production implementation of the OpenAI provider.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import logging

from openai import OpenAI

from app.agent.models import (
    LLMRequest,
    LLMResponse,
)
from app.agent.providers.base_provider import BaseProvider
from app.core.settings import settings

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseProvider):
    """
    OpenAI implementation of BaseProvider.
    """

    def __init__(self) -> None:
        super().__init__(
            name="OpenAI",
            model_name=settings.OPENAI_MODEL,
        )

        self._client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate a response using OpenAI.
        """

        logger.info(
            "Generating response using %s",
            self.model_name,
        )

        response = self._client.chat.completions.create(
            model=self.model_name,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": request.system_prompt,
                },
                {
                    "role": "user",
                    "content": request.user_prompt,
                },
            ],
        )

        return LLMResponse(
            content=response.choices[0].message.content or "",
            model_name=response.model,
            provider=self.name,
            tokens_used=(
                response.usage.total_tokens
                if response.usage
                else None
            ),
            finish_reason=response.choices[
                0
            ].finish_reason,
        )

    def health_check(self) -> bool:
        """
        Check whether OpenAI is reachable.
        """

        try:

            self._client.models.list()

            return True

        except Exception:

            logger.exception(
                "OpenAI health check failed."
            )

            return False


openai_provider = OpenAIProvider()