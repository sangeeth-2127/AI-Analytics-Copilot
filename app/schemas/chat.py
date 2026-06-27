"""
Chat Schemas

Pydantic models for the AI Analytics Copilot.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.visualization import ChartType


class ChatRequest(BaseModel):
    """
    User request to the AI Copilot.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="Natural language question about the uploaded dataset.",
        examples=[
            "Show the distribution of Age.",
            "Compare Age and Overall.",
            "Which feature has the highest variance?",
            "Recommend a machine learning model.",
        ],
    )

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }


class CopilotAction(BaseModel):
    """
    Represents an action that the frontend
    or backend should perform.
    """

    type: Literal[
        "visualization",
        "analysis",
        "recommendation",
        "report",
    ] = Field(
        ...,
        description="Action type."
    )

    chart_type: ChartType | None = Field(
        default=None,
        description="Visualization type."
    )

    x_column: str | None = Field(
        default=None,
        description="Primary column."
    )

    y_column: str | None = Field(
        default=None,
        description="Secondary column."
    )

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }


class ChatResponse(BaseModel):
    """
    AI Copilot response.
    """

    answer: str = Field(
        ...,
        description="Natural language response."
    )

    actions: list[CopilotAction] = Field(
        default_factory=list,
        description="Actions requested by the AI."
    )

    model_config = {
        "extra": "forbid",
        "frozen": True,
    }