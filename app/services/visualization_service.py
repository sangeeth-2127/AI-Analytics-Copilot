"""
Visualization Service

Coordinates visualization generation.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import pandas as pd

from app.schemas.visualization import (
    AvailableColumnsResponse,
    ChartMetadata,
    ChartResponse,
    ChartType,
)

from app.visualization.visualization_engine import (
    visualization_engine,
)


class VisualizationService:
    """
    Service responsible for visualization generation.
    """

    @staticmethod
    def get_available_columns(
        df: pd.DataFrame,
    ) -> AvailableColumnsResponse:
        """
        Return available columns grouped by datatype.
        """

        return AvailableColumnsResponse(
            numeric_columns=visualization_engine.get_numeric_columns(df),
            categorical_columns=visualization_engine.get_categorical_columns(df),
            datetime_columns=visualization_engine.get_datetime_columns(df),
        )

    @staticmethod
    def generate_chart(
        df: pd.DataFrame,
        chart_type: ChartType,
        x_column: str | None = None,
        y_column: str | None = None,
    ) -> ChartResponse:
        """
        Generate a visualization.
        """

        figure = visualization_engine.generate_chart(
            df=df,
            chart_type=chart_type,
            x_column=x_column,
            y_column=y_column,
        )

        return ChartResponse(
         chart_type=chart_type,
         x_column=x_column,
         y_column=y_column,
         metadata=ChartMetadata(
         title=figure.layout.title.text or "",
         x_label=x_column,
         y_label=y_column,
         total_rows=len(df),
         ),
         figure=figure.to_json(),
         )


visualization_service = VisualizationService()