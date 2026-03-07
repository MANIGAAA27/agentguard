"""Rate limiting with pluggable backends."""

from __future__ import annotations

import time
from collections import defaultdict

from agentguard.common.exceptions import RateLimitExceeded
from agentguard.config import settings


class _InMemoryBucket:
    __slots__ = ("tokens", "last_refill")

    def __init__(self, capacity: int):
        self.tokens = capacity
        self.last_refill = time.monotonic()


_buckets: dict[str, _InMemoryBucket] = defaultdict(
    lambda: _InMemoryBucket(settings.rate_limit_requests_per_minute)
)


def check_rate_limit(tenant_id: str, rpm: int | None = None) -> None:
    """Consume one token for *tenant_id*. Raises RateLimitExceeded if exhausted."""
    if not settings.rate_limit_enabled:
        return

    capacity = rpm or settings.rate_limit_requests_per_minute
    bucket = _buckets[tenant_id]

    now = time.monotonic()
    elapsed = now - bucket.last_refill
    refill = int(elapsed * (capacity / 60.0))
    if refill > 0:
        bucket.tokens = min(capacity, bucket.tokens + refill)
        bucket.last_refill = now

    if bucket.tokens <= 0:
        raise RateLimitExceeded(f"Tenant {tenant_id} exceeded {capacity} requests/min")

    bucket.tokens -= 1
