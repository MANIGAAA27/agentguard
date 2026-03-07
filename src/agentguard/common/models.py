"""Shared Pydantic models used across all modules."""

from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class InputDecision(str, enum.Enum):
    ALLOW = "allow"
    REDACT = "redact"
    BLOCK = "block"
    ESCALATE = "escalate"
    SAFE_COMPLETE_ONLY = "safe-complete-only"


class OutputDecision(str, enum.Enum):
    PASS = "pass"
    REPAIR = "repair"
    REJECT = "reject"
    ESCALATE = "escalate"


class ActionDecision(str, enum.Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require-approval"
    DRY_RUN = "dry-run"
    ESCALATE = "escalate"


class PolicyDecision(str, enum.Enum):
    ALLOW = "allow"
    DENY = "deny"
    WARN = "warn"
    ESCALATE = "escalate"


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CheckResult(BaseModel):
    """Result from a single guardrail check."""

    check_name: str
    passed: bool
    decision: str
    reason: str
    severity: RiskLevel = RiskLevel.LOW
    metadata: dict[str, Any] = Field(default_factory=dict)


class AuditEntry(BaseModel):
    """Immutable audit log entry for every enforcement decision."""

    id: str = Field(default_factory=lambda: uuid4().hex)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tenant_id: str
    correlation_id: str
    module: str
    decision: str
    reason: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class RequestContext(BaseModel):
    """Context carried through the entire request pipeline."""

    correlation_id: str = Field(default_factory=lambda: uuid4().hex)
    tenant_id: str = "default"
    user_id: str | None = None
    channel: str = "api"
    use_case: str | None = None
    model_provider: str | None = None
    model_name: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
