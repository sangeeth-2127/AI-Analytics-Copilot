"""
Dataset Profiling Module

Provides basic information about a dataset without modifying it.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

import pandas as pd


def profile_dataset(df):
    """
    Generate a summary profile of a dataset.
    """


    if df is None:
        raise ValueError("DataFrame cannot be None.")

    if df.empty:
        raise ValueError("The DataFrame is empty.")

    profile = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": df.columns.tolist(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_usage_bytes": int(df.memory_usage(deep=True).sum()),
    }

    return profile