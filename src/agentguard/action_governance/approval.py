"""Human-in-the-loop approval workflow for sensitive actions."""

from __future__ import annotations

from agentguard.common.models import RiskLevel

_HITL_THRESHOLD = RiskLevel.HIGH

_seen_idempotency_keys: set[str] = set()


def requires_approval(risk_level: RiskLevel) -> bool:
    """Determine if an action requires human approval based on risk level."""
    risk_order = [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]
    threshold_idx = risk_order.index(_HITL_THRESHOLD)
    current_idx = risk_order.index(risk_level)
    return current_idx >= threshold_idx


def check_idempotency(key: str | None) -> bool:
    """Returns True if this is a duplicate request (replay). False if new."""
    if not key:
        return False
    if key in _seen_idempotency_keys:
        return True
    _seen_idempotency_keys.add(key)
    return False
