"""Output validation API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from agentguard.common.dependencies import get_request_context
from agentguard.common.models import RequestContext
from agentguard.output_validation.engine import validate_output
from agentguard.output_validation.schemas import OutputValidationRequest, OutputValidationResponse
from agentguard.slop_score.scorer import compute_slop_score

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
    meta = dict(body.metadata)
    if body.include_quality_risk_score:
        grounded = bool(body.context_text and body.context_text.strip())
        schema_chk = next((c for c in checks if c.check_name == "schema_validity"), None)
        schema_valid = (
            bool(schema_chk and schema_chk.passed) if body.expected_schema is not None else True
        )
        slop = compute_slop_score(
            list(checks),
            grounded=grounded,
            schema_valid=schema_valid,
            action_risk=0.0,
        )
        meta["quality_risk_score"] = slop.quality_risk_score
        meta["quality_risk_decision"] = slop.decision

    return OutputValidationResponse(
        correlation_id=ctx.correlation_id,
        decision=decision,
        checks=checks,
        metadata=meta,
    )
