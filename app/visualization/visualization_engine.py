"""
Visualization Engine

Creates Plotly figures for the AI Analytics Copilot.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app.schemas.visualization import ChartType


class VisualizationEngine:
    """
    Generates Plotly figures for supported chart types.
    """

    @staticmethod
    def get_numeric_columns(
        df: pd.DataFrame,
    ) -> list[str]:
        return df.select_dtypes(
            include="number"
        ).columns.tolist()

    @staticmethod
    def get_categorical_columns(
        df: pd.DataFrame,
    ) -> list[str]:
        return df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

    @staticmethod
    def get_datetime_columns(
        df: pd.DataFrame,
    ) -> list[str]:
        return df.select_dtypes(
            include=["datetime64[ns]"]
        ).columns.tolist()

    @staticmethod
    def generate_chart(
        df: pd.DataFrame,
        chart_type: ChartType,
        x_column: str | None = None,
        y_column: str | None = None,
    ) -> go.Figure:
        """
        Generate a Plotly chart.
        """

        if df is None:
            raise ValueError("DataFrame cannot be None.")

        if df.empty:
            raise ValueError("DataFrame is empty.")

        match chart_type:

            case ChartType.histogram:

                if x_column is None:
                    raise ValueError(
                        "Histogram requires x_column."
                    )

                return px.histogram(
                    df,
                    x=x_column,
                    title=f"Distribution of {x_column}",
                )

            case ChartType.boxplot:

                if x_column is None:
                    raise ValueError(
                        "Boxplot requires x_column."
                    )

                return px.box(
                    df,
                    y=x_column,
                    title=f"Boxplot of {x_column}",
                )

            case ChartType.scatter:

                if x_column is None or y_column is None:
                    raise ValueError(
                        "Scatterplot requires x_column and y_column."
                    )

                return px.scatter(
                    df,
                    x=x_column,
                    y=y_column,
                    title=f"{x_column} vs {y_column}",
                )

            case ChartType.correlation:

                numeric_df = df.select_dtypes(
                    include="number"
                )

                if numeric_df.shape[1] < 2:
                    raise ValueError(
                        "At least two numeric columns are required."
                    )

                corr = numeric_df.corr(
                    numeric_only=True
                )

                return px.imshow(
                    corr,
                    text_auto=".2f",
                    aspect="auto",
                    color_continuous_scale="RdBu_r",
                    title="Correlation Heatmap",
                )

            case _:

                raise ValueError(
                    f"Unsupported chart type: {chart_type}"
                )


visualization_engine = VisualizationEngine()