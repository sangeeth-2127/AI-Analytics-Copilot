"""
Main Application

Entry point for the AI Analytics Copilot backend.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.visualization import router as visualization_router 
from app.api.datasets import router as datasets_router


app = FastAPI(
    title="AI Analytics Copilot",
    description="Production-ready AI-powered analytics backend built with FastAPI.",
    version="1.0.0",
)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.
    """

    return {
        "message": "Welcome to AI Analytics Copilot API 🚀",
        "docs": "/docs",
    }


# -------------------------
# Register API Routers
# -------------------------

app.include_router(health_router)
app.include_router(upload_router)
# Register API Routers
app.include_router(visualization_router)
app.include_router(datasets_router)