"""
Context Manager

Builds the execution context for the AI Analytics Agent.

The context manager gathers dataset information,
analysis results, and tool outputs into a single
AgentContext object.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from __future__ import annotations

import pandas as pd

from app.agent.models import (
    AgentContext,
    ToolResult,
)
from app.schemas.analysis import DatasetAnalysis


class ContextManager:
    """
    Builds an AgentContext from the current execution state.
    """

    SAMPLE_ROWS = 5

    def build(
        self,
        question: str,
        dataframe: pd.DataFrame,
        analysis: DatasetAnalysis,
        tool_results: list[ToolResult],
    ) -> AgentContext:
        """
        Build the context required by the AI Agent.

        Args:
            question:
                User question.

            dataframe:
                Active dataset.

            analysis:
                Dataset analysis.

            tool_results:
                Results returned by executed tools.

        Returns:
            AgentContext
        """

        return AgentContext(
            user_question=question,
            dataset_info=self._dataset_info(dataframe),
            analysis=analysis.model_dump(),
            available_columns=self._available_columns(dataframe),
            sample_rows=self._sample_rows(dataframe),
            tool_results=tool_results,
        )

    # ======================================================
    # Helper Methods
    # ======================================================

    @staticmethod
    def _dataset_info(
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Build dataset metadata.
        """

        return {
            "rows": len(dataframe),
            "columns": len(dataframe.columns),
            "column_names": dataframe.columns.tolist(),
            "memory_usage_bytes": int(
                dataframe.memory_usage(deep=True).sum()
            ),
        }

    @staticmethod
    def _available_columns(
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Categorize dataset columns by data type.
        """

        return {
            "numeric": dataframe.select_dtypes(
                include=["number"]
            ).columns.tolist(),

            "categorical": dataframe.select_dtypes(
                include=["object", "category"]
            ).columns.tolist(),

            "boolean": dataframe.select_dtypes(
                include=["bool"]
            ).columns.tolist(),

            "datetime": dataframe.select_dtypes(
                include=["datetime", "datetimetz"]
            ).columns.tolist(),
        }

    def _sample_rows(
        self,
        dataframe: pd.DataFrame,
    ) -> list[dict]:
        """
        Return sample rows for context.
        """

        return dataframe.head(
            self.SAMPLE_ROWS
        ).to_dict(
            orient="records"
        )


context_manager = ContextManager()