"""
Tool Dispatcher

Responsible for registering and executing tools
inside the AI Analytics Agent.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.agent.models import (
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

    # ======================================================
    # Registration
    # ======================================================

    def register(
        self,
        tool_type: ToolType,
        tool: BaseTool,
    ) -> None:
        """
        Register a tool.

        Raises:
            ValueError:
                If the tool is already registered.
        """

        if tool_type in self._tools:
            raise ValueError(
                f"{tool_type.value} tool already registered."
            )

        self._tools[tool_type] = tool

    # ======================================================
    # Lookup
    # ======================================================

    def get_tool(
        self,
        tool_type: ToolType,
    ) -> BaseTool:
        """
        Retrieve a registered tool.
        """

        if tool_type not in self._tools:
            raise ValueError(
                f"No tool registered for '{tool_type.value}'."
            )

        return self._tools[tool_type]

    # ======================================================
    # Execute
    # ======================================================

    def execute(
        self,
        dataset_id: str,
        request: ToolRequest,
    ) -> ToolResult:
        """
        Execute a tool request.
        """

        tool = self.get_tool(request.tool)

        tool.validate(request)

        return tool.execute(
            dataset_id=dataset_id,
            request=request,
        )

    # ======================================================
    # Utilities
    # ======================================================

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
        Check if a tool has been registered.
        """

        return tool_type in self._tools

    def __len__(self) -> int:
        return len(self._tools)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(registered_tools={len(self)})"
        )