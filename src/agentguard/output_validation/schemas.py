"""Request/response schemas for output validation."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from agentguard.common.models import CheckResult, OutputDecision


class OutputValidationRequest(BaseModel):
    """POST /v1/outputs/validate"""

    output_text: str = Field(..., description="The LLM-generated output to validate")
    context_text: str = Field("", description="Retrieved context used for grounding")
    expected_schema: dict[str, Any] | None = Field(None, description="JSON schema for output")
    require_citations: bool = Field(False, description="Whether citations are required")
    min_confidence: float = Field(0.5, ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class OutputValidationResponse(BaseModel):
    correlation_id: str
    decision: OutputDecision
    checks: list[CheckResult]
    metadata: dict[str, Any] = Field(default_factory=dict)
