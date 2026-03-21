"""Policy engine API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from agentguard.common.dependencies import get_request_context
from agentguard.common.models import RequestContext
from agentguard.policy.engine import evaluate_policy
from agentguard.policy.schemas import PolicyEvaluateRequest, PolicyEvaluateResponse

router = APIRouter(prefix="/v1/policies", tags=["policy-engine"])


@router.post(
    "/evaluate",
    response_model=PolicyEvaluateResponse,
    summary="Evaluate request context against a named policy set",
    description=(
        "Loads a policy set by name, evaluates all rules against the provided "
        "context, and returns an aggregate decision (allow/deny/warn/escalate) "
        "with per-rule results."
    ),
)
async def evaluate_policy_endpoint(
    body: PolicyEvaluateRequest,
    ctx: RequestContext = Depends(get_request_context),
) -> PolicyEvaluateResponse:
    decision, rule_results = evaluate_policy(body.policy_name, body.context)
    return PolicyEvaluateResponse(
        correlation_id=ctx.correlation_id,
        decision=decision,
        policy_name=body.policy_name,
        rule_results=rule_results,
    )
