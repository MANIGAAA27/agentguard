"""Detect toxic or abusive content in user input."""

from __future__ import annotations

import re

from agentguard.common.models import CheckResult, RiskLevel

_TOXIC_PATTERNS = [
    re.compile(r"\b(?:kill|murder|attack|bomb|shoot)\s+(?:people|someone|them)\b", re.IGNORECASE),
    re.compile(r"\b(?:hate|despise)\s+(?:all\s+)?(?:\w+\s+)?people\b", re.IGNORECASE),
    re.compile(r"\bhow\s+to\s+(?:make|build)\s+(?:a\s+)?(?:bomb|weapon|explosive)\b", re.IGNORECASE),
]


async def check(text: str) -> CheckResult:
    for pattern in _TOXIC_PATTERNS:
        if pattern.search(text):
            return CheckResult(
                check_name="toxicity",
                passed=False,
                decision="block",
                reason="Toxic or abusive content detected",
                severity=RiskLevel.CRITICAL,
            )
    return CheckResult(
        check_name="toxicity",
        passed=True,
        decision="allow",
        reason="No toxic content detected",
    )
