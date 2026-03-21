"""Action governance API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from agentguard.action_governance.allowlist import is_tool_allowed, validate_parameters
from agentguard.action_governance.approval import check_idempotency, requires_approval
from agentguard.action_governance.risk_scorer import score_action
from agentguard.action_governance.schemas import ActionAuthorizeRequest, ActionAuthorizeResponse
from agentguard.common.dependencies import get_request_context
from agentguard.common.models import ActionDecision, RequestContext, RiskLevel

router = APIRouter(prefix="/v1/actions", tags=["action-governance"])


@router.post(
    "/authorize",
    response_model=ActionAuthorizeResponse,
    summary="Authorize an agent action through risk scoring and policy checks",
    description=(
        "Validates the tool against an allowlist, checks parameters, computes "
        "a risk score, and determines whether the action is allowed, requires "
        "approval, or is denied. Supports dry-run mode and idempotency keys."
    ),
)
async def authorize_action(
    body: ActionAuthorizeRequest,
    ctx: RequestContext = Depends(get_request_context),
) -> ActionAuthorizeResponse:
    if check_idempotency(body.idempotency_key):
        return ActionAuthorizeResponse(
            correlation_id=ctx.correlation_id,
            decision=ActionDecision.DENY,
            risk_level=RiskLevel.LOW,
            risk_score=0.0,
            reason="Duplicate request (idempotency key already seen)",
        )

    if not is_tool_allowed(body.tool):
        return ActionAuthorizeResponse(
            correlation_id=ctx.correlation_id,
            decision=ActionDecision.DENY,
            risk_level=RiskLevel.CRITICAL,
            risk_score=1.0,
            reason=f"Tool '{body.tool}' is not in the allowlist",
        )

    param_errors = validate_parameters(body.tool, body.parameters)
    if param_errors:
        return ActionAuthorizeResponse(
            correlation_id=ctx.correlation_id,
            decision=ActionDecision.DENY,
            risk_level=RiskLevel.MEDIUM,
            risk_score=0.5,
            reason=f"Parameter validation failed: {'; '.join(param_errors)}",
        )

    risk_score, risk_level = score_action(body.action, body.tool, body.parameters)

    if body.dry_run:
        return ActionAuthorizeResponse(
            correlation_id=ctx.correlation_id,
            decision=ActionDecision.DRY_RUN,
            risk_level=risk_level,
            risk_score=risk_score,
            reason="Dry-run mode: action evaluated but not executed",
            dry_run=True,
        )

    needs_approval = requires_approval(risk_level)
    if needs_approval:
        decision = ActionDecision.REQUIRE_APPROVAL
        reason = f"Action requires human approval (risk: {risk_level.value})"
    elif risk_level == RiskLevel.CRITICAL:
        decision = ActionDecision.DENY
        reason = "Action denied: critical risk level"
    else:
        decision = ActionDecision.ALLOW
        reason = "Action authorized"

    return ActionAuthorizeResponse(
        correlation_id=ctx.correlation_id,
        decision=decision,
        risk_level=risk_level,
        risk_score=risk_score,
        reason=reason,
        requires_approval=needs_approval,
    )
