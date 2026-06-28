"""
Recommendation Rules

Contains rule-based recommendations for
machine learning and analytics.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.schemas.analysis import DatasetAnalysis


class RecommendationRules:
    """
    Rule engine for dataset recommendations.
    """

    @staticmethod
    def recommend_problem_type(
        analysis: DatasetAnalysis,
        target_column: str | None,
    ) -> str:
        """
        Recommend the ML problem type.
        """

        if target_column is None:
            return "Exploratory Data Analysis"

        statistics = analysis.statistics.statistics

        if target_column not in statistics:
            return "Exploratory Data Analysis"

        target = statistics[target_column]

        if target.dtype in (
            "int64",
            "float64",
        ):
            return "Regression"

        if target.unique_values <= 20:
            return "Classification"

        return "Clustering"

    @staticmethod
    def recommend_models(
        problem_type: str,
    ) -> list[str]:
        """
        Recommend ML algorithms.
        """

        recommendations = {

            "Regression": [

                "Linear Regression",

                "Random Forest Regressor",

                "XGBoost Regressor",

            ],

            "Classification": [

                "Logistic Regression",

                "Random Forest",

                "XGBoost",

                "LightGBM",

            ],

            "Clustering": [

                "K-Means",

                "DBSCAN",

                "Hierarchical Clustering",

            ],

            "Exploratory Data Analysis": [

                "Descriptive Statistics",

                "Correlation Analysis",

                "Visualization",

            ],

        }

        return recommendations.get(
            problem_type,
            [],
        )

    @staticmethod
    def recommend_preprocessing(
        analysis: DatasetAnalysis,
    ) -> list[str]:
        """
        Recommend preprocessing steps.
        """

        recommendations = []

        profile = analysis.profile

        if profile.missing_values > 0:

            recommendations.append(
                "Handle missing values."
            )

        if profile.duplicate_rows > 0:

            recommendations.append(
                "Remove duplicate rows."
            )

        recommendations.extend(

            [

                "Encode categorical variables.",

                "Scale numerical features.",

                "Split into train/test sets.",

            ]

        )

        return recommendations

    @staticmethod
    def recommend_metrics(
        problem_type: str,
    ) -> list[str]:
        """
        Recommend evaluation metrics.
        """

        metrics = {

            "Regression": [

                "MAE",

                "RMSE",

                "R² Score",

            ],

            "Classification": [

                "Accuracy",

                "Precision",

                "Recall",

                "F1 Score",

                "ROC-AUC",

            ],

            "Clustering": [

                "Silhouette Score",

                "Davies-Bouldin Index",

            ],

            "Exploratory Data Analysis": [

                "Summary Statistics",

            ],

        }

        return metrics.get(
            problem_type,
            [],
        )


recommendation_rules = RecommendationRules()