"""Audit trail logging for every enforcement decision."""

from __future__ import annotations

from typing import Any

import structlog

from agentguard.common.models import AuditEntry

logger = structlog.get_logger()

_audit_log: list[AuditEntry] = []
_MAX_IN_MEMORY = 10_000


def record_audit(
    tenant_id: str,
    correlation_id: str,
    module: str,
    decision: str,
    reason: str,
    metadata: dict[str, Any] | None = None,
) -> AuditEntry:
    """Record an audit entry. MVP: in-memory + structured log. Production: database."""
    entry = AuditEntry(
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        module=module,
        decision=decision,
        reason=reason,
        metadata=metadata or {},
    )

    logger.info(
        "audit.decision",
        audit_id=entry.id,
        tenant_id=tenant_id,
        correlation_id=correlation_id,
        module=module,
        decision=decision,
        reason=reason,
    )

    if len(_audit_log) >= _MAX_IN_MEMORY:
        _audit_log.pop(0)
    _audit_log.append(entry)

    return entry


def get_audit_log(
    tenant_id: str | None = None,
    limit: int = 100,
) -> list[AuditEntry]:
    """Retrieve recent audit entries, optionally filtered by tenant."""
    entries = _audit_log
    if tenant_id:
        entries = [e for e in entries if e.tenant_id == tenant_id]
    return entries[-limit:]
