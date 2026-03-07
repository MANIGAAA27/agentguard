"""Detect prompt injection attempts in user input."""

from __future__ import annotations

import re

from agentguard.common.models import CheckResult, RiskLevel

_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+(?:a|an)\s+", re.IGNORECASE),
    re.compile(r"system\s*:\s*", re.IGNORECASE),
    re.compile(r"<\|?(?:system|im_start|endoftext)\|?>", re.IGNORECASE),
    re.compile(r"(?:forget|disregard)\s+(?:everything|all|your)\s+", re.IGNORECASE),
    re.compile(r"new\s+instructions?\s*:", re.IGNORECASE),
    re.compile(r"override\s+(?:your|the)\s+(?:system|rules)", re.IGNORECASE),
]


async def check(text: str) -> CheckResult:
    for pattern in _INJECTION_PATTERNS:
        if pattern.search(text):
            return CheckResult(
                check_name="prompt_injection",
                passed=False,
                decision="block",
                reason=f"Prompt injection pattern detected: {pattern.pattern}",
                severity=RiskLevel.CRITICAL,
            )
    return CheckResult(
        check_name="prompt_injection",
        passed=True,
        decision="allow",
        reason="No prompt injection detected",
    )
