"""
Dataset Manager

Stores uploaded datasets in memory.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from datetime import datetime
from uuid import uuid4

import pandas as pd

from app.schemas.dataset_info import DatasetInfo


class DatasetManager:
    """
    Stores uploaded datasets in memory.
    """

    def __init__(self):
        self._datasets: dict[str, dict] = {}

    def save_dataset(
        self,
        filename: str,
        df: pd.DataFrame,
    ) -> DatasetInfo:
        """
        Store a dataset and return its metadata.
        """

        if df is None:
            raise ValueError("DataFrame cannot be None.")

        if df.empty:
            raise ValueError("The DataFrame is empty.")

        dataset_id = str(uuid4())

        info = DatasetInfo(
            dataset_id=dataset_id,
            filename=filename,
            rows=df.shape[0],
            columns=df.shape[1],
            uploaded_at=datetime.now(),
        )

        self._datasets[dataset_id] = {
            "info": info,
            "dataframe": df,
        }

        return info

    def get_dataset(self, dataset_id: str) -> pd.DataFrame:
        """
        Retrieve a DataFrame.
        """

        if dataset_id not in self._datasets:
            raise KeyError(f"Dataset '{dataset_id}' not found.")

        return self._datasets[dataset_id]["dataframe"]

    def get_dataset_info(
        self,
        dataset_id: str,
    ) -> DatasetInfo:
        """
        Retrieve dataset metadata.
        """

        if dataset_id not in self._datasets:
            raise KeyError(f"Dataset '{dataset_id}' not found.")

        return self._datasets[dataset_id]["info"]

    def list_datasets(
        self,
    ) -> list[DatasetInfo]:
        """
        Return metadata for all datasets.
        """

        return [
            dataset["info"]
            for dataset in self._datasets.values()
        ]

    def delete_dataset(
        self,
        dataset_id: str,
    ) -> None:
        """
        Delete a dataset.
        """

        if dataset_id not in self._datasets:
            raise KeyError(f"Dataset '{dataset_id}' not found.")

        del self._datasets[dataset_id]


dataset_manager = DatasetManager()