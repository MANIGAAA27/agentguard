"""AI Gateway router -- single entry point for all LLM and agent requests."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from agentguard.common.dependencies import get_request_context
from agentguard.common.models import RequestContext
from agentguard.config import settings
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
    stream: bool = Field(
        False,
        description=(
            "If true, response is OpenAI text/event-stream (SSE) when model_provider is openai. "
            "Run output validation separately after the stream completes (see ADR-001)."
        ),
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


class GatewayResponse(BaseModel):
    correlation_id: str
    tenant_id: str
    model: str
    output: dict[str, Any]


@router.post(
    "/complete",
    response_model=None,
    summary="Send a completion request through the trust layer",
)
async def gateway_complete(
    body: GatewayRequest,
    ctx: RequestContext = Depends(get_request_context),
):
    """Route a request through auth, tenant isolation, rate limiting, and model abstraction.

    When ``stream=true`` and provider is **OpenAI**, returns **SSE** passthrough. Aggregate
    output validation and ``quality_risk_score`` still require the **full** assistant text —
    call ``POST /v1/outputs/validate`` (or your own checks) after reassembling the stream
    client-side. See ``docs/adrs/adr-001-streaming-output-validation.md``.
    """
    tenant_cfg = get_tenant_config(ctx.tenant_id)
    check_rate_limit(ctx.tenant_id, tenant_cfg.get("rate_limit_rpm"))

    provider = get_model_provider(
        provider=body.model_provider,
        model=body.model_name,
    )

    if body.stream:
        if provider.provider != "openai":
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "streaming_not_supported",
                    "provider": provider.provider,
                    "message": "stream=true is only supported when routing to OpenAI.",
                },
            )
        if not settings.openai_api_key:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "missing_openai_api_key",
                    "message": "OPENAI_API_KEY is required for streaming completions.",
                },
            )
        return StreamingResponse(
            provider.iter_openai_chat_sse(body.messages),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
                "X-Correlation-Id": ctx.correlation_id,
            },
        )

    result = await provider.complete(body.messages)

    return GatewayResponse(
        correlation_id=ctx.correlation_id,
        tenant_id=ctx.tenant_id,
        model=provider.model,
        output=result,
    )
