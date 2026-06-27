"""
CSV Service

Provides functionality to load CSV files into Pandas DataFrames.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from pathlib import Path
from io import BytesIO
from fastapi import UploadFile
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

def load_uploaded_csv(file: UploadFile) -> pd.DataFrame:
    """
    Load an uploaded CSV file into a pandas DataFrame.

    Args:
        file (UploadFile):
            CSV file uploaded through FastAPI.

    Returns:
        pd.DataFrame
    """

    if file is None:
        raise ValueError("No file was uploaded.")

    if not file.filename.endswith(".csv"):
        raise ValueError("Only CSV files are supported.")

    try:
        file.file.seek(0)

        dataframe = pd.read_csv(BytesIO(file.file.read()))

        if dataframe.empty:
            raise ValueError("The uploaded CSV is empty.")

        return dataframe

    except Exception as error:
        raise ValueError(
            f"Failed to load uploaded CSV: {error}"
        )