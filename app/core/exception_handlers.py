"""
Global Exception Handlers

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import logging
import traceback

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AnalyticsCopilotError,
    DatasetNotFoundError,
    DatasetValidationError,
)

logger = logging.getLogger(__name__)


def register_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Register all application exception handlers.
    """

    @app.exception_handler(DatasetNotFoundError)
    async def dataset_not_found(
        request: Request,
        exc: DatasetNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "error": type(exc).__name__,
                "message": str(exc),
            },
        )

    @app.exception_handler(DatasetValidationError)
    async def dataset_validation(
        request: Request,
        exc: DatasetValidationError,
    ):
        return JSONResponse(
            status_code=400,
            content={
                "error": type(exc).__name__,
                "message": str(exc),
            },
        )

    @app.exception_handler(AnalyticsCopilotError)
    async def application_exception(
        request: Request,
        exc: AnalyticsCopilotError,
    ):
        logger.exception(exc)
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "error": type(exc).__name__,
                "message": str(exc),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception(
        request: Request,
        exc: Exception,
    ):
        logger.exception(exc)
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "error": type(exc).__name__,
                "message": str(exc),
            },
        )