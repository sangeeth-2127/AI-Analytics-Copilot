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

from app.agent.context.manager import (
    ContextManager,
)

from app.agent.models import (
    AgentResponse,
    ToolExecutionContext,
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

from app.schemas.analysis import (
    DatasetAnalysis,
)

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Coordinates the complete AI Agent workflow.

    The orchestrator contains no business logic.
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
        """

        logger.info(
            "Starting AI Agent execution."
        )

        logger.info(
            "Question: %s",
            question,
        )

        tool_results: list[ToolResult] = []

        intent = None

        plan = None

        context = None

        try:

            # =====================================================
            # Step 1
            # Detect Intent
            # =====================================================

            intent = self._intent_detector.detect(
                question
            )

            logger.info(
                "Detected intent: %s",
                intent.value,
            )

            # =====================================================
            # Step 2
            # Create Execution Plan
            # =====================================================

            plan = self._planner.create_plan(
                intent=intent,
                question=question,
            )

            logger.info(
                "Execution plan created."
            )

            # =====================================================
            # Step 3
            # Resolve Parameters
            # =====================================================

            plan = self._parameter_resolver.resolve(
                plan=plan,
                dataframe=dataframe,
                question=question,
            )

            logger.info(
                "Tool parameters resolved."
            )

            # =====================================================
            # Step 4
            # Create Execution Graph
            # =====================================================

            graph = ExecutionGraphManager(
                plan
            )

            execution_context = ToolExecutionContext(
                dataset_id=dataset_id,
                dataframe=dataframe,
                analysis=analysis,
            )

            # =====================================================
            # Step 5
            # Execute Tools
            # =====================================================

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

                    result = self._dispatcher.execute(
                        context=execution_context,
                        request=step.tool_request,
                    )

                    tool_results.append(
                        result
                    )

                    logger.info(
                        "Tool '%s' executed successfully.",
                        result.tool.value,
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
                        step.step_number,
                    )

            logger.info(
                "Execution graph completed."
            )

            # ---------- CONTINUES IN PART B ----------
                        # =====================================================
            # Step 6
            # Build Agent Context
            # =====================================================

            context = self._context_manager.build(
                question=question,
                dataframe=dataframe,
                analysis=analysis,
                tool_results=tool_results,
            )

            logger.info(
                "Agent context built successfully."
            )

            # =====================================================
            # Step 7
            # Compose Prompt
            # =====================================================

            llm_request = (
                self._prompt_composer.compose(
                    context=context,
                    intent=intent,
                )
            )

            logger.info(
                "Prompt composed successfully."
            )

            # =====================================================
            # Step 8
            # Generate LLM Response
            # =====================================================

            llm_response = self._provider.generate(
                llm_request
            )

            logger.info(
                "LLM response generated successfully."
            )

            # =====================================================
            # Step 9
            # Build Final Response
            # =====================================================

            response = AgentResponse(

                success=True,

                answer=llm_response.content,

                intent=intent,

                plan=plan,

                context=context,

                tool_results=tool_results,

                llm_response=llm_response,
            )

            logger.info(
                "AI Agent execution completed successfully."
            )

            return response

        except Exception as exc:

            logger.exception(
                "AI Agent execution failed."
            )

            return AgentResponse(

                success=False,

                answer=(
                    "An unexpected error occurred "
                    "while processing your request."
                ),

                intent=intent,

                plan=plan,

                context=context,

                tool_results=tool_results,

                llm_response=None,
            )