"""
Analysis Schemas

Pydantic models for complete dataset analysis.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.insights import DatasetInsights
from app.schemas.profile import DatasetProfile
from app.schemas.statistics import DatasetStatistics


class DatasetAnalysis(BaseModel):
    """
    Complete dataset analysis.

    Combines profiling, statistics,
    and generated insights.
    """

    profile: DatasetProfile = Field(
        ...,
        description="Dataset profile.",
    )

    statistics: DatasetStatistics = Field(
        ...,
        description="Dataset statistics.",
    )

    insights: DatasetInsights = Field(
        ...,
        description="Generated insights.",
    )

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )