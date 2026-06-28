"""
Execution State

Tracks tool execution during an agent run.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.agent.models import ToolResult


class ExecutionState:
    """
    Stores tool execution results.
    """

    def __init__(self) -> None:
        self._tool_results: list[ToolResult] = []

    def add_result(
        self,
        result: ToolResult,
    ) -> None:
        self._tool_results.append(result)

    @property
    def tool_results(
        self,
    ) -> list[ToolResult]:
        return self._tool_results.copy()

    def clear(
        self,
    ) -> None:
        self._tool_results.clear()