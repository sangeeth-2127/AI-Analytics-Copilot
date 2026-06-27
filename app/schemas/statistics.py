"""
Statistics Schemas

Pydantic models for dataset statistics.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from pydantic import BaseModel, Field


class DatasetStatistics(BaseModel):

    statistics: dict[str, dict[str, float | int]] = Field(
        ...,
        description="Statistics for all numeric columns."
    )

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }