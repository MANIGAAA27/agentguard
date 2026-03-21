"""Input guardrails API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from agentguard.common.dependencies import get_request_context
from agentguard.common.models import RequestContext
from agentguard.input_guardrails.engine import evaluate_input
from agentguard.input_guardrails.schemas import InputEvaluationRequest, InputEvaluationResponse

router = APIRouter(prefix="/v1/guardrails", tags=["input-guardrails"])


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
    body: InputEvaluationRequest,
    ctx: RequestContext = Depends(get_request_context),
) -> InputEvaluationResponse:
    decision, checks, redacted = await evaluate_input(body.text)
    return InputEvaluationResponse(
        correlation_id=ctx.correlation_id,
        decision=decision,
        checks=checks,
        redacted_text=redacted,
    )
