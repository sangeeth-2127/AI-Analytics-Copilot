"""
Dataset Management API

Provides endpoints for managing uploaded datasets.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from fastapi import APIRouter, HTTPException

from app.schemas.dataset_info import DatasetInfo
from app.services.dataset_manager import dataset_manager


router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"],
)


@router.get(
    "/",
    response_model=list[DatasetInfo],
    summary="List Uploaded Datasets",
    description="Returns metadata for all uploaded datasets.",
)
async def list_uploaded_datasets() -> list[DatasetInfo]:
    """
    Return metadata for all uploaded datasets.
    """

    return dataset_manager.list_datasets()


@router.get(
    "/{dataset_id}",
    response_model=DatasetInfo,
    summary="Get Dataset Information",
    description="Returns metadata for a specific dataset.",
)
async def get_dataset(dataset_id: str) -> DatasetInfo:
    """
    Retrieve dataset metadata.
    """

    try:
        return dataset_manager.get_dataset_info(dataset_id)

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )


@router.delete(
    "/{dataset_id}",
    summary="Delete Dataset",
    description="Deletes a stored dataset.",
)
async def delete_dataset(dataset_id: str):
    """
    Delete a stored dataset.
    """

    try:
        dataset_manager.delete_dataset(dataset_id)

        return {
            "message": "Dataset deleted successfully."
        }

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )