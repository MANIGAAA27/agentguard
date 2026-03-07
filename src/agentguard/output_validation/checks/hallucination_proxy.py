"""Proxy heuristic for hallucination detection.

Compares output claims against provided context. If the output makes specific
claims (dates, numbers, names) not found in the context, flag as potential hallucination.
"""

from __future__ import annotations

import re

from agentguard.common.models import CheckResult, RiskLevel

_SPECIFIC_CLAIM_PATTERN = re.compile(
    r"\b(?:\d{4}[-/]\d{2}[-/]\d{2}|\$[\d,.]+|\d+(?:\.\d+)?%)\b"
)


async def check(output_text: str, context_text: str) -> CheckResult:
    if not context_text:
        return CheckResult(
            check_name="hallucination_proxy",
            passed=True,
            decision="pass",
            reason="No context provided; hallucination check skipped",
        )

    output_claims = set(_SPECIFIC_CLAIM_PATTERN.findall(output_text))
    context_claims = set(_SPECIFIC_CLAIM_PATTERN.findall(context_text))

    unsupported = output_claims - context_claims
    if unsupported:
        ratio = len(unsupported) / max(len(output_claims), 1)
        severity = RiskLevel.HIGH if ratio > 0.5 else RiskLevel.MEDIUM
        return CheckResult(
            check_name="hallucination_proxy",
            passed=False,
            decision="repair" if ratio <= 0.5 else "reject",
            reason=f"Unsupported claims found: {unsupported}",
            severity=severity,
            metadata={"unsupported_claims": list(unsupported), "ratio": round(ratio, 3)},
        )

    return CheckResult(
        check_name="hallucination_proxy",
        passed=True,
        decision="pass",
        reason="All specific claims found in context",
    )
