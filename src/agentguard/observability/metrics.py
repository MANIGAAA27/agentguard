"""In-memory metrics collection for validation, hallucination, and refusal rates."""

from __future__ import annotations

from collections import defaultdict
from threading import Lock
from typing import Any


class MetricsCollector:
    """Thread-safe in-memory metrics collector. Production: replace with Prometheus/StatsD."""

    def __init__(self) -> None:
        self._counters: dict[str, int] = defaultdict(int)
        self._lock = Lock()

    def increment(self, metric: str, value: int = 1, tags: dict[str, str] | None = None) -> None:
        key = self._make_key(metric, tags)
        with self._lock:
            self._counters[key] += value

    def get(self, metric: str, tags: dict[str, str] | None = None) -> int:
        key = self._make_key(metric, tags)
        with self._lock:
            return self._counters[key]

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            return dict(self._counters)

    def reset(self) -> None:
        with self._lock:
            self._counters.clear()

    @staticmethod
    def _make_key(metric: str, tags: dict[str, str] | None) -> str:
        if not tags:
            return metric
        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{metric}{{{tag_str}}}"


metrics = MetricsCollector()
