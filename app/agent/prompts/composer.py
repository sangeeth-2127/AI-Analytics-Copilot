"""
Prompt Composer

Builds structured prompts for the AI Analytics Copilot.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import json

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
    Builds prompts for the language model.
    """

    _INTENT_PROMPTS = {

        AgentIntent.ANALYSIS:
            ANALYSIS_PROMPT,

        AgentIntent.VISUALIZATION:
            VISUALIZATION_PROMPT,

        AgentIntent.RECOMMENDATION:
            RECOMMENDATION_PROMPT,

        AgentIntent.REPORT:
            REPORT_PROMPT,

        AgentIntent.GENERAL:
            "",
    }

    # =====================================================
    # Public API
    # =====================================================

    def compose(
        self,
        context: AgentContext,
        intent: AgentIntent,
    ) -> LLMRequest:
        """
        Build the final LLM request.
        """

        system_prompt = self._build_system_prompt(
            intent
        )

        user_prompt = self._build_user_prompt(
            context
        )

        return LLMRequest(

            system_prompt=system_prompt,

            user_prompt=user_prompt,

            temperature=0.2,

            max_tokens=1200,
        )

    # =====================================================
    # System Prompt
    # =====================================================

    def _build_system_prompt(
        self,
        intent: AgentIntent,
    ) -> str:
        """
        Build the system prompt.
        """

        intent_prompt = (
            self._INTENT_PROMPTS.get(
                intent,
                "",
            )
        )

        return "\n\n".join(

            [

                BASE_SYSTEM_PROMPT,

                intent_prompt,

            ]

        ).strip()

    # =====================================================
    # User Prompt
    # =====================================================

    def _build_user_prompt(
        self,
        context: AgentContext,
    ) -> str:
        """
        Build the user prompt.
        """

        return f"""
==============================
USER QUESTION
==============================

{context.user_question}

==============================
DATASET INFORMATION
==============================

Rows:
{context.dataset_info["rows"]}

Columns:
{context.dataset_info["columns"]}

Memory Usage:
{context.dataset_info["memory_usage_bytes"]}

Column Names:

{context.dataset_info["column_names"]}

==============================
AVAILABLE COLUMNS
==============================

Numeric

{context.available_columns["numeric"]}

Categorical

{context.available_columns["categorical"]}

Boolean

{context.available_columns["boolean"]}

Datetime

{context.available_columns["datetime"]}

==============================
DATASET ANALYSIS
==============================

{json.dumps(
context.analysis,
indent=2,
default=str,
)}

==============================
SAMPLE ROWS
==============================

{json.dumps(
context.sample_rows,
indent=2,
default=str,
)}

==============================
TOOL RESULTS
==============================

{self._tool_results(
context
)}

==============================
INSTRUCTIONS
==============================

1. Use ONLY the supplied dataset.

2. Never fabricate information.

3. Never assume values.

4. If information is unavailable,
say so explicitly.

5. Explain your reasoning clearly.

6. If charts were generated,
include observations.

7. If recommendations were
generated,
explain why.

8. Respond professionally.
""".strip()

    # =====================================================
    # Tool Results
    # =====================================================

    @staticmethod
    def _tool_results(
        context: AgentContext,
    ) -> str:
        """
        Format tool results.
        """

        if not context.tool_results:

            return "No tools executed."

        sections = []

        for result in context.tool_results:

            sections.append(

                f"""
Tool

{result.tool.value}

Status

{"Success" if result.success else "Failed"}

Message

{result.message}

Payload

{json.dumps(
result.payload,
indent=2,
default=str,
)}
""".strip()

            )

        return "\n\n".join(
            sections
        )


prompt_composer = PromptComposer()