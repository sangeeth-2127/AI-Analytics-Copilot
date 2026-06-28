"""
Recommendation Engine

Generates intelligent recommendations based on
dataset analysis.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.recommendation.recommendation_rules import (
    recommendation_rules,
)

from app.schemas.analysis import DatasetAnalysis


class RecommendationEngine:
    """
    Recommendation engine responsible for
    generating ML and analytics recommendations.
    """

    def generate(
        self,
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

        problem_type = (
            recommendation_rules.recommend_problem_type(
                analysis,
                target_column,
            )
        )

        recommended_models = (
            recommendation_rules.recommend_models(
                problem_type,
            )
        )

        preprocessing = (
            recommendation_rules.recommend_preprocessing(
                analysis,
            )
        )

        evaluation_metrics = (
            recommendation_rules.recommend_metrics(
                problem_type,
            )
        )

        next_steps = self._generate_next_steps(
            problem_type,
        )

        return {
            "problem_type": problem_type,
            "recommended_models": recommended_models,
            "preprocessing": preprocessing,
            "evaluation_metrics": evaluation_metrics,
            "next_steps": next_steps,
        }

    # =====================================================
    # Internal Helpers
    # =====================================================

    @staticmethod
    def _generate_next_steps(
        problem_type: str,
    ) -> list[str]:
        """
        Suggest the next steps for the user.
        """

        common_steps = [
            "Understand the dataset.",
            "Perform data cleaning.",
            "Visualize important features.",
        ]

        mapping = {

            "Regression": [
                "Train multiple regression models.",
                "Tune hyperparameters.",
                "Compare regression metrics.",
            ],

            "Classification": [
                "Balance target classes if needed.",
                "Train multiple classifiers.",
                "Evaluate classification metrics.",
            ],

            "Clustering": [
                "Choose an appropriate number of clusters.",
                "Compare clustering algorithms.",
                "Evaluate clustering quality.",
            ],

            "Exploratory Data Analysis": [
                "Explore feature relationships.",
                "Identify important variables.",
                "Prepare the dataset for modeling.",
            ],

        }

        return common_steps + mapping.get(
            problem_type,
            [],
        )


recommendation_engine = RecommendationEngine()