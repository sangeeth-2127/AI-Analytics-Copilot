"""
Chat API

Exposes the AI Analytics Copilot chat endpoint.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import logging

from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.services.chat_service import (
    chat_service,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
async def chat(
    request: ChatRequest,
) -> ChatResponse:
    """
    Chat with the AI Analytics Copilot.

    If no conversation_id is supplied,
    a new conversation is automatically created.
    """

    logger.info(
        "Received chat request."
    )

    try:

        response = chat_service.chat(
            request=request,
        )

        logger.info(
            "Chat request completed successfully."
        )

        return response

    except KeyError as exc:

        logger.exception(
            "KeyError occurred."
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except ValueError as exc:

        logger.exception(
            "ValueError occurred."
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception:

        # =================================================
        # DEBUG MODE
        # =================================================
        # Let the full traceback appear in the terminal.
        # Do NOT convert it into an HTTPException.
        # =================================================

        logger.exception(
            "Unexpected exception occurred."
        )

        raise