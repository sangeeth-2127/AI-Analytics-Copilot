"""
CSV Service

Provides functionality to load CSV files into Pandas DataFrames.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from pathlib import Path

import pandas as pd


def load_csv(file_path):
    """
    Load a CSV file and return a Pandas DataFrame.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError("Only CSV files are supported.")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("The CSV file is empty.")

    return df