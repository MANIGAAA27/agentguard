"""Tenant isolation and resolution."""

from __future__ import annotations

from typing import Any

from agentguard.config import settings

# MVP: in-memory tenant registry. Production: database or config service.
_TENANT_REGISTRY: dict[str, dict[str, Any]] = {
    "default": {
        "id": "default",
        "name": "Default Tenant",
        "policy": "default",
        "rate_limit_rpm": 60,
        "allowed_models": ["gpt-4o", "claude-sonnet-4-20250514"],
    },
}


def get_tenant_config(tenant_id: str) -> dict[str, Any]:
    """Return tenant configuration. Falls back to default."""
    return _TENANT_REGISTRY.get(tenant_id, _TENANT_REGISTRY[settings.default_tenant_id])


def register_tenant(tenant_id: str, config: dict[str, Any]) -> None:
    """Register or update a tenant configuration at runtime."""
    _TENANT_REGISTRY[tenant_id] = config
