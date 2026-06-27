"""
Profile Schemas

Pydantic models for dataset profiling.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from pydantic import BaseModel, Field


class DatasetProfile(BaseModel):
    rows: int = Field(..., ge=0)
    columns: int = Field(..., ge=0)

    column_names: list[str]

    data_types: dict[str, str]

    missing_values: dict[str, int]

    duplicate_rows: int = Field(..., ge=0)

    memory_usage_bytes: int = Field(..., ge=0)

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }