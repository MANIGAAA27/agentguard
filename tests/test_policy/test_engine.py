"""Tests for the policy evaluation engine."""

from __future__ import annotations

from agentguard.policy.engine import _evaluate_rule, evaluate_policy, _policy_cache
from agentguard.policy.models import PolicyRule


def test_rule_equality_match():
    rule = PolicyRule(id="r1", description="test", condition={"channel": "api"}, decision="deny")
    assert _evaluate_rule(rule, {"channel": "api"})
    assert not _evaluate_rule(rule, {"channel": "web"})


def test_rule_in_operator():
    rule = PolicyRule(
        id="r2",
        description="test",
        condition={"role": {"$in": ["admin", "manager"]}},
        decision="allow",
    )
    assert _evaluate_rule(rule, {"role": "admin"})
    assert not _evaluate_rule(rule, {"role": "viewer"})


def test_rule_gt_operator():
    rule = PolicyRule(
        id="r3",
        description="test",
        condition={"amount": {"$gt": 1000}},
        decision="escalate",
    )
    assert _evaluate_rule(rule, {"amount": 5000})
    assert not _evaluate_rule(rule, {"amount": 500})


def test_rule_empty_condition_always_matches():
    rule = PolicyRule(id="r4", description="test", condition={}, decision="allow")
    assert _evaluate_rule(rule, {"anything": "value"})


def test_evaluate_default_policy():
    _policy_cache.clear()
    decision, results = evaluate_policy("default", {"requires_grounding": True, "grounded": False})
    assert decision.value == "deny"
    matched = [r for r in results if r["matched"]]
    assert len(matched) >= 1
