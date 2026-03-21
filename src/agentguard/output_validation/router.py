"""Output validation API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from agentguard.common.dependencies import get_request_context
from agentguard.common.models import RequestContext
from agentguard.output_validation.engine import validate_output
from agentguard.output_validation.schemas import OutputValidationRequest, OutputValidationResponse

router = APIRouter(prefix="/v1/outputs", tags=["output-validation"])


@router.post(
    "/validate",
    response_model=OutputValidationResponse,
    summary="Validate LLM output for safety, accuracy, and quality",
    description=(
        "Runs 7 parallel checks: JSON schema validity, citation presence, "
        "hallucination proxy, policy violations, unsafe language, confidence "
        "threshold, and genericity detection. Returns an aggregate decision "
        "(pass/repair/reject/escalate)."
    ),
)
async def validate_output_endpoint(
    body: OutputValidationRequest,
    ctx: RequestContext = Depends(get_request_context),
) -> OutputValidationResponse:
    decision, checks = await validate_output(
        body.output_text,
        context_text=body.context_text,
        expected_schema=body.expected_schema,
        require_citations=body.require_citations,
        min_confidence=body.min_confidence,
    )
    return OutputValidationResponse(
        correlation_id=ctx.correlation_id,
        decision=decision,
        checks=checks,
    )
