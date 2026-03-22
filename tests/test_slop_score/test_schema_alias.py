"""Legacy JSON field ``score`` maps to ``quality_risk_score``."""

from __future__ import annotations

from agentguard.slop_score.schemas import SlopScoreResult


def test_model_validate_accepts_legacy_score_key():
    r = SlopScoreResult.model_validate(
        {
            "score": 0.42,
            "decision": "repair",
            "components": {},
        },
    )
    assert r.quality_risk_score == 0.42
    assert r.score == 0.42
