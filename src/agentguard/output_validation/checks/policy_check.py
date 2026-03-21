"""Check output against policy rules (e.g., forbidden topics in responses)."""

from __future__ import annotations

import re

from agentguard.common.models import CheckResult, RiskLevel

_POLICY_VIOLATION_PATTERNS = [
    re.compile(r"\b(?:I\s+(?:am|was)\s+(?:trained|created)\s+by)\b", re.IGNORECASE),
    re.compile(r"\b(?:as\s+an?\s+AI\s+(?:language\s+)?model)\b", re.IGNORECASE),
    re.compile(r"\b(?:I\s+(?:cannot|can't|don't)\s+have\s+(?:feelings|emotions|opinions))\b", re.IGNORECASE),
]


async def check(output_text: str) -> CheckResult:
    for pattern in _POLICY_VIOLATION_PATTERNS:
        if pattern.search(output_text):
            return CheckResult(
                check_name="policy_check",
                passed=False,
                decision="repair",
                reason="Output contains policy-violating disclosure pattern",
                severity=RiskLevel.MEDIUM,
            )
    return CheckResult(
        check_name="policy_check",
        passed=True,
        decision="pass",
        reason="No policy violations detected in output",
    )
