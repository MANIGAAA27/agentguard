"""Detect prompt injection attempts in user input.

Uses a two-tier model:
- **Critical** patterns (high precision): any match blocks immediately.
- **Scored** patterns (lower precision alone): each match adds weight; block only if the
  cumulative score meets ``SCORE_BLOCK_THRESHOLD``. This reduces false positives from
  single broad matches on legitimate enterprise text.

This remains a heuristic; it is not a substitute for ML-backed classifiers or human review.
See README *Limitations* and *Input Guardrails* for scope.
"""

from __future__ import annotations

import re

from agentguard.common.models import CheckResult, RiskLevel

# Immediate block — patterns tuned for adversarial paraphrases of instruction override.
_CRITICAL_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"(?:forget|disregard)\s+(?:everything|all|your)\s+", re.IGNORECASE),
    re.compile(r"override\s+(?:your|the)\s+(?:system|rules)", re.IGNORECASE),
    re.compile(r"<\|?(?:system|im_start|endoftext)\|?>", re.IGNORECASE),
    re.compile(r"new\s+instructions?\s*:", re.IGNORECASE),
]

# Contributed to score — narrowed to avoid common business phrasing.
# ``system:`` only at line start (not "Our system: uptime").
_SCORED: list[tuple[re.Pattern[str], int]] = [
    # Role injection: article + word ("...a helpful..." not "...able to...")
    (re.compile(r"\byou\s+are\s+now\s+(?:a|an)\s+\w+", re.IGNORECASE), 4),
    # Pretend system message at beginning of a line only
    (re.compile(r"(?m)^\s*system\s*:\s*\S", re.IGNORECASE), 4),
]

# One scored hit (weight 4) meets threshold; adjust weights/threshold together if tuning.
SCORE_BLOCK_THRESHOLD = 4


async def check(text: str) -> CheckResult:
    for pattern in _CRITICAL_PATTERNS:
        if pattern.search(text):
            return CheckResult(
                check_name="prompt_injection",
                passed=False,
                decision="block",
                reason="Prompt injection pattern detected (critical)",
                severity=RiskLevel.CRITICAL,
                metadata={"pattern_type": "critical", "pattern": pattern.pattern},
            )

    score = 0
    matched: list[str] = []
    for pattern, weight in _SCORED:
        if pattern.search(text):
            score += weight
            matched.append(pattern.pattern)

    if score >= SCORE_BLOCK_THRESHOLD:
        return CheckResult(
            check_name="prompt_injection",
            passed=False,
            decision="block",
            reason="Prompt injection score exceeded threshold (heuristic)",
            severity=RiskLevel.HIGH,
            metadata={
                "pattern_type": "scored",
                "score": score,
                "threshold": SCORE_BLOCK_THRESHOLD,
                "matched_patterns": matched,
            },
        )

    meta: dict[str, object] = {}
    if score:
        meta["injection_score"] = score
    return CheckResult(
        check_name="prompt_injection",
        passed=True,
        decision="allow",
        reason="No prompt injection detected",
        metadata=meta,
    )
