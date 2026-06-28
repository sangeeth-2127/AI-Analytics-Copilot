"""
Application Dependencies

Creates and manages application-level dependencies.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from functools import lru_cache

from app.agent.context.manager import ContextManager
from app.agent.orchestrator import AgentOrchestrator

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

from app.agent.registry.provider_registry import (
    provider_registry,
)

from app.agent.registry.tool_registry import (
    tool_registry,
)

from app.agent.tools.dispatcher import (
    ToolDispatcher,
)


# =====================================================
# Provider
# =====================================================

@lru_cache(maxsize=1)
def get_provider() -> BaseProvider:
    """
    Return the configured LLM provider.
    """

    return provider_registry.build()


# =====================================================
# Individual Components
# =====================================================

@lru_cache(maxsize=1)
def get_intent_detector() -> IntentDetector:
    """
    Return the singleton IntentDetector.
    """

    return IntentDetector()


@lru_cache(maxsize=1)
def get_task_planner() -> TaskPlanner:
    """
    Return the singleton TaskPlanner.
    """

    return TaskPlanner()


@lru_cache(maxsize=1)
def get_parameter_resolver() -> ParameterResolver:
    """
    Return the singleton ParameterResolver.
    """

    return ParameterResolver()


@lru_cache(maxsize=1)
def get_dispatcher() -> ToolDispatcher:
    """
    Return the configured ToolDispatcher.
    """

    return tool_registry.build()


@lru_cache(maxsize=1)
def get_context_manager() -> ContextManager:
    """
    Return the singleton ContextManager.
    """

    return ContextManager()


@lru_cache(maxsize=1)
def get_prompt_composer() -> PromptComposer:
    """
    Return the singleton PromptComposer.
    """

    return PromptComposer()


# =====================================================
# AI Agent
# =====================================================

@lru_cache(maxsize=1)
def get_agent() -> AgentOrchestrator:
    """
    Build the AI Analytics Agent.
    """

    return AgentOrchestrator(

        intent_detector=get_intent_detector(),

        planner=get_task_planner(),

        parameter_resolver=get_parameter_resolver(),

        dispatcher=get_dispatcher(),

        context_manager=get_context_manager(),

        prompt_composer=get_prompt_composer(),

        provider=get_provider(),
    )