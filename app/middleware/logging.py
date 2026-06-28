"""
Logging Middleware

Logs every incoming request and outgoing response.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs request information.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        start = time.perf_counter()

        logger.info(
            "Incoming Request | %s %s",
            request.method,
            request.url.path,
        )

        response = await call_next(request)

        elapsed = (
            time.perf_counter()
            - start
        ) * 1000

        logger.info(
            "Completed | %s %s | %d | %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            elapsed,
        )

        return response