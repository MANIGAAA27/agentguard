"""Check that output contains citations when grounding is required."""

from __future__ import annotations

import re

from agentguard.common.models import CheckResult, RiskLevel

_CITATION_PATTERN = re.compile(r"\[\d+\]|\[source[:\s]", re.IGNORECASE)


async def check(output_text: str, require_citations: bool = False) -> CheckResult:
    if not require_citations:
        return CheckResult(
            check_name="citation_check",
            passed=True,
            decision="pass",
            reason="Citations not required for this use case",
        )

    citations_found = bool(_CITATION_PATTERN.search(output_text))
    if not citations_found:
        return CheckResult(
            check_name="citation_check",
            passed=False,
            decision="repair",
            reason="Output lacks citations but grounding is required",
            severity=RiskLevel.HIGH,
        )

    return CheckResult(
        check_name="citation_check",
        passed=True,
        decision="pass",
        reason="Citations present in output",
    )
