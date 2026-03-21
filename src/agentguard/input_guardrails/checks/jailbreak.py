"""Detect jailbreak attempts (DAN, role-play exploits, etc.)."""

from __future__ import annotations

import re

from agentguard.common.models import CheckResult, RiskLevel

_JAILBREAK_PATTERNS = [
    re.compile(r"\bDAN\b.*\bmode\b", re.IGNORECASE),
    re.compile(r"do\s+anything\s+now", re.IGNORECASE),
    re.compile(r"jailbreak", re.IGNORECASE),
    re.compile(r"pretend\s+(?:you\s+)?(?:are|have)\s+no\s+(?:rules|restrictions)", re.IGNORECASE),
    re.compile(r"act\s+as\s+(?:an?\s+)?unrestricted", re.IGNORECASE),
    re.compile(r"developer\s+mode\s+enabled", re.IGNORECASE),
]


async def check(text: str) -> CheckResult:
    for pattern in _JAILBREAK_PATTERNS:
        if pattern.search(text):
            return CheckResult(
                check_name="jailbreak",
                passed=False,
                decision="block",
                reason=f"Jailbreak pattern detected: {pattern.pattern}",
                severity=RiskLevel.CRITICAL,
            )
    return CheckResult(
        check_name="jailbreak",
        passed=True,
        decision="allow",
        reason="No jailbreak attempt detected",
    )
