"""Check model confidence signals against a threshold."""

from __future__ import annotations

from agentguard.common.models import CheckResult, RiskLevel

_HEDGING_PHRASES = [
    "i'm not sure",
    "i don't know",
    "i cannot confirm",
    "it's possible that",
    "this might be",
    "i think",
    "perhaps",
    "it seems like",
    "i believe",
]


async def check(output_text: str, min_confidence: float = 0.5) -> CheckResult:
    """Heuristic confidence check based on hedging language density."""
    lower = output_text.lower()
    hedge_count = sum(1 for phrase in _HEDGING_PHRASES if phrase in lower)
    word_count = max(len(lower.split()), 1)
    hedge_ratio = hedge_count / (word_count / 50)  # normalize per ~50 words

    confidence = max(0.0, 1.0 - hedge_ratio)

    if confidence < min_confidence:
        return CheckResult(
            check_name="confidence_threshold",
            passed=False,
            decision="escalate",
            reason=f"Low confidence ({confidence:.2f} < {min_confidence})",
            severity=RiskLevel.MEDIUM,
            metadata={"confidence": round(confidence, 3), "hedge_count": hedge_count},
        )

    return CheckResult(
        check_name="confidence_threshold",
        passed=True,
        decision="pass",
        reason=f"Confidence adequate ({confidence:.2f})",
        metadata={"confidence": round(confidence, 3)},
    )
