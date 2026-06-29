"""
Ollama Provider

Local LLM Provider using Ollama.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from ollama import Client

from app.agent.models import (
    LLMRequest,
    LLMResponse,
)

from app.agent.providers.base_provider import (
    BaseProvider,
)

from app.core.settings import (
    settings,
)


class OllamaProvider(BaseProvider):
    """
    Ollama implementation of the BaseProvider.
    """

    def __init__(self) -> None:

        super().__init__(
            name="Ollama",
            model_name=settings.OLLAMA_MODEL,
        )

        self._client = Client(
            host=settings.OLLAMA_BASE_URL,
        )

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        response = self._client.chat(
            model=self.model_name,
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
            options={
                "temperature": request.temperature,
                "num_predict": request.max_tokens,
            },
        )

        message = response["message"]["content"]

        prompt_tokens = response.get("prompt_eval_count", 0)
        completion_tokens = response.get("eval_count", 0)

        return LLMResponse(
            content=message,
            model_name=self.model_name,
            provider=self.name,
            tokens_used=prompt_tokens + completion_tokens,
            finish_reason="stop",
        )

    def health_check(self) -> bool:

        try:

            self._client.list()

            return True

        except Exception:

            return False