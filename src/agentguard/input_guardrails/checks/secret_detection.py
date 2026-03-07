"""Detect secrets and credentials in user input."""

from __future__ import annotations

import re

from agentguard.common.models import CheckResult, RiskLevel

_SECRET_PATTERNS = {
    "aws_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "github_token": re.compile(r"gh[ps]_[A-Za-z0-9_]{36,}"),
    "generic_api_key": re.compile(r"(?:api[_-]?key|apikey|secret[_-]?key)\s*[:=]\s*\S{8,}", re.IGNORECASE),
    "jwt_token": re.compile(r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
    "connection_string": re.compile(r"(?:postgres|mysql|mongodb)://\S+:\S+@\S+", re.IGNORECASE),
}


async def check(text: str) -> CheckResult:
    found: list[str] = []
    for name, pattern in _SECRET_PATTERNS.items():
        if pattern.search(text):
            found.append(name)

    if found:
        return CheckResult(
            check_name="secret_detection",
            passed=False,
            decision="block",
            reason=f"Secrets detected: {', '.join(found)}",
            severity=RiskLevel.CRITICAL,
            metadata={"secret_types": found},
        )
    return CheckResult(
        check_name="secret_detection",
        passed=True,
        decision="allow",
        reason="No secrets detected",
    )
