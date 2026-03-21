"""Action risk scoring based on action type, parameters, and context."""

from __future__ import annotations

from typing import Any

from agentguard.common.models import RiskLevel
from agentguard.action_governance.allowlist import get_tool_config

_RISK_THRESHOLDS = {
    RiskLevel.LOW: 0.3,
    RiskLevel.MEDIUM: 0.5,
    RiskLevel.HIGH: 0.7,
    RiskLevel.CRITICAL: 0.85,
}

_HIGH_RISK_ACTIONS = {
    "delete_record", "refund_approval", "customer_entitlement_override",
    "crm_data_mutation", "bulk_update",
}

_SENSITIVE_PARAM_KEYS = {"password", "secret", "token", "ssn", "credit_card"}


def score_action(
    action: str,
    tool: str,
    parameters: dict[str, Any],
) -> tuple[float, RiskLevel]:
    """Compute a risk score (0.0-1.0) and risk level for an action."""
    base_score = 0.3

    tool_config = get_tool_config(tool)
    if tool_config:
        base_score = tool_config.get("risk_base", 0.3)

    if action in _HIGH_RISK_ACTIONS:
        base_score = max(base_score, 0.7)

    param_penalty = 0.0
    for key in parameters:
        if key.lower() in _SENSITIVE_PARAM_KEYS:
            param_penalty += 0.1

    if "amount" in parameters:
        try:
            amount = float(parameters["amount"])
            if amount > 1000:
                param_penalty += 0.15
            if amount > 10000:
                param_penalty += 0.15
        except (ValueError, TypeError):
            pass

    if isinstance(parameters.get("record_ids"), list) and len(parameters["record_ids"]) > 10:
        param_penalty += 0.2

    final_score = min(base_score + param_penalty, 1.0)

    level = RiskLevel.LOW
    for risk_level, threshold in sorted(_RISK_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
        if final_score >= threshold:
            level = risk_level
            break

    return round(final_score, 3), level
