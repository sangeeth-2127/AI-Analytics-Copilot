"""
Visualization Engine

Generates interactive visualizations for the
AI Analytics Copilot.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

import pandas as pd
import plotly.express as px


def generate_histograms(
    df: pd.DataFrame,
    columns: list[str] | None = None,
) -> dict:

    if df is None:
        raise ValueError("DataFrame cannot be None.")

    if df.empty:
        raise ValueError("The DataFrame is empty.")

    if columns is None:
        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()
    else:
        numeric_columns = columns

    if not numeric_columns:
        raise ValueError("No numeric columns found.")

    histograms = {}

    for column in numeric_columns:

        histogram_figure = px.histogram(
            data_frame=df,
            x=column,
            title=f"Distribution of {column.replace('_', ' ').title()}",
            labels={
                column: column.replace("_", " ").title(),
                "count": "Frequency",
            },
        )
        histograms[column] = {
            "figure": histogram_figure,
            "chart_type": "histogram",
            "column": column,
        }   

    return histograms



def generate_boxplots(
    df: pd.DataFrame,
    columns: list[str] | None = None,
) -> dict:
    if df is None:
        raise ValueError("DataFrame cannot be None.")

    if df.empty:
        raise ValueError("The DataFrame is empty.")

    if columns is None:
        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()
    else:
        numeric_columns = columns

    if not numeric_columns:
        raise ValueError("No numeric columns found.")

    boxplots = {}

    for column in numeric_columns:

        boxplot_figure = px.box(
            data_frame=df,
            y=column,
            title=f"Box Plot of {column.replace('_', ' ').title()}",
            labels={
                column: column.replace("_", " ").title()
            },
        )

        boxplots[column] = {
            "figure": boxplot_figure,
            "chart_type": "boxplot",
            "column": column,
        }

    return boxplots


from itertools import combinations


def generate_scatterplots(
    df: pd.DataFrame,
    columns: list[str] | None = None,
) -> dict:

    if df is None:
        raise ValueError("DataFrame cannot be None.")

    if df.empty:
        raise ValueError("The DataFrame is empty.")

    if columns is None:
        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()
    else:
        numeric_columns = columns

    if len(numeric_columns) < 2:
        raise ValueError(
            "At least two numeric columns are required."
        )

    scatterplots = {}

    for x_column, y_column in combinations(numeric_columns, 2):

        scatter_figure = px.scatter(
            data_frame=df,
            x=x_column,
            y=y_column,
            title=(
                f"{x_column.replace('_', ' ').title()} vs "
                f"{y_column.replace('_', ' ').title()}"
            ),
            labels={
                x_column: x_column.replace("_", " ").title(),
                y_column: y_column.replace("_", " ").title(),
            },
        )

        scatterplots[f"{x_column}_vs_{y_column}"] = {
            "figure": scatter_figure,
            "chart_type": "scatterplot",
            "x_column": x_column,
            "y_column": y_column,
        }

    return scatterplots


def generate_missing_value_chart(df: pd.DataFrame) -> dict:
    """
    Generate a bar chart showing missing values for each column.
    """

    if df is None:
        raise ValueError("DataFrame cannot be None.")

    if df.empty:
        raise ValueError("The DataFrame is empty.")

    missing_values = df.isnull().sum()

    missing_values = missing_values[missing_values > 0]

    if missing_values.empty:
        return {}

    missing_df = missing_values.reset_index()
    missing_df.columns = ["Column", "Missing Values"]

    missing_value_figure = px.bar(
        data_frame=missing_df,
        x="Column",
        y="Missing Values",
        title="Missing Values by Column",
        labels={
            "Column": "Column",
            "Missing Values": "Missing Values",
        },
    )

    return {
        "missing_values": {
            "figure": missing_value_figure,
            "chart_type": "missing_value_chart",
        }
    }



def generate_correlation_heatmap(df: pd.DataFrame) -> dict:
    """
    Generate a correlation heatmap for numeric columns.
    """

    if df is None:
        raise ValueError("DataFrame cannot be None.")

    if df.empty:
        raise ValueError("The DataFrame is empty.")

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        raise ValueError("No numeric columns found.")

    correlation_matrix = numeric_df.corr()

    heatmap_figure = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        title="Correlation Heatmap",
        aspect="auto",
        color_continuous_scale="RdBu_r",
    )

    return {
        "correlation_heatmap": {
            "figure": heatmap_figure,
            "chart_type": "correlation_heatmap",
        }
    }


def generate_visualizations(df: pd.DataFrame) -> dict:
    """
    Generate all visualizations for a dataset.
    """

    return {
        "histograms": generate_histograms(df),
        "boxplots": generate_boxplots(df),
        "scatterplots": generate_scatterplots(df),
        "missing_values": generate_missing_value_chart(df),
        "correlation_heatmap": generate_correlation_heatmap(df),
    }