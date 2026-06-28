"""
Conversation Manager

Stores and manages AI conversations.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.agent.memory.conversation import (
    Conversation,
)
from app.schemas.chat import ChatMessage


class ConversationManager:
    """
    In-memory conversation storage.
    """

    def __init__(self) -> None:

        self._conversations: dict[
            str,
            Conversation,
        ] = {}

    # =====================================================
    # Create
    # =====================================================

    def create(
        self,
    ) -> Conversation:
        """
        Create a new conversation.
        """

        conversation = Conversation()

        self._conversations[
            conversation.conversation_id
        ] = conversation

        return conversation

    # =====================================================
    # Retrieve
    # =====================================================

    def get(
        self,
        conversation_id: str,
    ) -> Conversation:
        """
        Retrieve a conversation.
        """

        self._ensure_exists(
            conversation_id
        )

        return self._conversations[
            conversation_id
        ]

    # =====================================================
    # Append Message
    # =====================================================

    def append(
        self,
        conversation_id: str,
        message: ChatMessage,
    ) -> None:
        """
        Append a message to a conversation.
        """

        conversation = self.get(
            conversation_id
        )

        conversation.append(
            message
        )

    # =====================================================
    # Clear
    # =====================================================

    def clear(
        self,
        conversation_id: str,
    ) -> None:
        """
        Remove all messages from a conversation.
        """

        conversation = self.get(
            conversation_id
        )

        conversation.clear()

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        conversation_id: str,
    ) -> None:
        """
        Delete a conversation.
        """

        self._ensure_exists(
            conversation_id
        )

        del self._conversations[
            conversation_id
        ]

    # =====================================================
    # List
    # =====================================================

    def list(
        self,
    ) -> list[Conversation]:
        """
        Return all conversations.
        """

        return list(
            self._conversations.values()
        )

    # =====================================================
    # Exists
    # =====================================================

    def exists(
        self,
        conversation_id: str,
    ) -> bool:
        """
        Check whether a conversation exists.
        """

        return (
            conversation_id
            in self._conversations
        )

    # =====================================================
    # Utilities
    # =====================================================

    def _ensure_exists(
        self,
        conversation_id: str,
    ) -> None:
        """
        Validate conversation existence.
        """

        if not self.exists(
            conversation_id
        ):
            raise KeyError(
                f"Conversation '{conversation_id}' not found."
            )


conversation_manager = ConversationManager()