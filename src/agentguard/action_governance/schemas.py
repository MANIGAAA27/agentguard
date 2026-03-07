"""Request/response schemas for action governance."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from agentguard.common.models import ActionDecision, RiskLevel


class ActionAuthorizeRequest(BaseModel):
    """POST /v1/actions/authorize"""

    action: str = Field(..., description="Action name (e.g., 'delete_record', 'refund_approval')")
    tool: str = Field(..., description="Tool or service being invoked")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Action parameters")
    dry_run: bool = Field(False, description="If true, evaluate but do not execute")
    idempotency_key: str | None = Field(None, description="Idempotency key for replay protection")
    metadata: dict[str, Any] = Field(default_factory=dict)


class ActionAuthorizeResponse(BaseModel):
    correlation_id: str
    decision: ActionDecision
    risk_level: RiskLevel
    risk_score: float
    reason: str
    requires_approval: bool = False
    dry_run: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)
