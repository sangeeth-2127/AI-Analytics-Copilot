"""
Recommendation Tool

Generates intelligent machine learning
recommendations for the AI Analytics Copilot.

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

from app.services.recommendation_service import (
    recommendation_service,
)

from app.services.analysis_service import (
    analyze_dataset,
)


class RecommendationTool(BaseTool):
    """
    Tool responsible for generating
    machine learning recommendations.
    """

    def __init__(self) -> None:

        super().__init__(
            name="Recommendation Tool",
            description=(
                "Generates machine learning "
                "recommendations."
            ),
            version="1.0.0",
        )
    @property
    def tool_type(self) -> ToolType:
        return ToolType.RECOMMENDATION    

    # =====================================================
    # Validation
    # =====================================================

    def validate(
        self,
        request: ToolRequest,
    ) -> None:
        """
        Validate recommendation request.
        """

        if request.tool != ToolType.RECOMMENDATION:

            raise ValueError(
                "RecommendationTool received "
                "an invalid tool request."
            )

        if not self.supports(
            request.action
        ):

            raise ValueError(
                f"Unsupported recommendation "
                f"action '{request.action}'."
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
        Generate recommendations.
        """

        start_time = time.perf_counter()

        # ----------------------------------------
        # Reuse analysis if available
        # ----------------------------------------

        if context.analysis is not None:

            analysis = context.analysis

        else:

            analysis = analyze_dataset(
                context.dataframe
            )

        target_column = (
            request.parameters.get(
                "target_column"
            )
        )

        recommendations = (
            recommendation_service.generate_recommendations(
                analysis=analysis,
                target_column=target_column,
            )
        )

        execution_time = (
            time.perf_counter()
            - start_time
        )

        return ToolResult(

            tool=ToolType.RECOMMENDATION,

            success=True,

            message=(
                "Recommendations generated "
                "successfully."
            ),

            payload=recommendations,

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
        Supported recommendation actions.
        """

        return action.lower() in {

            "recommend",

            "recommendation",

            "model",

            "ml",

            "machine learning",

            "algorithm",

            "classification",

            "regression",

            "clustering",

            "prediction",
        }