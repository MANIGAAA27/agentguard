"""Request tracing with correlation IDs and structured logging."""

from __future__ import annotations

import structlog

logger = structlog.get_logger()


def log_request_start(
    correlation_id: str,
    tenant_id: str,
    endpoint: str,
    **extra: object,
) -> None:
    logger.info(
        "request.start",
        correlation_id=correlation_id,
        tenant_id=tenant_id,
        endpoint=endpoint,
        **extra,
    )


def log_request_end(
    correlation_id: str,
    tenant_id: str,
    endpoint: str,
    duration_ms: float,
    status: str = "ok",
    **extra: object,
) -> None:
    logger.info(
        "request.end",
        correlation_id=correlation_id,
        tenant_id=tenant_id,
        endpoint=endpoint,
        duration_ms=round(duration_ms, 2),
        status=status,
        **extra,
    )
