"""
Application Entry Point

Starts the AI Analytics Copilot API.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.exception_handlers import (
    register_exception_handlers,
)
from app.core.logging import (
    configure_logging,
)
from app.core.settings import settings
from app.middleware import (
    LoggingMiddleware,
    RequestIDMiddleware,
    TimingMiddleware,
)

logger = logging.getLogger(__name__)


# =====================================================
# Application Lifespan
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown.
    """

    configure_logging()

    logger.info("=" * 60)
    logger.info("Starting %s", settings.APP_NAME)
    logger.info("Version: %s", settings.APP_VERSION)
    logger.info("=" * 60)

    yield

    logger.info("=" * 60)
    logger.info("Stopping %s", settings.APP_NAME)
    logger.info("=" * 60)


# =====================================================
# FastAPI Application
# =====================================================

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# =====================================================
# Global Exception Handlers
# =====================================================

register_exception_handlers(app)


# =====================================================
# Middleware
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestIDMiddleware)

app.add_middleware(TimingMiddleware)

app.add_middleware(LoggingMiddleware)


# =====================================================
# Health Endpoints
# =====================================================

@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """
    Root endpoint.
    """

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health", tags=["Health"])
async def health() -> dict[str, str]:
    """
    Liveness probe.
    """

    return {
        "status": "healthy",
    }


@app.get("/ready", tags=["Health"])
async def readiness() -> dict[str, str]:
    """
    Readiness probe.
    """

    return {
        "status": "ready",
    }


# =====================================================
# Register API Routes
# =====================================================

app.include_router(api_router)


# =====================================================
# Public Exports
# =====================================================

__all__ = [
    "app",
]