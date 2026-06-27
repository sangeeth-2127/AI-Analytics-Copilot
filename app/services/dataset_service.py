"""
Dataset Service

Coordinates dataset upload, storage,
and analysis.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from fastapi import UploadFile

from app.schemas.dataset import DatasetUploadResponse
from app.services.analysis_service import analyze_dataset
from app.services.csv_service import load_uploaded_csv
from app.services.dataset_manager import dataset_manager


def upload_dataset(file: UploadFile) -> DatasetUploadResponse:
    """
    Upload, store, and analyze a dataset.

    Args:
        file:
            Uploaded CSV file.

    Returns:
        DatasetUploadResponse
    """

    # Convert CSV to DataFrame
    df = load_uploaded_csv(file)

    # Save dataset and metadata
    dataset_info = dataset_manager.save_dataset(
        filename=file.filename,
        df=df,
    )

    # Analyze dataset
    analysis = analyze_dataset(df)

    # Return upload response
    return DatasetUploadResponse(
        dataset=dataset_info,
        analysis=analysis,
    )