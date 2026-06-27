"""
Dataset Information Schemas

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from datetime import datetime

from pydantic import BaseModel, Field


class DatasetInfo(BaseModel):
    """
    Metadata describing a stored dataset.
    """

    dataset_id: str = Field(
        ...,
        description="Unique dataset identifier."
    )

    filename: str = Field(
        ...,
        description="Original uploaded filename."
    )

    rows: int = Field(
        ...,
        ge=0,
        description="Number of rows."
    )

    columns: int = Field(
        ...,
        ge=0,
        description="Number of columns."
    )

    uploaded_at: datetime = Field(
        ...,
        description="Upload timestamp."
    )

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }