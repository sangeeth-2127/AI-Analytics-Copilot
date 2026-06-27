"""
Visualization Schemas

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from enum import Enum

from pydantic import BaseModel, Field


class ChartType(str, Enum):
    """
    Supported chart types.
    """

    histogram = "histogram"
    boxplot = "boxplot"
    scatter = "scatter"
    correlation = "correlation"


class AvailableColumnsResponse(BaseModel):
    """
    Lists available columns by datatype.
    """

    numeric_columns: list[str] = Field(
        ...,
        description="Numeric columns."
    )

    categorical_columns: list[str] = Field(
        ...,
        description="Categorical columns."
    )

    datetime_columns: list[str] = Field(
        ...,
        description="Datetime columns."
    )

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }


class ChartResponse(BaseModel):
    """
    Generic visualization response.
    """

    chart_type: ChartType = Field(
        ...,
        description="Generated chart type."
    )

    x_column: str | None = Field(
        default=None,
        description="X-axis column."
    )

    y_column: str | None = Field(
        default=None,
        description="Y-axis column."
    )

    figure: str = Field(
        ...,
        description="Plotly JSON."
    )

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }