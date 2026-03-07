"""Policy-as-code evaluation engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from agentguard.common.models import PolicyDecision
from agentguard.config import settings
from agentguard.policy.models import PolicyRule, PolicySet

_policy_cache: dict[str, PolicySet] = {}


def load_policy(name: str) -> PolicySet:
    """Load a policy set from YAML file."""
    if name in _policy_cache:
        return _policy_cache[name]

    policy_path = Path(settings.policy_dir) / f"{name}.yaml"
    if not policy_path.exists():
        examples_path = Path(settings.policy_dir) / "examples" / f"{name}.yaml"
        if examples_path.exists():
            policy_path = examples_path
        else:
            return PolicySet(name=name, rules=[])

    with open(policy_path) as f:
        data = yaml.safe_load(f)

    policy = PolicySet(**data)
    _policy_cache[name] = policy
    return policy


def evaluate_policy(
    policy_name: str,
    context: dict[str, Any],
) -> tuple[PolicyDecision, list[dict[str, Any]]]:
    """Evaluate a policy set against a request context.

    Returns (aggregate_decision, list_of_rule_results).
    """
    policy = load_policy(policy_name)
    results: list[dict[str, Any]] = []
    worst_decision = "allow"
    decision_priority = {"deny": 0, "escalate": 1, "warn": 2, "allow": 3}

    sorted_rules = sorted(policy.rules, key=lambda r: r.priority)

    for rule in sorted_rules:
        matched = _evaluate_rule(rule, context)
        result = {
            "rule_id": rule.id,
            "description": rule.description,
            "matched": matched,
            "decision": rule.decision if matched else "allow",
        }
        results.append(result)

        if matched:
            rule_decision = rule.decision
            if decision_priority.get(rule_decision, 99) < decision_priority.get(worst_decision, 99):
                worst_decision = rule_decision

    return PolicyDecision(worst_decision), results


def _evaluate_rule(rule: PolicyRule, context: dict[str, Any]) -> bool:
    """Evaluate a single rule's conditions against context.

    Condition format: {"field": "value"} for equality,
    {"field": {"$in": [...]}} for membership,
    {"field": {"$gt": n}} for comparison.
    """
    if not rule.condition:
        return True

    for field, expected in rule.condition.items():
        actual = context.get(field)
        if isinstance(expected, dict):
            if "$in" in expected and actual not in expected["$in"]:
                return False
            if "$gt" in expected and (actual is None or actual <= expected["$gt"]):
                return False
            if "$lt" in expected and (actual is None or actual >= expected["$lt"]):
                return False
            if "$ne" in expected and actual == expected["$ne"]:
                return False
        elif actual != expected:
            return False

    return True
