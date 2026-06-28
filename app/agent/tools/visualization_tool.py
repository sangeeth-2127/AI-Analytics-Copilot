"""
Visualization Tool

Generates interactive Plotly visualizations for
the AI Analytics Copilot.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import time

from app.agent.models import (
    ToolExecutionContext,
    ToolMetadata,
    ToolRequest,
    ToolResult,
    ToolType,
)
from app.agent.tools.base import BaseTool

from app.schemas.visualization import ChartType

from app.services.visualization_service import (
    visualization_service,
)


class VisualizationTool(BaseTool):
    """
    Tool responsible for generating visualizations.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Visualization Tool",
            description="Generates interactive Plotly charts.",
            version="1.0.0",
        )
    @property
    def tool_type(self) -> ToolType:
        return ToolType.VISUALIZATION    

    # =====================================================
    # Validation
    # =====================================================

    def validate(
        self,
        request: ToolRequest,
    ) -> None:
        """
        Validate the visualization request.
        """

        if request.tool != ToolType.VISUALIZATION:
            raise ValueError(
                "VisualizationTool received an invalid tool request."
            )

        if not self.supports(request.action):
            raise ValueError(
                f"Unsupported visualization action "
                f"'{request.action}'."
            )

    # =====================================================
    # Execution
    # =====================================================

    def execute(
        self,
        context: ToolExecutionContext,
        request: ToolRequest,
    ) -> ToolResult:
        """
        Generate a visualization.
        """

        start_time = time.perf_counter()

        params = request.parameters

        chart_type = params.get("chart_type")

        if chart_type is None:
            raise ValueError(
                "Missing required parameter 'chart_type'."
            )

        chart = visualization_service.generate_chart(
            df=context.dataframe,
            chart_type=ChartType(chart_type),
            x_column=params.get("x_column"),
            y_column=params.get("y_column"),
        )

        execution_time = (
            time.perf_counter() - start_time
        )

        return ToolResult(
            tool=ToolType.VISUALIZATION,
            success=True,
            message="Visualization generated successfully.",
            payload=chart.model_dump(),
            metadata=ToolMetadata(
                execution_time=execution_time,
            ),
        )

    # =====================================================
    # Supported Actions
    # =====================================================

    def supports(
        self,
        action: str,
    ) -> bool:
        """
        Return whether the visualization action
        is supported.
        """

        return action.lower() in {
            "scatter",
            "histogram",
            "boxplot",
            "correlation",
            
            
        }