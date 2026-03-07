"""Detect restricted or off-limits topics based on policy."""

from __future__ import annotations

import re

from agentguard.common.models import CheckResult, RiskLevel

_DEFAULT_RESTRICTED = [
    re.compile(r"\b(?:insider\s+trading|market\s+manipulation)\b", re.IGNORECASE),
    re.compile(r"\b(?:money\s+laundering)\b", re.IGNORECASE),
    re.compile(r"\b(?:illegal\s+drugs?|controlled\s+substances?)\s+(?:how|where|buy)\b", re.IGNORECASE),
    re.compile(r"\b(?:child\s+exploitation|csam)\b", re.IGNORECASE),
]


async def check(text: str, extra_patterns: list[re.Pattern[str]] | None = None) -> CheckResult:
    patterns = _DEFAULT_RESTRICTED + (extra_patterns or [])
    for pattern in patterns:
        if pattern.search(text):
            return CheckResult(
                check_name="restricted_topics",
                passed=False,
                decision="block",
                reason="Restricted topic detected",
                severity=RiskLevel.HIGH,
            )
    return CheckResult(
        check_name="restricted_topics",
        passed=True,
        decision="allow",
        reason="No restricted topics detected",
    )
