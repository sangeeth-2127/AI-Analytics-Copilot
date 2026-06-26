"""
Health Check API

Provides endpoints to verify that the
AI Analytics Copilot backend is running.
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health_check():
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
        "message": "AI Analytics Copilot is running successfully."
    }