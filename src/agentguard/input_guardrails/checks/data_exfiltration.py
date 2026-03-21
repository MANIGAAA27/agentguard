"""Detect data exfiltration attempts (e.g., asking the model to leak training data)."""

from __future__ import annotations

import re

from agentguard.common.models import CheckResult, RiskLevel

_EXFIL_PATTERNS = [
    re.compile(r"(?:list|show|dump|print|output)\s+(?:all\s+)?(?:your\s+)?(?:training|system)\s+(?:data|prompt|instructions)", re.IGNORECASE),
    re.compile(r"repeat\s+(?:everything|all)\s+(?:above|before|from\s+the\s+start)", re.IGNORECASE),
    re.compile(r"(?:extract|exfiltrate|steal)\s+(?:data|information|records)", re.IGNORECASE),
    re.compile(r"send\s+(?:this|the|all)\s+(?:data|info|content)\s+to\s+", re.IGNORECASE),
]


async def check(text: str) -> CheckResult:
    for pattern in _EXFIL_PATTERNS:
        if pattern.search(text):
            return CheckResult(
                check_name="data_exfiltration",
                passed=False,
                decision="block",
                reason="Data exfiltration attempt detected",
                severity=RiskLevel.CRITICAL,
            )
    return CheckResult(
        check_name="data_exfiltration",
        passed=True,
        decision="allow",
        reason="No data exfiltration attempt detected",
    )
