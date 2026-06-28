"""
Agent Orchestrator

Coordinates the complete execution flow of the
AI Analytics Copilot.

Responsibilities:
- Detect user intent
- Create execution plan
- Resolve tool parameters
- Execute tools
- Build execution context
- Compose LLM prompt
- Generate final response

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import logging

import pandas as pd

from app.agent.models import (
    AgentResponse,
    ToolMetadata,
    ToolResult,
)
from app.agent.planning.execution_graph import (
    ExecutionGraphManager,
)
from app.agent.planning.intent_detector import (
    IntentDetector,
)
from app.agent.planning.parameter_resolver import (
    ParameterResolver,
)
from app.agent.planning.task_planner import (
    TaskPlanner,
)
from app.agent.prompts.composer import (
    PromptComposer,
)
from app.agent.providers.base_provider import (
    BaseProvider,
)
from app.agent.tools.dispatcher import (
    ToolDispatcher,
)

from app.schemas.analysis import DatasetAnalysis


logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Coordinates the complete AI Agent workflow.

    The orchestrator contains NO business logic.

    It simply coordinates the various
    components of the AI Agent.
    """

    def __init__(
        self,
        intent_detector: IntentDetector,
        planner: TaskPlanner,
        parameter_resolver: ParameterResolver,
        dispatcher: ToolDispatcher,
        context_manager: ContextManager,
        prompt_composer: PromptComposer,
        provider: BaseProvider,
    ) -> None:
        """
        Initialize the AI Agent.

        Args:
            intent_detector:
                Detects user intent.

            planner:
                Creates execution plans.

            parameter_resolver:
                Resolves tool parameters.

            dispatcher:
                Executes tools.

            context_manager:
                Builds execution context.

            prompt_composer:
                Builds prompts.

            provider:
                LLM provider.
        """

        self._intent_detector = intent_detector

        self._planner = planner

        self._parameter_resolver = parameter_resolver

        self._dispatcher = dispatcher

        self._context_manager = context_manager

        self._prompt_composer = prompt_composer

        self._provider = provider

    # =====================================================
    # Public API
    # =====================================================

    def run(
        self,
        dataset_id: str,
        dataframe: pd.DataFrame,
        analysis: DatasetAnalysis,
        question: str,
    ) -> AgentResponse:
        """
        Execute the complete AI Agent pipeline.

        Args:
            dataset_id:
                Dataset identifier.

            dataframe:
                Uploaded dataset.

            analysis:
                Dataset analysis.

            question:
                User question.

        Returns:
            AgentResponse
        """

        logger.info(
            "Starting AI Agent execution."
        )

        logger.info(
            "Question: %s",
            question,
        )

        try:

            # --------------------------------------------
            # Step 1
            # Detect Intent
            # --------------------------------------------

            intent = self._intent_detector.detect(
                question
            )

            logger.info(
                "Detected intent: %s",
                intent.value,
            )

            # --------------------------------------------
            # Step 2
            # Create Plan
            # --------------------------------------------

            plan = self._planner.create_plan(
                intent=intent,
                question=question,
            )

            logger.info(
                "Execution steps: %d",
                len(
                    plan.execution_graph.steps
                ),
            )

            # --------------------------------------------
            # Step 3
            # Resolve Parameters
            # --------------------------------------------

            plan = self._parameter_resolver.resolve(
                plan=plan,
                dataframe=dataframe,
                question=question,
            )

            # --------------------------------------------
            # Step 4
            # Create Execution Graph
            # --------------------------------------------

            graph = ExecutionGraphManager(
                plan
            )

            tool_results: list[
                ToolResult
            ] = []
                        # --------------------------------------------
            # Step 5
            # Execute Plan
            # --------------------------------------------

            while graph.has_next():

                step = graph.next_step()

                if step is None:
                    break

                logger.info(
                    "Executing Step %d: %s",
                    step.step_number,
                    step.description,
                )

                try:

                    tool_result = self._dispatcher.execute(
                        dataset_id=dataset_id,
                        request=step.tool_request,
                    )

                    tool_results.append(tool_result)

                    logger.info(
                        "Tool '%s' executed successfully.",
                        tool_result.tool.value,
                    )

                except Exception as exc:

                    logger.exception(
                        "Tool execution failed."
                    )

                    tool_results.append(
                        ToolResult(
                     tool=step.tool_request.tool,
                     success=False,
                        message=str(exc),
                        payload={},
                        metadata=ToolMetadata(
                      execution_time=0.0,
                        ),
                        error=str(exc),
                     )
                )

                finally:

                    graph.mark_completed(
                        step.step_number
                    )

            logger.info(
                "Tool execution completed."
            )

            # --------------------------------------------
            # Step 6
            # Build Context
            # --------------------------------------------

            context = self._context_manager.build(
                question=question,
                dataframe=dataframe,
                analysis=analysis,
                tool_results=tool_results,
            )

            logger.info(
                "Context successfully built."
            )

            # --------------------------------------------
            # Step 7
            # Compose Prompt
            # --------------------------------------------

            llm_request = (
                self._prompt_composer.compose(
                    context=context,
                    intent=intent,
                )
            )

            logger.info(
                "Prompt successfully composed."
            )
