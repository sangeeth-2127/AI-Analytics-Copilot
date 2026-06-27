"""
Analysis Schemas

Pydantic models for complete dataset analysis.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from pydantic import BaseModel, Field

from app.schemas.profile import DatasetProfile
from app.schemas.statistics import DatasetStatistics
from app.schemas.insights import DatasetInsights


class DatasetAnalysis(BaseModel):
    """
    Represents the complete analysis of a dataset.
    """

    profile: DatasetProfile = Field(
        ...,
        description="Structural profile of the dataset."
    )

    statistics: DatasetStatistics = Field(
        ...,
        description="Descriptive statistics for the dataset."
    )

    insights: DatasetInsights = Field(
        ...,
        description="Generated insights for the dataset."
    )

    model_config = {
        "extra": "forbid",
        "frozen": True,
        "json_schema_extra": {
            "example": {
                "profile": {
                    "rows": 54600,
                    "columns": 75,
                    "column_names": [
                        "player_name",
                        "age",
                        "club_name"
                    ],
                    "data_types": {
                        "player_name": "object",
                        "age": "int64",
                        "club_name": "object"
                    },
                    "missing_values": {
                        "player_name": 0,
                        "age": 0,
                        "club_name": 0
                    },
                    "duplicate_rows": 0,
                    "memory_usage_bytes": 70545323
                },
                "statistics": {
                    "statistics": {
                        "age": {
                            "count": 54600,
                            "mean": 24.31,
                            "std": 4.85,
                            "min": 16,
                            "max": 45,
                            "median": 24,
                            "sum": 1327626
                        }
                    }
                },
                "insights": {
                    "summary": "Dataset contains 54,600 rows and 75 columns.",
                    "insights": [
                        {
                            "type": "Statistics",
                            "message": "The mean value of 'age' is 24.31."
                        },
                        {
                            "type": "Duplicates",
                            "message": "No duplicate rows were found."
                        },
                        {
                            "type": "Missing Values",
                            "message": "No missing values were detected."
                        }
                    ]
                }
            }
        }
    }