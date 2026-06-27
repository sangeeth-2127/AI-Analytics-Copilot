"""
Upload API

Handles dataset uploads.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from fastapi import APIRouter, File, UploadFile

from app.schemas.dataset import DatasetUploadResponse
from app.services.dataset_service import upload_dataset


router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post(
    "/",
    response_model=DatasetUploadResponse,
    summary="Upload Dataset",
    description="Upload a CSV dataset, store it, and return the dataset metadata along with its analysis.",
)
async def upload_csv(
    file: UploadFile = File(...)
) -> DatasetUploadResponse:
    """
    Upload a CSV dataset.

    Args:
        file (UploadFile):
            CSV file uploaded by the user.

    Returns:
        DatasetUploadResponse:
            Metadata of the uploaded dataset and its analysis.
    """

    return upload_dataset(file)