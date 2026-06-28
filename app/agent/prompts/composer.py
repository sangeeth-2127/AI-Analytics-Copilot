"""
Prompt Composer

Builds structured prompts for the AI Analytics Agent.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

from app.agent.models import (
    AgentContext,
    AgentIntent,
    LLMRequest,
)

from app.agent.prompts import (
    ANALYSIS_PROMPT,
    BASE_SYSTEM_PROMPT,
    RECOMMENDATION_PROMPT,
    REPORT_PROMPT,
    VISUALIZATION_PROMPT,
)


class PromptComposer:
    """
    Composes prompts for the language model.
    """

    _INTENT_PROMPTS = {
        AgentIntent.ANALYSIS: ANALYSIS_PROMPT,
        AgentIntent.VISUALIZATION: VISUALIZATION_PROMPT,
        AgentIntent.RECOMMENDATION: RECOMMENDATION_PROMPT,
        AgentIntent.REPORT: REPORT_PROMPT,
        AgentIntent.GENERAL: "",
    }

    def compose(
        self,
        context: AgentContext,
        intent: AgentIntent,
    ) -> LLMRequest:
        """
        Build an LLM request.

        Args:
            context:
                Agent execution context.

            intent:
                Detected user intent.

        Returns:
            LLMRequest
        """

        system_prompt = "\n\n".join(
            [
                BASE_SYSTEM_PROMPT,
                self._INTENT_PROMPTS[intent],
            ]
        ).strip()

        user_prompt = self._build_user_prompt(context)

        return LLMRequest(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2,
            max_tokens=1200,
        )

    # ======================================================
    # Private Helpers
    # ======================================================

    def _build_user_prompt(
        self,
        context: AgentContext,
    ) -> str:
        """
        Build the user prompt from the execution context.
        """

        return f"""
USER QUESTION
-------------
{context.user_question}

DATASET INFORMATION
-------------------
Rows: {context.dataset_info.get("rows")}
Columns: {context.dataset_info.get("columns")}
Memory Usage: {context.dataset_info.get("memory_usage_bytes")} bytes

Column Names:
{context.dataset_info.get("column_names")}

AVAILABLE COLUMNS
-----------------
Numeric:
{context.available_columns.get("numeric")}

Categorical:
{context.available_columns.get("categorical")}

Boolean:
{context.available_columns.get("boolean")}

Datetime:
{context.available_columns.get("datetime")}

DATASET ANALYSIS
----------------
{context.analysis}

SAMPLE ROWS
-----------
{context.sample_rows}

TOOL RESULTS
------------
{self._format_tool_results(context)}

Instructions
------------
Use ONLY the supplied context.

If the answer cannot be determined from the provided
context, explicitly state that additional information
is required.

Never fabricate values or observations.
""".strip()

    @staticmethod
    def _format_tool_results(
        context: AgentContext,
    ) -> str:
        """
        Convert tool results into a readable format.
        """

        if not context.tool_results:
            return "No tool results available."

        formatted_results: list[str] = []

        for result in context.tool_results:

            formatted_results.append(
                f"""
Tool: {result.tool.value}

Status: {"Success" if result.success else "Failed"}

Message:
{result.message}

Payload:
{result.payload}
""".strip()
            )

        return "\n\n".join(formatted_results)


prompt_composer = PromptComposer()