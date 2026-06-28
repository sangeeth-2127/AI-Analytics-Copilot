"""
Analysis Tool

Executes dataset analysis for the AI Analytics Agent.

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
from app.services.analysis_service import analyze_dataset


class AnalysisTool(BaseTool):
    """
    Tool responsible for dataset analysis.
    """

    def __init__(self) -> None:
        super().__init__(
            name="Analysis Tool",
            description="Performs complete dataset analysis.",
            version="1.0.0",
        )
    @property
    def tool_type(self) -> ToolType:
        return ToolType.ANALYSIS    

    # =====================================================
    # Validation
    # =====================================================

    def validate(
        self,
        request: ToolRequest,
    ) -> None:
        """
        Validate the incoming tool request.
        """

        if request.tool != ToolType.ANALYSIS:
            raise ValueError(
                "AnalysisTool received an invalid tool request."
            )

        if not self.supports(request.action):
            raise ValueError(
                f"Unsupported action '{request.action}' "
                f"for AnalysisTool."
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
        Execute dataset analysis.

        Uses the cached analysis if available,
        otherwise generates a new analysis.
        """

        start_time = time.perf_counter()

        # --------------------------------------------
        # Use cached analysis if available
        # --------------------------------------------

        if context.analysis is not None:

            analysis = context.analysis

            message = (
                "Using cached dataset analysis."
            )

        else:

            analysis = analyze_dataset(
                context.dataframe
            )

            message = (
                "Dataset analysis generated successfully."
            )

        execution_time = (
            time.perf_counter() - start_time
        )

        return ToolResult(
            tool=ToolType.ANALYSIS,
            success=True,
            message=message,
            payload=analysis.model_dump(),
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
        Return whether the action is supported.
        """

        return action.lower() in {
            "analyze",
            "analysis",
            "summary",
            "statistics",
            "profile",
            "insights",
        }