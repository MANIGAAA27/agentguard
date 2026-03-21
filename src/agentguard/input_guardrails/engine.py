"""Check orchestrator -- runs all input checks in parallel and aggregates decisions."""

from __future__ import annotations

import asyncio

from agentguard.common.models import CheckResult, InputDecision
from agentguard.input_guardrails.checks import (
    data_exfiltration,
    jailbreak,
    pii_detection,
    prompt_injection,
    restricted_topics,
    secret_detection,
    toxicity,
)

_DECISION_PRIORITY = {
    "block": 0,
    "escalate": 1,
    "safe-complete-only": 2,
    "redact": 3,
    "allow": 4,
}


async def evaluate_input(text: str) -> tuple[InputDecision, list[CheckResult], str | None]:
    """Run all input checks concurrently and return the aggregate decision.

    Returns (decision, check_results, redacted_text_or_none).
    """
    results: list[CheckResult] = await asyncio.gather(
        prompt_injection.check(text),
        jailbreak.check(text),
        toxicity.check(text),
        pii_detection.check(text),
        secret_detection.check(text),
        restricted_topics.check(text),
        data_exfiltration.check(text),
    )

    worst_decision = "allow"
    for r in results:
        if _DECISION_PRIORITY.get(r.decision, 99) < _DECISION_PRIORITY.get(worst_decision, 99):
            worst_decision = r.decision

    redacted_text: str | None = None
    if worst_decision == "redact":
        redacted_text = _apply_redaction(text, results)

    return InputDecision(worst_decision), results, redacted_text


def _apply_redaction(text: str, results: list[CheckResult]) -> str:
    """Replace detected PII/secrets with placeholders."""
    import re

    redacted = text
    for r in results:
        if r.decision == "redact" and r.metadata.get("pii_types"):
            for pii_type in r.metadata["pii_types"]:
                from agentguard.input_guardrails.checks.pii_detection import get_pii_patterns

                pattern = get_pii_patterns().get(pii_type)
                if pattern:
                    redacted = pattern.sub(f"[REDACTED_{pii_type.upper()}]", redacted)
    return redacted
