"""
Timing Middleware

Measures request execution time.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Measures request execution time.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        start = time.perf_counter()

        response = await call_next(
            request
        )

        elapsed = (
            time.perf_counter()
            - start
        ) * 1000

        response.headers[
            "X-Response-Time"
        ] = f"{elapsed:.2f} ms"

        return response