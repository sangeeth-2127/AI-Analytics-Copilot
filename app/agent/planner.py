"""
Planner

Responsible for converting a user question into
an execution plan for the AI Analytics Copilot.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import re

from app.copilot.models import (
    AgentIntent,
    AgentPlan,
    PlanStep,
    ToolRequest,
    ToolType,
)


class Planner:
    """
    Creates execution plans from natural language questions.
    """

    def create_plan(
        self,
        question: str,
    ) -> AgentPlan:
        """
        Generate an execution plan.

        Args:
            question:
                User's natural language query.

        Returns:
            AgentPlan
        """

        question_lower = question.lower()

        # -------------------------------------------------
        # Visualization Intent
        # -------------------------------------------------

        if any(
            keyword in question_lower
            for keyword in [
                "plot",
                "graph",
                "chart",
                "visualize",
                "distribution",
                "scatter",
                "histogram",
                "boxplot",
                "correlation",
            ]
        ):

            return self._visualization_plan(question)

        # -------------------------------------------------
        # Recommendation Intent
        # -------------------------------------------------

        if any(
            keyword in question_lower
            for keyword in [
                "recommend",
                "model",
                "algorithm",
            ]
        ):

            return self._recommendation_plan()

        # -------------------------------------------------
        # Report Intent
        # -------------------------------------------------

        if any(
            keyword in question_lower
            for keyword in [
                "report",
                "summary pdf",
                "generate report",
            ]
        ):

            return self._report_plan()

        # -------------------------------------------------
        # Default → Analysis
        # -------------------------------------------------

        return self._analysis_plan()

    # ==========================================================
    # Analysis
    # ==========================================================

    def _analysis_plan(
        self,
    ) -> AgentPlan:

        return AgentPlan(
            intent=AgentIntent.ANALYSIS,
            requires_llm=True,
            steps=[
                PlanStep(
                    step_number=1,
                    description="Perform dataset analysis.",
                    tool_request=ToolRequest(
                        tool=ToolType.ANALYSIS,
                        operation="analysis",
                    ),
                )
            ],
        )

    # ==========================================================
    # Visualization
    # ==========================================================

    def _visualization_plan(
        self,
        question: str,
    ) -> AgentPlan:

        chart_type = "histogram"

        question_lower = question.lower()

        if "scatter" in question_lower:

            chart_type = "scatter"

        elif "box" in question_lower:

            chart_type = "boxplot"

        elif "correlation" in question_lower:

            chart_type = "correlation"

        return AgentPlan(
            intent=AgentIntent.VISUALIZATION,
            requires_llm=True,
            steps=[
                PlanStep(
                    step_number=1,
                    description="Generate visualization.",
                    tool_request=ToolRequest(
                        tool=ToolType.VISUALIZATION,
                        operation=chart_type,
                        parameters={
                            "question": question,
                        },
                    ),
                )
            ],
        )

    # ==========================================================
    # Recommendation
    # ==========================================================

    def _recommendation_plan(
        self,
    ) -> AgentPlan:

        return AgentPlan(
            intent=AgentIntent.RECOMMENDATION,
            requires_llm=True,
            steps=[
                PlanStep(
                    step_number=1,
                    description="Recommend ML model.",
                    tool_request=ToolRequest(
                        tool=ToolType.RECOMMENDATION,
                        operation="recommend",
                    ),
                )
            ],
        )

    # ==========================================================
    # Report
    # ==========================================================

    def _report_plan(
        self,
    ) -> AgentPlan:

        return AgentPlan(
            intent=AgentIntent.REPORT,
            requires_llm=True,
            steps=[
                PlanStep(
                    step_number=1,
                    description="Generate report.",
                    tool_request=ToolRequest(
                        tool=ToolType.REPORT,
                        operation="report",
                    ),
                )
            ],
        )


planner = Planner()