"""Unit tests for output validation checks."""

from __future__ import annotations

import pytest

from agentguard.output_validation.checks import (
    citation_check,
    confidence_threshold,
    genericity_detector,
    hallucination_proxy,
    policy_check,
    schema_validity,
    unsafe_language,
)


@pytest.mark.asyncio
async def test_schema_valid_json():
    schema = {"type": "object", "properties": {"answer": {"type": "string"}}, "required": ["answer"]}
    result = await schema_validity.check('{"answer": "hello"}', schema)
    assert result.passed


@pytest.mark.asyncio
async def test_schema_invalid_json():
    result = await schema_validity.check("not json", {"type": "object"})
    assert not result.passed
    assert result.decision == "repair"


@pytest.mark.asyncio
async def test_schema_no_schema():
    result = await schema_validity.check("anything", None)
    assert result.passed


@pytest.mark.asyncio
async def test_citation_required_present():
    result = await citation_check.check("The answer is X [1].", require_citations=True)
    assert result.passed


@pytest.mark.asyncio
async def test_citation_required_missing():
    result = await citation_check.check("The answer is X.", require_citations=True)
    assert not result.passed


@pytest.mark.asyncio
async def test_hallucination_no_context():
    result = await hallucination_proxy.check("Some output with $100", "")
    assert result.passed


@pytest.mark.asyncio
async def test_hallucination_supported():
    result = await hallucination_proxy.check("The cost is $100", "The cost is $100")
    assert result.passed


@pytest.mark.asyncio
async def test_hallucination_unsupported():
    result = await hallucination_proxy.check("The cost is $999 on 2024-01-01", "The cost is $100")
    assert not result.passed


@pytest.mark.asyncio
async def test_hallucination_low_bigram_overlap_flags():
    """Long output with different vocabulary than long context → overlap heuristic."""
    context = (
        " ".join(
            [
                "refund policy states thirty day window receipt required",
                "electronics category separate restocking fee applies",
                "customer must initiate portal ticket before return label",
            ]
            * 8
        )
    )
    output = (
        " ".join(
            [
                "quantum mechanics describes particle behavior probabilities",
                "wave function collapse measurement problem interpretation",
                "entanglement nonlocality bell experiments verification",
            ]
            * 8
        )
    )
    result = await hallucination_proxy.check(output, context)
    assert not result.passed
    assert "overlap" in result.reason.lower()


@pytest.mark.asyncio
async def test_policy_check_clean():
    result = await policy_check.check("Here is the refund policy information.")
    assert result.passed


@pytest.mark.asyncio
async def test_unsafe_language_clean():
    result = await unsafe_language.check("The product ships in 3-5 business days.")
    assert result.passed


@pytest.mark.asyncio
async def test_confidence_high():
    result = await confidence_threshold.check("The answer is definitively 42.", 0.5)
    assert result.passed


@pytest.mark.asyncio
async def test_genericity_clean():
    result = await genericity_detector.check("The refund window is 30 days with valid receipt.")
    assert result.passed


@pytest.mark.asyncio
async def test_genericity_detected():
    text = (
        "In today's fast-paced world, it's important to note that "
        "there are many factors to consider. Generally speaking, "
        "there are pros and cons to everything."
    )
    result = await genericity_detector.check(text)
    assert not result.passed
    assert result.decision == "repair"
