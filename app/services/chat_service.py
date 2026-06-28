"""
Chat Service

Coordinates conversational interactions with
the AI Analytics Copilot.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import logging
import time

from app.agent.memory import memory_service
from app.core.dependencies import get_agent
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.dataset_manager import dataset_manager

logger = logging.getLogger(__name__)


class ChatService:
    """
    Coordinates chat interactions between the
    API layer and the AI Agent.
    """

    def __init__(self) -> None:
        """
        Initialize the chat service.
        """

        self._agent = get_agent()

    # =====================================================
    # Public API
    # =====================================================

    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """
        Process a user chat request.

        Args:
            request:
                Incoming chat request.

        Returns:
            ChatResponse
        """

        logger.info(
            "Processing chat request."
        )

        start_time = time.perf_counter()

        # =====================================================
        # Conversation
        # =====================================================

        if (
            request.conversation_id is None
            or request.conversation_id.strip() == ""
        ):

            conversation = (
                memory_service.create_conversation()
            )

            logger.info(
                "Created new conversation: %s",
                conversation.conversation_id,
            )

        else:

            try:

                conversation = (
                    memory_service.get_conversation(
                        request.conversation_id
                    )
                )

                logger.info(
                    "Loaded conversation: %s",
                    conversation.conversation_id,
                )

            except KeyError:

                logger.warning(
                    "Conversation '%s' not found. Creating a new one.",
                    request.conversation_id,
                )

                conversation = (
                    memory_service.create_conversation()
                )

                logger.info(
                    "Created new conversation: %s",
                    conversation.conversation_id,
                )

        # =====================================================
        # Dataset
        # =====================================================

        dataframe = dataset_manager.get_dataset(
            request.dataset_id
        )

        analysis = dataset_manager.get_analysis(
            request.dataset_id
        )

        # =====================================================
        # Store User Message
        # =====================================================

        memory_service.add_user_message(
            conversation_id=conversation.conversation_id,
            content=request.question,
        )

        # =====================================================
        # Execute AI Agent
        # =====================================================

        agent_response = self._agent.run(
            dataset_id=request.dataset_id,
            dataframe=dataframe,
            analysis=analysis,
            question=request.question,
        )

        # =====================================================
        # Store Assistant Message
        # =====================================================

        memory_service.add_assistant_message(
            conversation_id=conversation.conversation_id,
            content=agent_response.answer,
        )

        # =====================================================
        # Build Response
        # =====================================================

        execution_time = (
            time.perf_counter() - start_time
        )

        logger.info(
            "Conversation completed in %.3f seconds.",
            execution_time,
        )

        return ChatResponse(
            conversation_id=conversation.conversation_id,
            answer=agent_response.answer,
            execution_time=execution_time,
        )


chat_service = ChatService()