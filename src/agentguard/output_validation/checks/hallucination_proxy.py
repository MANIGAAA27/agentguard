"""Heuristic checks for unsupported LLM output relative to context.

**Not** full hallucination detection. This module combines:

1. **Numeric / date / percent literals** — if the output contains dates, currency, or
   percentages that do not appear in the context, flag (narrow literal matching).
2. **Bigram overlap** — for longer outputs against substantial context, very low
   shared bigram overlap suggests the model may be producing narrative unrelated to
   the provided context (still a heuristic; paraphrase and jargon can cause false
   positives/negatives).

Fabricated prose with no dates or numbers, or creative toxicity without literals,
may still pass. See README *Output Validation* warnings.
"""

from __future__ import annotations

import re
from collections import Counter

from agentguard.common.models import CheckResult, RiskLevel

_SPECIFIC_CLAIM_PATTERN = re.compile(
    r"\b(?:\d{4}[-/]\d{2}[-/]\d{2}|\$[\d,.]+|\d+(?:\.\d+)?%)\b"
)

_TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)

# Minimum words to run overlap heuristic
_MIN_OUTPUT_WORDS = 25
_MIN_CONTEXT_WORDS = 40
# Below this Jaccard on bigram sets → flag (tune with care)
_OVERLAP_FAIL_JACCARD = 0.06


def _word_tokens(s: str) -> list[str]:
    return _TOKEN_RE.findall(s.lower())


def _bigrams(words: list[str]) -> list[tuple[str, str]]:
    if len(words) < 2:
        return []
    return list(zip(words, words[1:], strict=False))


def _bigram_jaccard(output_text: str, context_text: str) -> float | None:
    """Return Jaccard similarity of bigram multisets, or None if check skipped."""
    cw = _word_tokens(context_text)
    ow = _word_tokens(output_text)
    if len(cw) < _MIN_CONTEXT_WORDS or len(ow) < _MIN_OUTPUT_WORDS:
        return None

    cb = _bigrams(cw)
    ob = _bigrams(ow)
    if not cb or not ob:
        return None

    c_count = Counter(cb)
    o_count = Counter(ob)
    intersection = sum((c_count & o_count).values())
    union = sum((c_count | o_count).values())
    if union == 0:
        return None
    return intersection / union


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
    numeric_fail = bool(unsupported)
    jaccard = _bigram_jaccard(output_text, context_text)
    overlap_fail = jaccard is not None and jaccard < _OVERLAP_FAIL_JACCARD

    if numeric_fail and overlap_fail:
        ratio = len(unsupported) / max(len(output_claims), 1)
        severity = RiskLevel.HIGH if ratio > 0.5 else RiskLevel.MEDIUM
        return CheckResult(
            check_name="hallucination_proxy",
            passed=False,
            decision="reject" if ratio > 0.5 else "repair",
            reason="Unsupported literals and low context bigram overlap",
            severity=severity,
            metadata={
                "unsupported_claims": list(unsupported),
                "ratio": round(ratio, 3),
                "bigram_jaccard": round(jaccard, 4) if jaccard is not None else None,
            },
        )

    if numeric_fail:
        ratio = len(unsupported) / max(len(output_claims), 1)
        severity = RiskLevel.HIGH if ratio > 0.5 else RiskLevel.MEDIUM
        return CheckResult(
            check_name="hallucination_proxy",
            passed=False,
            decision="repair" if ratio <= 0.5 else "reject",
            reason=f"Unsupported literals vs context: {unsupported}",
            severity=severity,
            metadata={"unsupported_claims": list(unsupported), "ratio": round(ratio, 3)},
        )

    if overlap_fail:
        return CheckResult(
            check_name="hallucination_proxy",
            passed=False,
            decision="repair",
            reason="Very low bigram overlap with context (heuristic; possible unsupported narrative)",
            severity=RiskLevel.MEDIUM,
            metadata={"bigram_jaccard": round(jaccard, 4) if jaccard is not None else None},
        )

    meta: dict[str, object] = {}
    if jaccard is not None:
        meta["bigram_jaccard"] = round(jaccard, 4)
    return CheckResult(
        check_name="hallucination_proxy",
        passed=True,
        decision="pass",
        reason="Heuristic checks passed (see module docstring for limits)",
        metadata=meta,
    )
