"""
Dataset Manager

Stores uploaded datasets and cached analysis in memory.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

import pandas as pd

from app.schemas.analysis import DatasetAnalysis
from app.schemas.dataset_info import DatasetInfo


class DatasetManager:
    """
    Stores uploaded datasets, metadata,
    and cached analysis in memory.
    """

    def __init__(self) -> None:
        self._datasets: dict[str, dict] = {}

    # =====================================================
    # Storage
    # =====================================================

    def save_dataset(
        self,
        filename: str,
        df: pd.DataFrame,
        analysis: DatasetAnalysis,
    ) -> DatasetInfo:
        """
        Store a dataset together with its
        cached analysis.

        Args:
            filename:
                Original filename.

            df:
                Uploaded dataframe.

            analysis:
                Cached dataset analysis.

        Returns:
            DatasetInfo
        """

        if df is None:
            raise ValueError(
                "DataFrame cannot be None."
            )

        if df.empty:
            raise ValueError(
                "The DataFrame is empty."
            )

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
            "analysis": analysis,
        }

        return info

    # =====================================================
    # Retrieval
    # =====================================================

    def get_dataset(
        self,
        dataset_id: str,
    ) -> pd.DataFrame:
        """
        Retrieve a dataframe.
        """

        self._ensure_exists(dataset_id)

        return self._datasets[
            dataset_id
        ]["dataframe"]

    def get_analysis(
        self,
        dataset_id: str,
    ) -> DatasetAnalysis:
        """
        Retrieve cached analysis.
        """

        self._ensure_exists(dataset_id)

        return self._datasets[
            dataset_id
        ]["analysis"]

    def get_dataset_info(
        self,
        dataset_id: str,
    ) -> DatasetInfo:
        """
        Retrieve dataset metadata.
        """

        self._ensure_exists(dataset_id)

        return self._datasets[
            dataset_id
        ]["info"]

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

    # =====================================================
    # Delete
    # =====================================================

    def delete_dataset(
        self,
        dataset_id: str,
    ) -> None:
        """
        Delete a dataset.
        """

        self._ensure_exists(dataset_id)

        del self._datasets[dataset_id]

    # =====================================================
    # Utilities
    # =====================================================

    def exists(
        self,
        dataset_id: str,
    ) -> bool:
        """
        Check whether a dataset exists.
        """

        return dataset_id in self._datasets

    def _ensure_exists(
        self,
        dataset_id: str,
    ) -> None:
        """
        Validate dataset existence.
        """

        if not self.exists(dataset_id):
            raise KeyError(
                f"Dataset '{dataset_id}' not found."
            )


dataset_manager = DatasetManager()