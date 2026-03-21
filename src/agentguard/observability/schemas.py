"""Request/response schemas for observability and evaluation."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class EvalCase(BaseModel):
    """A single evaluation test case."""

    id: str
    input_text: str
    expected_decision: str
    context: dict[str, Any] = Field(default_factory=dict)


class EvalRunRequest(BaseModel):
    """POST /v1/evals/run"""

    suite_name: str = Field(..., description="Name of the evaluation suite")
    cases: list[EvalCase] = Field(..., description="Test cases to evaluate")


class EvalCaseResult(BaseModel):
    case_id: str
    passed: bool
    expected: str
    actual: str
    details: dict[str, Any] = Field(default_factory=dict)


class EvalRunResponse(BaseModel):
    correlation_id: str
    suite_name: str
    total: int
    passed: int
    failed: int
    results: list[EvalCaseResult]
