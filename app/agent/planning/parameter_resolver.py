"""
Parameter Resolver

Extracts tool parameters from the user's question.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import re

import pandas as pd

from app.agent.models import (
    AgentPlan,
    ToolType,
)


class ParameterResolver:
    """
    Resolves tool parameters using
    the user's question and dataset.
    """

    def resolve(
        self,
        plan: AgentPlan,
        dataframe: pd.DataFrame,
        question: str,
    ) -> AgentPlan:
        """
        Populate ToolRequest parameters.
        """

        columns = dataframe.columns.tolist()

        updated_steps = []

        for step in plan.execution_graph.steps:

            request = step.tool_request

            parameters = dict(request.parameters)

            match request.tool:

                case ToolType.VISUALIZATION:

                    parameters.update(
                        self._resolve_visualization(
                            question,
                            columns,
                        )
                    )

                case ToolType.ANALYSIS:

                    parameters.update(
                        self._resolve_analysis(
                            question,
                            columns,
                        )
                    )

                case ToolType.RECOMMENDATION:

                    parameters.update(
                        self._resolve_recommendation(
                            question,
                            columns,
                        )
                    )

            updated_steps.append(
                step.model_copy(
                    update={
                        "tool_request": request.model_copy(
                            update={
                                "parameters": parameters,
                            }
                        )
                    }
                )
            )

        return plan.model_copy(
            update={
                "execution_graph":
                plan.execution_graph.model_copy(
                    update={
                        "steps": updated_steps,
                    }
                )
            }
        )

    # =====================================================
    # Visualization
    # =====================================================

    def _resolve_visualization(
        self,
        question: str,
        columns: list[str],
    ) -> dict:

        question = question.lower()

        matched_columns = self._match_columns(
            question,
            columns,
        )

        # Scatter Plot
        if any(
            keyword in question
            for keyword in (
                "scatter",
                "relationship",
                "compare",
                "correlation",
            )
        ):

            if len(matched_columns) >= 2:

                return {
                    "chart_type": "scatter",
                    "x_column": matched_columns[0],
                    "y_column": matched_columns[1],
                }

        # Histogram
        if any(
            keyword in question
            for keyword in (
                "histogram",
                "distribution",
                "frequency",
            )
        ):

            if matched_columns:

                return {
                    "chart_type": "histogram",
                    "x_column": matched_columns[0],
                }

        # Box Plot
        if any(
            keyword in question
            for keyword in (
                "box",
                "boxplot",
            )
        ):

            if matched_columns:

                return {
                    "chart_type": "boxplot",
                    "x_column": matched_columns[0],
                }

        # Line Chart
        if any(
            keyword in question
            for keyword in (
                "line",
                "trend",
            )
        ):

            if len(matched_columns) >= 2:

                return {
                    "chart_type": "line",
                    "x_column": matched_columns[0],
                    "y_column": matched_columns[1],
                }

        # Bar Chart
        if any(
            keyword in question
            for keyword in (
                "bar",
                "count",
            )
        ):

            if matched_columns:

                return {
                    "chart_type": "bar",
                    "x_column": matched_columns[0],
                }

        # Correlation Heatmap

        if any(
            keyword in question
            for keyword in (
                "heatmap",
                "correlation matrix",
            )
        ):

            return {
                "chart_type": "correlation",
            }

        return {}

    # =====================================================
    # Analysis
    # =====================================================

    def _resolve_analysis(
        self,
        question: str,
        columns: list[str],
    ) -> dict:

        return {
            "columns": self._match_columns(
                question.lower(),
                columns,
            )
        }

    # =====================================================
    # Recommendation
    # =====================================================

    def _resolve_recommendation(
        self,
        question: str,
        columns: list[str],
    ) -> dict:

        matched = self._match_columns(
            question.lower(),
            columns,
        )

        if matched:

            return {
                "target_column": matched[-1]
            }

        return {}

    # =====================================================
    # Utilities
    # =====================================================

    @staticmethod
    def _match_columns(
        question: str,
        columns: list[str],
    ) -> list[str]:
        """
        Match dataset columns
        mentioned in the user question.
        """

        matches = []

        for column in columns:

            pattern = (
                r"\b"
                + re.escape(column.lower())
                + r"\b"
            )

            if re.search(
                pattern,
                question,
            ):

                matches.append(column)

        return matches


parameter_resolver = ParameterResolver()