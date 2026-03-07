"""Integration tests for the output validation engine."""

from __future__ import annotations

import pytest

from agentguard.output_validation.engine import validate_output


@pytest.mark.asyncio
async def test_clean_output_passes():
    decision, checks = await validate_output("The refund policy allows returns within 30 days.")
    assert decision.value == "pass"


@pytest.mark.asyncio
async def test_generic_output_repairs():
    text = (
        "In today's fast-paced world, it's important to note that "
        "there are many factors to consider. Generally speaking, "
        "there are pros and cons to everything. At the end of the day, "
        "it's a complex topic."
    )
    decision, checks = await validate_output(text)
    assert decision.value == "repair"
