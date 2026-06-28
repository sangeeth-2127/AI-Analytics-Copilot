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

        Args:
            plan:
                Execution plan.

            dataframe:
                Uploaded dataset.

            question:
                User question.

        Returns:
            Updated AgentPlan.
        """

        columns = dataframe.columns.tolist()

        updated_steps = []

        for step in plan.execution_graph.steps:

            request = step.tool_request

            parameters = dict(request.parameters)

            if request.tool == ToolType.VISUALIZATION:

                parameters.update(
                    self._resolve_visualization(
                        question,
                        columns,
                    )
                )

            elif request.tool == ToolType.ANALYSIS:

                parameters.update(
                    self._resolve_analysis(
                        question,
                        columns,
                    )
                )

            elif request.tool == ToolType.RECOMMENDATION:

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
                                "parameters": parameters
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
                        "steps": updated_steps
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

        question_lower = question.lower()

        matched_columns = self._match_columns(
            question_lower,
            columns,
        )

        if "scatter" in question_lower:

            if len(matched_columns) >= 2:

                return {
                    "x_column": matched_columns[0],
                    "y_column": matched_columns[1],
                }

        if "histogram" in question_lower:

            if matched_columns:

                return {
                    "column": matched_columns[0]
                }

        if "box" in question_lower:

            if matched_columns:

                return {
                    "column": matched_columns[0]
                }

        if "line" in question_lower:

            if len(matched_columns) >= 2:

                return {
                    "x_column": matched_columns[0],
                    "y_column": matched_columns[1],
                }

        if "bar" in question_lower:

            if matched_columns:

                return {
                    "column": matched_columns[0]
                }

        if "heatmap" in question_lower:

            return {}

        return {}

    # =====================================================
    # Analysis
    # =====================================================

    def _resolve_analysis(
        self,
        question: str,
        columns: list[str],
    ) -> dict:

        matched_columns = self._match_columns(
            question.lower(),
            columns,
        )

        return {
            "columns": matched_columns
        }

    # =====================================================
    # Recommendation
    # =====================================================

    def _resolve_recommendation(
        self,
        question: str,
        columns: list[str],
    ) -> dict:

        matched_columns = self._match_columns(
            question.lower(),
            columns,
        )

        if matched_columns:

            return {
                "target_column": matched_columns[-1]
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
        Match dataset columns mentioned
        in the user question.
        """

        matches = []

        for column in columns:

            pattern = (
                r"\b"
                + re.escape(column.lower())
                + r"\b"
            )

            if re.search(pattern, question):

                matches.append(column)

        return matches


parameter_resolver = ParameterResolver()