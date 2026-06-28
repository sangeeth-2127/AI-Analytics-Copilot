"""
Base Tool

Defines the contract for every tool inside the
AI Analytics Agent.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.agent.models import ToolRequest, ToolResult


class BaseTool(ABC):
    """
    Abstract base class for all AI Agent tools.

    Every tool must implement the execute() method.
    """

    def __init__(
        self,
        name: str,
        description: str,
        version: str = "1.0.0",
    ) -> None:
        self._name = name
        self._description = description
        self._version = version

    @property
    def name(self) -> str:
        """
        Tool name.
        """
        return self._name

    @property
    def description(self) -> str:
        """
        Tool description.
        """
        return self._description

    @property
    def version(self) -> str:
        """
        Tool version.
        """
        return self._version

    def validate(
        self,
        request: ToolRequest,
    ) -> None:
        """
        Validate the incoming tool request.

        Tools that require custom validation should
        override this method.
        """
        return

    @abstractmethod
    def execute(
        self,
        dataset_id: str,
        request: ToolRequest,
    ) -> ToolResult:
        """
        Execute the tool.

        Args:
            dataset_id:
                Dataset identifier.

            request:
                Tool execution request.

        Returns:
            ToolResult
        """
        raise NotImplementedError

    def supports(
        self,
        action: str,
    ) -> bool:
        """
        Check whether the tool supports an action.

        Override this method if the tool supports
        only specific actions.
        """
        return True

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"version='{self.version}')"
        )