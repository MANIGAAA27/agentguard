"""Policy data models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PolicyRule(BaseModel):
    """A single policy rule within a policy set."""

    id: str
    description: str
    scope: str = "global"  # global | tenant | use_case | channel | role
    condition: dict[str, Any] = Field(default_factory=dict)
    decision: str = "allow"  # allow | deny | warn | escalate
    priority: int = 100  # lower = higher priority


class PolicySet(BaseModel):
    """A named collection of policy rules."""

    name: str
    version: str = "1.0.0"
    description: str = ""
    tenant_id: str | None = None
    rules: list[PolicyRule] = Field(default_factory=list)
