"""Detect personally identifiable information (PII) in user input."""

from __future__ import annotations

import re

from agentguard.common.models import CheckResult, RiskLevel

_PII_PATTERNS = {
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "phone_us": re.compile(r"\b(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "credit_card": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
    "ip_address": re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
}


async def check(text: str) -> CheckResult:
    found: list[str] = []
    for name, pattern in _PII_PATTERNS.items():
        if pattern.search(text):
            found.append(name)

    if found:
        return CheckResult(
            check_name="pii_detection",
            passed=False,
            decision="redact",
            reason=f"PII detected: {', '.join(found)}",
            severity=RiskLevel.HIGH,
            metadata={"pii_types": found},
        )
    return CheckResult(
        check_name="pii_detection",
        passed=True,
        decision="allow",
        reason="No PII detected",
    )
