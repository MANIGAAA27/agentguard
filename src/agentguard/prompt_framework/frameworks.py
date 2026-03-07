"""Supported prompt framework types and their structural requirements."""

from __future__ import annotations

import enum
from typing import Any

from pydantic import BaseModel, Field


class FrameworkType(str, enum.Enum):
    RAG_QA = "RAG_QA"
    TOOL_USE = "TOOL_USE"
    STRUCTURED_SUMMARY = "STRUCTURED_SUMMARY"
    CLASSIFICATION = "CLASSIFICATION"
    CRITIC_REPAIR = "CRITIC_REPAIR"
    ACTION_EXECUTION = "ACTION_EXECUTION"


class FrameworkSpec(BaseModel):
    """Structural requirements for a prompt framework type."""

    type: FrameworkType
    requires_grounding: bool = False
    requires_output_schema: bool = False
    requires_tool_definitions: bool = False
    requires_refusal_policy: bool = True
    requires_role_definition: bool = True
    max_context_tokens: int | None = None


FRAMEWORK_SPECS: dict[FrameworkType, FrameworkSpec] = {
    FrameworkType.RAG_QA: FrameworkSpec(
        type=FrameworkType.RAG_QA,
        requires_grounding=True,
        requires_output_schema=False,
    ),
    FrameworkType.TOOL_USE: FrameworkSpec(
        type=FrameworkType.TOOL_USE,
        requires_tool_definitions=True,
        requires_output_schema=True,
    ),
    FrameworkType.STRUCTURED_SUMMARY: FrameworkSpec(
        type=FrameworkType.STRUCTURED_SUMMARY,
        requires_output_schema=True,
    ),
    FrameworkType.CLASSIFICATION: FrameworkSpec(
        type=FrameworkType.CLASSIFICATION,
        requires_output_schema=True,
    ),
    FrameworkType.CRITIC_REPAIR: FrameworkSpec(
        type=FrameworkType.CRITIC_REPAIR,
        requires_output_schema=True,
    ),
    FrameworkType.ACTION_EXECUTION: FrameworkSpec(
        type=FrameworkType.ACTION_EXECUTION,
        requires_tool_definitions=True,
        requires_output_schema=True,
    ),
}
