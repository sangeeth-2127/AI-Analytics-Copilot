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

    numeric_columns: list[str]

    categorical_columns: list[str]

    datetime_columns: list[str]

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }


class ChartMetadata(BaseModel):
    """
    Metadata describing a chart.
    """

    title: str

    x_label: str | None = None

    y_label: str | None = None

    total_rows: int

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }


class ChartResponse(BaseModel):
    """
    Generic visualization response.
    """

    chart_type: ChartType

    x_column: str | None = None

    y_column: str | None = None

    metadata: ChartMetadata

    figure: str

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }