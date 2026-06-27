"""
Visualization API

Provides visualization endpoints for stored datasets.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
)

from app.schemas.visualization import (
    AvailableColumnsResponse,
    ChartResponse,
    ChartType,
)

from app.services.dataset_manager import dataset_manager
from app.services.visualization_service import (
    visualization_service,
)

router = APIRouter(
    prefix="/visualizations",
    tags=["Visualizations"],
)


@router.get(
    "/columns/{dataset_id}",
    response_model=AvailableColumnsResponse,
    summary="Get Available Columns",
)
async def get_available_columns(
    dataset_id: str,
):
    """
    Return dataset columns grouped by datatype.
    """

    try:

        df = dataset_manager.get_dataset(dataset_id)

        return visualization_service.get_available_columns(df)

    except KeyError:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found.",
        )


@router.get(
    "/chart/{dataset_id}",
    response_model=ChartResponse,
    summary="Generate Chart",
)
async def generate_chart(
    dataset_id: str,
    chart_type: ChartType = Query(
        ...,
        description="Type of chart to generate.",
    ),
    x_column: str | None = Query(
        default=None,
        description="Primary column.",
    ),
    y_column: str | None = Query(
        default=None,
        description="Secondary column.",
    ),
):
    """
    Generate a visualization.
    """

    try:

        df = dataset_manager.get_dataset(dataset_id)

        return visualization_service.generate_chart(
            df=df,
            chart_type=chart_type,
            x_column=x_column,
            y_column=y_column,
        )

    except KeyError:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found.",
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )