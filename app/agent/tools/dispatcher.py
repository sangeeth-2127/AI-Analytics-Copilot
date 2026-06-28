"""
Tool Dispatcher

Responsible for registering and executing tools
inside the AI Analytics Agent.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.agent.models import (
    ToolExecutionContext,
    ToolRequest,
    ToolResult,
    ToolType,
)
from app.agent.tools.base import BaseTool


class ToolDispatcher:
    """
    Dispatches tool requests to the appropriate tool.
    """

    def __init__(self) -> None:
        self._tools: dict[ToolType, BaseTool] = {}

    # =====================================================
    # Registration
    # =====================================================

    def register(
        self,
        tool_type: ToolType,
        tool: BaseTool,
    ) -> None:
        """
        Register a tool.

        Args:
            tool_type:
                Type of tool.

            tool:
                Tool implementation.
        """

        if tool_type in self._tools:
            raise ValueError(
                f"Tool '{tool_type.value}' is already registered."
            )

        self._tools[tool_type] = tool

    # =====================================================
    # Lookup
    # =====================================================

    def get_tool(
        self,
        tool_type: ToolType,
    ) -> BaseTool:
        """
        Retrieve a registered tool.

        Args:
            tool_type:
                Requested tool type.

        Returns:
            BaseTool
        """

        try:
            return self._tools[tool_type]

        except KeyError as exc:
            raise ValueError(
                f"No tool registered for "
                f"'{tool_type.value}'."
            ) from exc

    # =====================================================
    # Execute
    # =====================================================

    def execute(
        self,
        context: ToolExecutionContext,
        request: ToolRequest,
    ) -> ToolResult:
        """
        Execute a tool request.

        Args:
            context:
                Runtime execution context.

            request:
                Tool execution request.

        Returns:
            ToolResult
        """

        tool = self.get_tool(
            request.tool
        )

        tool.validate(request)

        return tool.execute(
            context=context,
            request=request,
        )

    # =====================================================
    # Utilities
    # =====================================================

    def registered_tools(
        self,
    ) -> list[str]:
        """
        Return registered tool names.
        """

        return [
            tool.name
            for tool in self._tools.values()
        ]

    def is_registered(
        self,
        tool_type: ToolType,
    ) -> bool:
        """
        Check whether a tool has been registered.
        """

        return tool_type in self._tools

    def clear(self) -> None:
        """
        Remove all registered tools.
        """

        self._tools.clear()

    def __len__(self) -> int:
        """
        Number of registered tools.
        """

        return len(self._tools)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"registered_tools={len(self)})"
        )