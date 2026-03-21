"""Output validation check orchestrator."""

from __future__ import annotations

import asyncio
from typing import Any

from agentguard.common.models import CheckResult, OutputDecision
from agentguard.output_validation.checks import (
    citation_check,
    confidence_threshold,
    genericity_detector,
    hallucination_proxy,
    policy_check,
    schema_validity,
    unsafe_language,
)

_DECISION_PRIORITY = {
    "reject": 0,
    "escalate": 1,
    "repair": 2,
    "pass": 3,
}


async def validate_output(
    output_text: str,
    *,
    context_text: str = "",
    expected_schema: dict[str, Any] | None = None,
    require_citations: bool = False,
    min_confidence: float = 0.5,
) -> tuple[OutputDecision, list[CheckResult]]:
    """Run all output checks concurrently and return the aggregate decision."""
    results: list[CheckResult] = await asyncio.gather(
        schema_validity.check(output_text, expected_schema),
        citation_check.check(output_text, require_citations),
        hallucination_proxy.check(output_text, context_text),
        policy_check.check(output_text),
        unsafe_language.check(output_text),
        confidence_threshold.check(output_text, min_confidence),
        genericity_detector.check(output_text),
    )

    worst = "pass"
    for r in results:
        if _DECISION_PRIORITY.get(r.decision, 99) < _DECISION_PRIORITY.get(worst, 99):
            worst = r.decision

    return OutputDecision(worst), results
