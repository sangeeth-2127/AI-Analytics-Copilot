"""
Analysis Service

Coordinates the complete analytics pipeline.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

import pandas as pd

from app.analytics.insights import generate_insights
from app.analytics.profiling import profile_dataset
from app.analytics.statistics import generate_statistics

from app.schemas.analysis import DatasetAnalysis
from app.schemas.profile import DatasetProfile
from app.schemas.statistics import DatasetStatistics
from app.schemas.insights import DatasetInsights


def analyze_dataset(df: pd.DataFrame) -> DatasetAnalysis:
    """
    Run the complete analytics pipeline.

    Args:
        df (pd.DataFrame):
            Input dataset.

    Returns:
        DatasetAnalysis:
            Complete analysis of the dataset.
    """

    if df is None:
        raise ValueError("DataFrame cannot be None.")

    if df.empty:
        raise ValueError("The DataFrame is empty.")

    # -----------------------------
    # Generate raw analytics
    # -----------------------------

    profile_data = profile_dataset(df)

    statistics_data = generate_statistics(df)

    insights_data = generate_insights(
        profile_data,
        statistics_data,
    )

    # -----------------------------
    # Convert to Domain Models
    # -----------------------------

    profile = DatasetProfile(
        **profile_data
    )

    statistics = DatasetStatistics(
        statistics=statistics_data
    )

    insights = DatasetInsights(
        **insights_data
    )

    # -----------------------------
    # Compose Final Analysis
    # -----------------------------

    analysis = DatasetAnalysis(
        profile=profile,
        statistics=statistics,
        insights=insights,
    )

    return analysis