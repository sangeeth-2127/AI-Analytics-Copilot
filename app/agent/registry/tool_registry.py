"""
Tool Registry

Registers all AI Agent tools.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.agent.tools.analysis_tool import (
    AnalysisTool,
)
from app.agent.tools.base import (
    BaseTool,
)
from app.agent.tools.dispatcher import (
    ToolDispatcher,
)
from app.agent.tools.recommendation_tool import (
    RecommendationTool,
)
from app.agent.tools.visualization_tool import (
    VisualizationTool,
)


class ToolRegistry:
    """
    Registry responsible for registering
    AI Agent tools.
    """

    def __init__(self) -> None:

        self._dispatcher = ToolDispatcher()

    # =====================================================
    # Registration
    # =====================================================

    def register(
        self,
        tool: BaseTool,
    ) -> None:
        """
        Register a tool.
        """

        self._dispatcher.register(
            tool.tool_type,
            tool,
        )

    def register_defaults(
        self,
    ) -> None:
        """
        Register built-in tools.
        """

        self.register(
            AnalysisTool()
        )

        self.register(
            VisualizationTool()
        )

        self.register(
            RecommendationTool()
        )

    # =====================================================
    # Builder
    # =====================================================

    def build(
        self,
    ) -> ToolDispatcher:
        """
        Build dispatcher.
        """

        if len(self._dispatcher) == 0:

            self.register_defaults()

        return self._dispatcher


tool_registry = ToolRegistry()