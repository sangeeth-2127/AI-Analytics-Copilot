"""
Memory Service

High-level interface for managing AI
conversation memory.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.agent.memory.conversation import (
    Conversation,
)
from app.agent.memory.conversation_manager import (
    conversation_manager,
)
from app.schemas.chat import (
    ChatMessage,
    ChatRole,
)


class MemoryService:
    """
    Service layer for conversation memory.
    """

    # =====================================================
    # Conversation Lifecycle
    # =====================================================

    def create_conversation(
        self,
    ) -> Conversation:
        """
        Create a new conversation.
        """

        return conversation_manager.create()

    def get_conversation(
        self,
        conversation_id: str,
    ) -> Conversation:
        """
        Retrieve a conversation.
        """

        return conversation_manager.get(
            conversation_id
        )

    def delete_conversation(
        self,
        conversation_id: str,
    ) -> None:
        """
        Delete a conversation.
        """

        conversation_manager.delete(
            conversation_id
        )

    def clear_conversation(
        self,
        conversation_id: str,
    ) -> None:
        """
        Remove all messages.
        """

        conversation_manager.clear(
            conversation_id
        )

    # =====================================================
    # Messages
    # =====================================================

    def add_user_message(
        self,
        conversation_id: str,
        content: str,
    ) -> None:
        """
        Add a user message.
        """

        conversation_manager.append(
            conversation_id,
            ChatMessage(
                role=ChatRole.USER,
                content=content,
            ),
        )

    def add_assistant_message(
        self,
        conversation_id: str,
        content: str,
    ) -> None:
        """
        Add an assistant message.
        """

        conversation_manager.append(
            conversation_id,
            ChatMessage(
                role=ChatRole.ASSISTANT,
                content=content,
            ),
        )

    # =====================================================
    # Retrieval
    # =====================================================

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[ChatMessage]:
        """
        Retrieve conversation messages.
        """

        return self.get_conversation(
            conversation_id
        ).messages

    def list_conversations(
        self,
    ) -> list[Conversation]:
        """
        List all conversations.
        """

        return conversation_manager.list()


memory_service = MemoryService()