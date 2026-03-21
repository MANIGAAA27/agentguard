"""Detect unsafe or harmful language in LLM output."""

from __future__ import annotations

import re

from agentguard.common.models import CheckResult, RiskLevel

_UNSAFE_OUTPUT_PATTERNS = [
    re.compile(r"\b(?:kill|murder|harm)\s+(?:yourself|themselves|people)\b", re.IGNORECASE),
    re.compile(r"\b(?:instructions?\s+(?:to|for)\s+(?:making|building)\s+(?:a\s+)?(?:bomb|weapon))\b", re.IGNORECASE),
    re.compile(r"\b(?:here(?:'s|\s+is)\s+how\s+to\s+(?:hack|exploit|attack))\b", re.IGNORECASE),
]


async def check(output_text: str) -> CheckResult:
    for pattern in _UNSAFE_OUTPUT_PATTERNS:
        if pattern.search(output_text):
            return CheckResult(
                check_name="unsafe_language",
                passed=False,
                decision="reject",
                reason="Unsafe language detected in output",
                severity=RiskLevel.CRITICAL,
            )
    return CheckResult(
        check_name="unsafe_language",
        passed=True,
        decision="pass",
        reason="No unsafe language detected",
    )
