"""
Intent Detector

Identifies the user's intent from a natural language query.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.agent.models import AgentIntent


class IntentDetector:
    """
    Detects the high-level intent of a user query.
    """

    _INTENT_KEYWORDS: dict[AgentIntent, set[str]] = {
        AgentIntent.VISUALIZATION: {
            "plot",
            "graph",
            "chart",
            "visualize",
            "histogram",
            "scatter",
            "boxplot",
            "heatmap",
            "distribution",
            "trend",
            "correlation",
        },
        AgentIntent.ANALYSIS: {
            "analyze",
            "analysis",
            "summary",
            "describe",
            "statistics",
            "profile",
            "insights",
            "overview",
            "eda",
        },
        AgentIntent.RECOMMENDATION: {
            "recommend",
            "suggest",
            "prediction",
            "predict",
            "model",
            "algorithm",
            "best",
        },
        AgentIntent.REPORT: {
            "report",
            "pdf",
            "document",
            "export",
            "download",
            "presentation",
        },
    }

    def detect(
        self,
        question: str,
    ) -> AgentIntent:
        """
        Detect the user's intent.

        Args:
            question:
                User's natural language query.

        Returns:
            AgentIntent
        """

        normalized_question = question.lower().strip()

        if not normalized_question:
            return AgentIntent.GENERAL

        for intent, keywords in self._INTENT_KEYWORDS.items():
            if any(
                keyword in normalized_question
                for keyword in keywords
            ):
                return intent

        return AgentIntent.GENERAL


intent_detector = IntentDetector()