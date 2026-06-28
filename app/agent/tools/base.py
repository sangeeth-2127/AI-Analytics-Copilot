"""
Base Tool

Defines the contract for every tool inside the
AI Analytics Agent.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from app.agent.models import (
    ToolExecutionContext,
    ToolRequest,
    ToolResult,
    ToolType,
)


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
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def version(self) -> str:
        return self._version
    
    @property
    @abstractmethod
    def tool_type(self) -> ToolType:
        """
        Return the type of this tool.
        """
        raise NotImplementedError

    def validate(
        self,
        request: ToolRequest,
    ) -> None:
        """
        Validate the incoming request.

        Override if custom validation is required.
        """
        return

    @abstractmethod
    def execute(
        self,
        context: ToolExecutionContext,
        request: ToolRequest,
    ) -> ToolResult:
        """
        Execute the tool.

        Args:
            context:
                Runtime execution context.

            request:
                Tool request.

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
        """

        return True

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"version='{self.version}')"
        )