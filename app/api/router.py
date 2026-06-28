from fastapi import APIRouter

from app.api.chat import router as chat_router
from app.api.datasets import router as datasets_router
from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.visualization import router as visualization_router

api_router = APIRouter()

api_router.include_router(
    health_router,
    tags=["Health"],
)

api_router.include_router(
    upload_router,
    prefix="/upload",
    tags=["Upload"],
)

api_router.include_router(
    datasets_router,
    prefix="/datasets",
    tags=["Datasets"],
)

api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"],
)

api_router.include_router(
    visualization_router,
    prefix="/visualization",
    tags=["Visualization"],
)