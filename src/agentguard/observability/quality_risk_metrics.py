"""Counters for quality_risk_score samples (optional; in-memory MetricsCollector)."""

from __future__ import annotations

from agentguard.config import settings
from agentguard.observability.metrics import metrics


def _bucket(score: float) -> str:
    if score <= 0.3:
        return "low"
    if score <= 0.7:
        return "mid"
    return "high"


def record_quality_risk_sample(score: float, decision: str) -> None:
    if not settings.enable_quality_risk_metrics:
        return
    tags = {"bucket": _bucket(score), "decision": decision}
    metrics.increment("agentguard_quality_risk_total", tags=tags)
