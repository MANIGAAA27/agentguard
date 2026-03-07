"""Tool allowlist and parameter validation."""

from __future__ import annotations

from typing import Any

_TOOL_ALLOWLIST: dict[str, dict[str, Any]] = {
    "search_documents": {
        "description": "Search internal document store",
        "risk_base": 0.1,
        "required_params": ["query"],
        "max_risk": "low",
    },
    "send_email": {
        "description": "Send an email to a customer",
        "risk_base": 0.4,
        "required_params": ["to", "subject", "body"],
        "max_risk": "medium",
    },
    "update_record": {
        "description": "Update a CRM record",
        "risk_base": 0.5,
        "required_params": ["record_id", "fields"],
        "max_risk": "medium",
    },
    "delete_record": {
        "description": "Delete a record from the system",
        "risk_base": 0.8,
        "required_params": ["record_id"],
        "max_risk": "critical",
    },
    "refund_approval": {
        "description": "Approve a customer refund",
        "risk_base": 0.7,
        "required_params": ["order_id", "amount"],
        "max_risk": "high",
    },
    "bulk_update": {
        "description": "Bulk update multiple records",
        "risk_base": 0.9,
        "required_params": ["record_ids", "fields"],
        "max_risk": "critical",
    },
}


def is_tool_allowed(tool: str) -> bool:
    return tool in _TOOL_ALLOWLIST


def get_tool_config(tool: str) -> dict[str, Any] | None:
    return _TOOL_ALLOWLIST.get(tool)


def validate_parameters(tool: str, parameters: dict[str, Any]) -> list[str]:
    """Validate that required parameters are present. Returns list of errors."""
    config = _TOOL_ALLOWLIST.get(tool)
    if not config:
        return [f"Tool '{tool}' is not in the allowlist"]

    errors = []
    for param in config.get("required_params", []):
        if param not in parameters:
            errors.append(f"Missing required parameter: {param}")
    return errors
