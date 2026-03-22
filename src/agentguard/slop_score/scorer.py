"""AI Slop Prevention Score -- composite scoring model."""

from __future__ import annotations

from agentguard.common.models import CheckResult
from agentguard.config import settings
from agentguard.slop_score.schemas import SlopScoreComponents, SlopScoreResult

_DEFAULT_WEIGHTS = {
    "grounding_coverage": 0.25,
    "schema_compliance": 0.15,
    "unsupported_claim_ratio": 0.20,
    "genericity_score": 0.15,
    "policy_risk_score": 0.15,
    "action_risk_score": 0.10,
}


def compute_slop_score(
    output_checks: list[CheckResult],
    *,
    grounded: bool = True,
    schema_valid: bool = True,
    action_risk: float = 0.0,
    weights: dict[str, float] | None = None,
) -> SlopScoreResult:
    """Compute the composite AI Slop Prevention Score from check results.

    Score range: 0.0 (clean) to 1.0 (maximum slop).
    """
    w = weights or _DEFAULT_WEIGHTS

    grounding_coverage = 0.0 if grounded else 1.0
    schema_compliance = 0.0 if schema_valid else 1.0

    unsupported_ratio = 0.0
    genericity = 0.0
    policy_risk = 0.0

    for check in output_checks:
        if check.check_name == "hallucination_proxy" and not check.passed:
            unsupported_ratio = check.metadata.get("ratio", 0.5)
        if check.check_name == "genericity_detector":
            genericity = min(check.metadata.get("genericity_score", 0) / 5.0, 1.0)
        if check.check_name == "policy_check" and not check.passed:
            policy_risk = 0.7
        if check.check_name == "unsafe_language" and not check.passed:
            policy_risk = 1.0

    components = SlopScoreComponents(
        grounding_coverage=round(grounding_coverage, 3),
        schema_compliance=round(schema_compliance, 3),
        unsupported_claim_ratio=round(unsupported_ratio, 3),
        genericity_score=round(genericity, 3),
        policy_risk_score=round(policy_risk, 3),
        action_risk_score=round(action_risk, 3),
    )

    composite = (
        w["grounding_coverage"] * grounding_coverage
        + w["schema_compliance"] * schema_compliance
        + w["unsupported_claim_ratio"] * unsupported_ratio
        + w["genericity_score"] * genericity
        + w["policy_risk_score"] * policy_risk
        + w["action_risk_score"] * action_risk
    )
    composite = round(min(composite, 1.0), 3)

    if composite <= settings.slop_score_threshold_pass:
        decision = "pass"
    elif composite <= settings.slop_score_threshold_repair:
        decision = "repair"
    else:
        decision = "reject"

    return SlopScoreResult(
        quality_risk_score=composite,
        decision=decision,
        components=components,
    )
