"""
Conversation Models

Represents a conversation between
the user and the AI Analytics Copilot.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.chat import ChatMessage


class Conversation(BaseModel):
    """
    Stores a conversation session.
    """

    conversation_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    messages: list[ChatMessage] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        extra="forbid",
        frozen=False,
    )

    def append(
        self,
        message: ChatMessage,
    ) -> None:
        """
        Append a message.
        """

        self.messages.append(message)

        self.updated_at = datetime.now(
            UTC
        )

    def clear(self) -> None:
        """
        Clear the conversation.
        """

        self.messages.clear()

        self.updated_at = datetime.now(
            UTC
        )