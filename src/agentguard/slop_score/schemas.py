"""Schemas for the composite output quality / risk score (internal module: slop_score)."""

from __future__ import annotations

from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class SlopScoreComponents(BaseModel):
    """Individual components of the composite quality/risk score."""

    grounding_coverage: float = Field(0.0, ge=0.0, le=1.0, description="0=fully grounded, 1=no grounding")
    schema_compliance: float = Field(0.0, ge=0.0, le=1.0, description="0=fully compliant, 1=non-compliant")
    unsupported_claim_ratio: float = Field(0.0, ge=0.0, le=1.0, description="Ratio of unsupported claims")
    genericity_score: float = Field(0.0, ge=0.0, le=1.0, description="0=specific, 1=very generic")
    policy_risk_score: float = Field(0.0, ge=0.0, le=1.0, description="Policy violation risk")
    action_risk_score: float = Field(0.0, ge=0.0, le=1.0, description="Action risk level")


class SlopScoreResult(BaseModel):
    """Composite quality/risk score for LLM output under heuristic checks."""

    model_config = ConfigDict(populate_by_name=True)

    quality_risk_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description=(
            "Composite quality/risk score (0 = low risk, 1 = high risk). "
            "The legacy JSON field `score` duplicates this value."
        ),
        validation_alias=AliasChoices("quality_risk_score", "score"),
    )
    decision: str = Field(..., description="pass | repair | reject")
    components: SlopScoreComponents
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def score(self) -> float:
        """Deprecated in documentation; use ``quality_risk_score``. Same numeric value."""
        return self.quality_risk_score

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        data = super().model_dump(**kwargs)
        data["score"] = data["quality_risk_score"]
        return data
