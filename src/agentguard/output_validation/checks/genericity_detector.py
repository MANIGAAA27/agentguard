"""Detect low-value, generic AI responses (classic 'slop')."""

from __future__ import annotations

from agentguard.common.models import CheckResult, RiskLevel

_GENERIC_PHRASES = [
    "in today's fast-paced world",
    "it's important to note that",
    "there are many factors to consider",
    "it depends on your specific needs",
    "here are some general tips",
    "in conclusion",
    "as mentioned earlier",
    "it's worth noting that",
    "generally speaking",
    "there are pros and cons",
    "at the end of the day",
    "it's a complex topic",
    "let me break this down",
    "great question",
    "that's a really good question",
]

_GENERIC_THRESHOLD = 3


async def check(output_text: str) -> CheckResult:
    lower = output_text.lower()
    matches = [p for p in _GENERIC_PHRASES if p in lower]
    score = len(matches)

    if score >= _GENERIC_THRESHOLD:
        return CheckResult(
            check_name="genericity_detector",
            passed=False,
            decision="repair",
            reason=f"Output appears generic ({score} generic phrases detected)",
            severity=RiskLevel.LOW,
            metadata={"generic_phrases": matches, "genericity_score": score},
        )

    return CheckResult(
        check_name="genericity_detector",
        passed=True,
        decision="pass",
        reason="Output does not appear generic",
        metadata={"genericity_score": score},
    )
