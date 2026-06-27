"""
Insights Schemas

Pydantic models for generated insights.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from pydantic import BaseModel, Field


class Insight(BaseModel):

    type: str = Field(
        ...,
        description="Category of the insight."
    )

    message: str = Field(
        ...,
        description="Insight message."
    )

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }


class DatasetInsights(BaseModel):

    summary: str = Field(
        ...,
        description="Overall dataset summary."
    )

    insights: list[Insight] = Field(
        ...,
        description="Generated insights."
    )

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }