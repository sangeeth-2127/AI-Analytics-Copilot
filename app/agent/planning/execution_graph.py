"""
Execution Graph

Utility class for traversing and validating
execution graphs.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.agent.models import (
    AgentPlan,
    ExecutionStep,
)


class ExecutionGraphManager:
    """
    Manages execution of an AgentPlan.
    """

    def __init__(
        self,
        plan: AgentPlan,
    ) -> None:
        self._plan = plan
        self._completed_steps: set[int] = set()

    @property
    def plan(self) -> AgentPlan:
        """
        Return the execution plan.
        """
        return self._plan

    def has_next(self) -> bool:
        """
        Check whether executable steps remain.
        """

        return self.next_step() is not None

    def next_step(
        self,
    ) -> ExecutionStep | None:
        """
        Return the next executable step.

        Returns:
            ExecutionStep or None
        """

        for step in self._plan.execution_graph.steps:

            if step.step_number in self._completed_steps:
                continue

            if self._dependencies_completed(step):
                return step

        return None

    def mark_completed(
        self,
        step_number: int,
    ) -> None:
        """
        Mark a step as completed.
        """

        self._completed_steps.add(step_number)

    def is_completed(
        self,
        step_number: int,
    ) -> bool:
        """
        Check whether a step has been completed.
        """

        return step_number in self._completed_steps

    def reset(
        self,
    ) -> None:
        """
        Reset execution state.
        """

        self._completed_steps.clear()

    def completed_steps(
        self,
    ) -> list[int]:
        """
        Return completed step numbers.
        """

        return sorted(self._completed_steps)

    def remaining_steps(
        self,
    ) -> list[ExecutionStep]:
        """
        Return remaining execution steps.
        """

        return [

            step

            for step in self._plan.execution_graph.steps

            if step.step_number
            not in self._completed_steps

        ]

    # ======================================================
    # Private Helpers
    # ======================================================

    def _dependencies_completed(
        self,
        step: ExecutionStep,
    ) -> bool:
        """
        Check whether all dependencies have
        already been completed.
        """

        return all(
            dependency in self._completed_steps
            for dependency in step.depends_on
        )

    def __len__(
        self,
    ) -> int:
        return len(self._plan.execution_graph.steps)

    def __repr__(
        self,
    ) -> str:
        return (
            f"{self.__class__.__name__}("
            f"steps={len(self)}, "
            f"completed={len(self._completed_steps)})"
        )