"""Schemas for the AI Slop Prevention Score."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SlopScoreComponents(BaseModel):
    """Individual components of the slop score."""

    grounding_coverage: float = Field(0.0, ge=0.0, le=1.0, description="0=fully grounded, 1=no grounding")
    schema_compliance: float = Field(0.0, ge=0.0, le=1.0, description="0=fully compliant, 1=non-compliant")
    unsupported_claim_ratio: float = Field(0.0, ge=0.0, le=1.0, description="Ratio of unsupported claims")
    genericity_score: float = Field(0.0, ge=0.0, le=1.0, description="0=specific, 1=very generic")
    policy_risk_score: float = Field(0.0, ge=0.0, le=1.0, description="Policy violation risk")
    action_risk_score: float = Field(0.0, ge=0.0, le=1.0, description="Action risk level")


class SlopScoreResult(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0, description="Composite slop score (0=clean, 1=maximum slop)")
    decision: str = Field(..., description="pass | repair | reject")
    components: SlopScoreComponents
    metadata: dict[str, Any] = Field(default_factory=dict)
