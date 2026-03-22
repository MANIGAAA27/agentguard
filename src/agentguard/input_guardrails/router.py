"""Input guardrails API router."""

from __future__ import annotations

import time

import structlog
from fastapi import APIRouter, Depends, Request

from agentguard.common.dependencies import get_request_context
from agentguard.config import settings
from agentguard.common.models import RequestContext
from agentguard.input_guardrails.engine import evaluate_input
from agentguard.input_guardrails.schemas import InputEvaluationRequest, InputEvaluationResponse

router = APIRouter(prefix="/v1/guardrails", tags=["input-guardrails"])
logger = structlog.get_logger()


@router.post(
    "/evaluate-input",
    response_model=InputEvaluationResponse,
    summary="Evaluate user input for safety, policy compliance, and data protection",
    description=(
        "Runs 7 parallel checks: prompt injection, jailbreak, toxicity, "
        "PII detection, secret detection, restricted topics, and data exfiltration. "
        "Returns an aggregate decision (allow/redact/block/escalate/safe-complete-only)."
    ),
)
async def evaluate_input_endpoint(
    request: Request,
    body: InputEvaluationRequest,
    ctx: RequestContext = Depends(get_request_context),
) -> InputEvaluationResponse:
    t0 = time.perf_counter()
    decision, checks, redacted = await evaluate_input(body.text)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    request.state.agentguard_input_guardrails_ms = elapsed_ms
    if settings.enable_guardrail_timing_logs:
        logger.info(
            "input_guardrails.timing",
            duration_ms=round(elapsed_ms, 3),
            correlation_id=ctx.correlation_id,
        )
    return InputEvaluationResponse(
        correlation_id=ctx.correlation_id,
        decision=decision,
        checks=checks,
        redacted_text=redacted,
    )
