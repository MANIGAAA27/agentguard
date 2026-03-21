"""Request/response schemas for input guardrails."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from agentguard.common.models import CheckResult, InputDecision


class InputEvaluationRequest(BaseModel):
    """POST /v1/guardrails/evaluate-input"""

    text: str = Field(..., description="The user input text to evaluate")
    use_case: str | None = Field(None, description="Use-case identifier for policy lookup")
    channel: str = Field("api", description="Originating channel")
    metadata: dict[str, Any] = Field(default_factory=dict)


class InputEvaluationResponse(BaseModel):
    correlation_id: str
    decision: InputDecision
    checks: list[CheckResult]
    redacted_text: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
