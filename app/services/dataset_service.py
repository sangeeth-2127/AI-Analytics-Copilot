"""
Dataset Service

Coordinates dataset upload, storage,
and analysis.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from fastapi import UploadFile

from app.schemas.analysis import DatasetAnalysis
from app.schemas.dataset import DatasetUploadResponse
from app.schemas.dataset_info import DatasetInfo

from app.services.analysis_service import (
    analyze_dataset,
)
from app.services.csv_service import (
    load_uploaded_csv,
)
from app.services.dataset_manager import (
    dataset_manager,
)


def upload_dataset(
    file: UploadFile,
) -> DatasetUploadResponse:
    """
    Upload, store, and analyze a dataset.

    Args:
        file:
            Uploaded CSV file.

    Returns:
        DatasetUploadResponse
    """

    # -------------------------------------------------
    # Load CSV
    # -------------------------------------------------

    df = load_uploaded_csv(file)

    # -------------------------------------------------
    # Analyze dataset (only once)
    # -------------------------------------------------

    analysis: DatasetAnalysis = analyze_dataset(
        df
    )

    # -------------------------------------------------
    # Store dataframe + cached analysis
    # -------------------------------------------------

    dataset_info: DatasetInfo = (
        dataset_manager.save_dataset(
            filename=file.filename or "dataset.csv",
            df=df,
            analysis=analysis,
        )
    )

    # -------------------------------------------------
    # Build response
    # -------------------------------------------------

    return DatasetUploadResponse(
        dataset=dataset_info,
        analysis=analysis,
    )