"""Request/response schemas for the policy engine."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from agentguard.common.models import PolicyDecision


class PolicyEvaluateRequest(BaseModel):
    """POST /v1/policies/evaluate"""

    policy_name: str = Field(..., description="Name of the policy set to evaluate")
    context: dict[str, Any] = Field(
        ...,
        description="Request context to evaluate against policy rules",
    )


class PolicyEvaluateResponse(BaseModel):
    correlation_id: str
    decision: PolicyDecision
    policy_name: str
    rule_results: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
