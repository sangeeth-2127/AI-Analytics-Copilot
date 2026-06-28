"""
Application Exceptions

Custom exceptions used throughout the
AI Analytics Copilot.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations


class AnalyticsCopilotError(Exception):
    """
    Base application exception.
    """

    pass


# =====================================================
# Dataset
# =====================================================

class DatasetNotFoundError(
    AnalyticsCopilotError,
):
    """
    Dataset could not be found.
    """

    pass


class DatasetValidationError(
    AnalyticsCopilotError,
):
    """
    Invalid dataset.
    """

    pass


# =====================================================
# AI Agent
# =====================================================

class AgentExecutionError(
    AnalyticsCopilotError,
):
    """
    Agent execution failed.
    """

    pass


class PlanningError(
    AnalyticsCopilotError,
):
    """
    Planner failed.
    """

    pass


# =====================================================
# Tools
# =====================================================

class ToolExecutionError(
    AnalyticsCopilotError,
):
    """
    Tool execution failed.
    """

    pass


class VisualizationError(
    ToolExecutionError,
):
    """
    Visualization generation failed.
    """

    pass


class RecommendationError(
    ToolExecutionError,
):
    """
    Recommendation generation failed.
    """

    pass


# =====================================================
# Provider
# =====================================================

class ProviderError(
    AnalyticsCopilotError,
):
    """
    LLM provider error.
    """

    pass