"""Tests for action governance risk scoring."""

from __future__ import annotations

from agentguard.action_governance.allowlist import is_tool_allowed, validate_parameters
from agentguard.action_governance.risk_scorer import score_action
from agentguard.common.models import RiskLevel


def test_allowed_tool():
    assert is_tool_allowed("search_documents")
    assert not is_tool_allowed("hack_system")


def test_parameter_validation_pass():
    errors = validate_parameters("search_documents", {"query": "test"})
    assert len(errors) == 0


def test_parameter_validation_fail():
    errors = validate_parameters("search_documents", {})
    assert len(errors) == 1
    assert "query" in errors[0]


def test_low_risk_action():
    score, level = score_action("search", "search_documents", {"query": "test"})
    assert score < 0.5
    assert level in (RiskLevel.LOW, RiskLevel.MEDIUM)


def test_high_risk_action():
    score, level = score_action("delete_record", "delete_record", {"record_id": "123"})
    assert score >= 0.7
    assert level in (RiskLevel.HIGH, RiskLevel.CRITICAL)


def test_bulk_update_critical():
    score, level = score_action(
        "bulk_update",
        "bulk_update",
        {"record_ids": list(range(20)), "fields": {"status": "archived"}},
    )
    assert score >= 0.85
    assert level == RiskLevel.CRITICAL
