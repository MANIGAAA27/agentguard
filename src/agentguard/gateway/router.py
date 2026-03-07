"""AI Gateway router -- single entry point for all LLM and agent requests."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from agentguard.common.dependencies import get_request_context
from agentguard.common.models import RequestContext
from agentguard.gateway.model_router import get_model_provider
from agentguard.gateway.rate_limiter import check_rate_limit
from agentguard.gateway.tenant import get_tenant_config

router = APIRouter(prefix="/v1/gateway", tags=["gateway"])


class GatewayRequest(BaseModel):
    """Top-level request to the AI Gateway."""

    messages: list[dict[str, str]]
    use_case: str | None = None
    model_provider: str | None = None
    model_name: str | None = None
    stream: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class GatewayResponse(BaseModel):
    correlation_id: str
    tenant_id: str
    model: str
    output: dict[str, Any]


@router.post(
    "/complete",
    response_model=GatewayResponse,
    summary="Send a completion request through the trust layer",
)
async def gateway_complete(
    body: GatewayRequest,
    ctx: RequestContext = Depends(get_request_context),
) -> GatewayResponse:
    """Route a request through auth, tenant isolation, rate limiting, and model abstraction.

    This is the raw gateway endpoint. The full pipeline (guardrails, prompt compile,
    output validation) is wired in the /v1/gateway/pipeline endpoint.
    """
    tenant_cfg = get_tenant_config(ctx.tenant_id)
    check_rate_limit(ctx.tenant_id, tenant_cfg.get("rate_limit_rpm"))

    provider = get_model_provider(
        provider=body.model_provider,
        model=body.model_name,
    )
    result = await provider.complete(body.messages)

    return GatewayResponse(
        correlation_id=ctx.correlation_id,
        tenant_id=ctx.tenant_id,
        model=provider.model,
        output=result,
    )
