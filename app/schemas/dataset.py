"""
Dataset Schemas

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from pydantic import BaseModel, Field

from app.schemas.analysis import DatasetAnalysis
from app.schemas.dataset_info import DatasetInfo


class DatasetUploadResponse(BaseModel):
    """
    Response returned after uploading a dataset.
    """

    dataset: DatasetInfo = Field(
        ...,
        description="Metadata of the uploaded dataset."
    )

    analysis: DatasetAnalysis = Field(
        ...,
        description="Analysis generated for the uploaded dataset."
    )

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }