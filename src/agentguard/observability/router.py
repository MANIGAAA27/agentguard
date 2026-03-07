"""Observability and evaluation API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from agentguard.common.dependencies import get_request_context
from agentguard.common.models import RequestContext
from agentguard.input_guardrails.engine import evaluate_input
from agentguard.observability.audit import get_audit_log
from agentguard.observability.metrics import metrics
from agentguard.observability.schemas import (
    EvalCaseResult,
    EvalRunRequest,
    EvalRunResponse,
)

router = APIRouter(prefix="/v1/evals", tags=["observability"])


@router.post(
    "/run",
    response_model=EvalRunResponse,
    summary="Run an evaluation suite against the guardrails pipeline",
    description=(
        "Executes a set of test cases through the input guardrails engine "
        "and compares actual decisions against expected decisions. "
        "Useful for golden dataset regression testing and red-team evaluation."
    ),
)
async def run_evaluation(
    body: EvalRunRequest,
    ctx: RequestContext = Depends(get_request_context),
) -> EvalRunResponse:
    results: list[EvalCaseResult] = []

    for case in body.cases:
        decision, checks, _ = await evaluate_input(case.input_text)
        passed = decision.value == case.expected_decision
        results.append(
            EvalCaseResult(
                case_id=case.id,
                passed=passed,
                expected=case.expected_decision,
                actual=decision.value,
                details={"checks": [c.model_dump() for c in checks]},
            )
        )
        metrics.increment(
            "eval.case",
            tags={"suite": body.suite_name, "result": "pass" if passed else "fail"},
        )

    passed_count = sum(1 for r in results if r.passed)
    return EvalRunResponse(
        correlation_id=ctx.correlation_id,
        suite_name=body.suite_name,
        total=len(results),
        passed=passed_count,
        failed=len(results) - passed_count,
        results=results,
    )


@router.get("/metrics", summary="Get current metrics snapshot")
async def get_metrics() -> dict[str, int]:
    return metrics.snapshot()


@router.get("/audit", summary="Get recent audit log entries")
async def get_audit(tenant_id: str | None = None, limit: int = 100) -> list[dict]:
    entries = get_audit_log(tenant_id=tenant_id, limit=limit)
    return [e.model_dump() for e in entries]
