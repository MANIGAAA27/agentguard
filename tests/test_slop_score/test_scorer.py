"""Tests for the AI Slop Prevention Score."""

from __future__ import annotations

from agentguard.common.models import CheckResult
from agentguard.slop_score.scorer import compute_slop_score


def test_clean_output_low_score():
    checks = [
        CheckResult(check_name="hallucination_proxy", passed=True, decision="pass", reason="ok"),
        CheckResult(check_name="genericity_detector", passed=True, decision="pass", reason="ok", metadata={"genericity_score": 0}),
        CheckResult(check_name="policy_check", passed=True, decision="pass", reason="ok"),
        CheckResult(check_name="unsafe_language", passed=True, decision="pass", reason="ok"),
    ]
    result = compute_slop_score(checks, grounded=True, schema_valid=True)
    assert result.score <= 0.3
    assert result.decision == "pass"


def test_ungrounded_increases_score():
    checks = [
        CheckResult(check_name="hallucination_proxy", passed=True, decision="pass", reason="ok"),
        CheckResult(check_name="genericity_detector", passed=True, decision="pass", reason="ok", metadata={"genericity_score": 0}),
        CheckResult(check_name="policy_check", passed=True, decision="pass", reason="ok"),
        CheckResult(check_name="unsafe_language", passed=True, decision="pass", reason="ok"),
    ]
    result = compute_slop_score(checks, grounded=False, schema_valid=True)
    assert result.score > 0.0
    assert result.components.grounding_coverage == 1.0


def test_high_slop_rejects():
    checks = [
        CheckResult(check_name="hallucination_proxy", passed=False, decision="reject", reason="bad", metadata={"ratio": 0.8}),
        CheckResult(check_name="genericity_detector", passed=False, decision="repair", reason="generic", metadata={"genericity_score": 5}),
        CheckResult(check_name="policy_check", passed=False, decision="repair", reason="violation"),
        CheckResult(check_name="unsafe_language", passed=True, decision="pass", reason="ok"),
    ]
    result = compute_slop_score(checks, grounded=False, schema_valid=False, action_risk=0.8)
    assert result.score > 0.7
    assert result.decision == "reject"
