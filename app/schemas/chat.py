"""
Chat Schemas

Defines request and response models for the
AI Analytics Copilot chat API.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


# =====================================================
# Chat Role
# =====================================================

class ChatRole(str, Enum):
    """
    Chat message role.
    """

    SYSTEM = "system"

    USER = "user"

    ASSISTANT = "assistant"


# =====================================================
# Chat Message
# =====================================================

class ChatMessage(BaseModel):
    """
    Represents a single message
    within a conversation.
    """

    role: ChatRole

    content: str = Field(
        ...,
        min_length=1,
        description="Message content.",
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Message creation time.",
    )

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )


# =====================================================
# Chat Request
# =====================================================

class ChatRequest(BaseModel):
    """
    Incoming chat request.

    If conversation_id is omitted,
    a new conversation will be created.
    """

    dataset_id: str = Field(
        ...,
        min_length=1,
        description="Dataset identifier.",
    )

    question: str = Field(
        ...,
        min_length=1,
        description="User question.",
    )

    conversation_id: str | None = Field(
        default=None,
        description=(
            "Existing conversation ID. "
            "Leave empty to create a new conversation."
        ),
    )

    model_config = ConfigDict(
        extra="forbid",
    )


# =====================================================
# Chat Response
# =====================================================

class ChatResponse(BaseModel):
    """
    Response returned to the frontend.
    """

    conversation_id: str = Field(
        ...,
        description="Conversation identifier.",
    )

    answer: str = Field(
        ...,
        description="Assistant response.",
    )

    execution_time: float = Field(
        ...,
        ge=0,
        description="Execution time in seconds.",
    )

    model_config = ConfigDict(
        extra="forbid",
    )