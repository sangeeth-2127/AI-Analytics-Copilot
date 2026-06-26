"""
Statistics Module

Generates descriptive statistics for numeric columns.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

import pandas as pd


def generate_statistics(df):
    """
    Generate descriptive statistics for all numeric columns.
    """

    if df is None:
        raise ValueError("DataFrame cannot be None.")

    if df.empty:
        raise ValueError("The DataFrame is empty.")

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

    if not numeric_columns:
        return {}

    statistics = {}
    for column in numeric_columns:
        series = df[column]
        statistics[column] = {
            "count": int(series.count()),
            "mean": float(series.mean()),
            "std": float(series.std()),
            "min": float(series.min()),
            "max": float(series.max()),
            "median": float(series.median()),
            "sum": float(series.sum()),
            "variance": float(series.var()),
            "unique_values": int(series.nunique()),
            "missing_values": int(series.isnull().sum()),
        }

    return statistics