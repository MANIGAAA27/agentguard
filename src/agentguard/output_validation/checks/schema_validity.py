"""Validate LLM output against a JSON schema."""

from __future__ import annotations

import json
from typing import Any

import jsonschema

from agentguard.common.models import CheckResult, RiskLevel


async def check(output_text: str, expected_schema: dict[str, Any] | None) -> CheckResult:
    if not expected_schema:
        return CheckResult(
            check_name="schema_validity",
            passed=True,
            decision="pass",
            reason="No schema to validate against",
        )

    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError as exc:
        return CheckResult(
            check_name="schema_validity",
            passed=False,
            decision="repair",
            reason=f"Output is not valid JSON: {exc}",
            severity=RiskLevel.MEDIUM,
        )

    try:
        jsonschema.validate(parsed, expected_schema)
    except jsonschema.ValidationError as exc:
        return CheckResult(
            check_name="schema_validity",
            passed=False,
            decision="repair",
            reason=f"Schema validation failed: {exc.message}",
            severity=RiskLevel.MEDIUM,
            metadata={"path": list(exc.absolute_path)},
        )

    return CheckResult(
        check_name="schema_validity",
        passed=True,
        decision="pass",
        reason="Output matches expected schema",
    )
