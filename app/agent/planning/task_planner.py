"""
Task Planner

Creates an execution plan for the AI Analytics Agent
based on the detected user intent.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.agent.models import (
    AgentIntent,
    AgentPlan,
    ExecutionGraph,
    ExecutionStep,
    ToolRequest,
    ToolType,
)


class TaskPlanner:
    """
    Converts an AgentIntent into an executable plan.
    """

    def create_plan(
        self,
        intent: AgentIntent,
        question: str,
    ) -> AgentPlan:
        """
        Create an execution plan.

        Args:
            intent:
                Detected user intent.

            question:
                Original user question.

        Returns:
            AgentPlan
        """

        graph = ExecutionGraph(
            steps=self._build_steps(
                intent=intent,
                question=question,
            )
        )

        return AgentPlan(
            intent=intent,
            execution_graph=graph,
            requires_llm=True,
        )

    # =====================================================
    # Private Helpers
    # =====================================================

    def _build_steps(
        self,
        intent: AgentIntent,
        question: str,
    ) -> list[ExecutionStep]:
        """
        Build execution steps for an intent.
        """

        if intent == AgentIntent.ANALYSIS:
            return self._analysis_steps()

        if intent == AgentIntent.VISUALIZATION:
            return self._visualization_steps(question)

        if intent == AgentIntent.RECOMMENDATION:
            return self._recommendation_steps()

        if intent == AgentIntent.REPORT:
            return self._report_steps()

        return self._general_steps()

    # =====================================================
    # Analysis
    # =====================================================

    def _analysis_steps(
        self,
    ) -> list[ExecutionStep]:

        return [
            ExecutionStep(
                step_number=1,
                description="Analyze the dataset.",
                tool_request=ToolRequest(
                    tool=ToolType.ANALYSIS,
                    action="analyze",
                ),
            )
        ]

    # =====================================================
    # Visualization
    # =====================================================

    def _visualization_steps(
        self,
        question: str,
    ) -> list[ExecutionStep]:

        action = self._detect_chart(question)

        return [
            ExecutionStep(
                step_number=1,
                description="Generate visualization.",
                tool_request=ToolRequest(
                    tool=ToolType.VISUALIZATION,
                    action=action,
                    parameters={
                        "question": question,
                    },
                ),
            )
        ]

    # =====================================================
    # Recommendation
    # =====================================================

    def _recommendation_steps(
        self,
    ) -> list[ExecutionStep]:

        return [
            ExecutionStep(
                step_number=1,
                description="Recommend an ML model.",
                tool_request=ToolRequest(
                    tool=ToolType.RECOMMENDATION,
                    action="recommend",
                ),
            )
        ]

    # =====================================================
    # Report
    # =====================================================

    def _report_steps(
        self,
    ) -> list[ExecutionStep]:

        return [
            ExecutionStep(
                step_number=1,
                description="Generate report.",
                tool_request=ToolRequest(
                    tool=ToolType.REPORT,
                    action="generate_report",
                ),
            )
        ]

    # =====================================================
    # General
    # =====================================================

    def _general_steps(
        self,
    ) -> list[ExecutionStep]:

        return []

    # =====================================================
    # Chart Detection
    # =====================================================

    @staticmethod
    def _detect_chart(
        question: str,
    ) -> str:
        """
        Detect requested chart type.
        """

        text = question.lower()

        if "scatter" in text:
            return "scatter"

        if "box" in text:
            return "boxplot"

        if "heatmap" in text:
            return "heatmap"

        if "correlation" in text:
            return "correlation"

        if "line" in text:
            return "line"

        if "bar" in text:
            return "bar"

        return "histogram"


task_planner = TaskPlanner()