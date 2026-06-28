"""
Recommendation Service

Coordinates recommendation generation.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.recommendation.recommendation_engine import (
    recommendation_engine,
)

from app.schemas.analysis import DatasetAnalysis


class RecommendationService:
    """
    Service responsible for generating
    machine learning recommendations.
    """

    @staticmethod
    def generate_recommendations(
        analysis: DatasetAnalysis,
        target_column: str | None = None,
    ) -> dict:
        """
        Generate recommendations for a dataset.

        Args:
            analysis:
                Dataset analysis.

            target_column:
                Optional target column.

        Returns:
            Recommendation dictionary.
        """

        return recommendation_engine.generate(
            analysis=analysis,
            target_column=target_column,
        )


recommendation_service = RecommendationService()