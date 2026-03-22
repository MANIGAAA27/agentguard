"""In-process FastAPI integration: middleware + optional input guardrail dependency.

Use this when AgentGuard runs **inside** your app instead of as a separate HTTP service.
For the full REST surface, use :mod:`agentguard.main` or mount routers selectively.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Body, FastAPI, HTTPException

from agentguard.common.middleware import CorrelationIdMiddleware, TenantContextMiddleware
from agentguard.common.models import InputDecision
from agentguard.gateway.router import router as gateway_router
from agentguard.input_guardrails import engine as input_engine


def register_agentguard_middleware(app: FastAPI) -> None:
    """Register correlation + tenant middleware required by gateway dependencies.

    Call **before** routes that use ``include_gateway_router`` or
    ``get_request_context``. Matches the middleware stack expected by the gateway.
    """
    app.add_middleware(TenantContextMiddleware)
    app.add_middleware(CorrelationIdMiddleware)


def include_gateway_router(app: FastAPI) -> None:
    """Mount ``POST /v1/gateway/complete`` on your FastAPI app.

    Call :func:`register_agentguard_middleware` first. In non-development
    ``APP_ENV``, configure API key auth as documented for
    :func:`agentguard.common.dependencies.get_request_context`.
    """
    app.include_router(gateway_router)


async def guardrailed_user_text(
    text: Annotated[str, Body(..., description="User content evaluated by input guardrails")],
) -> str:
    """FastAPI dependency: returns ``text`` (or redacted form) only if decision is **allow**.

    Example::

        @app.post("/echo")
        async def echo(safe: Annotated[str, Depends(guardrailed_user_text)]):
            return {"ok": safe}

    Request body: ``{"text": "..."}``.
    """
    decision, checks, redacted = await input_engine.evaluate_input(text)
    if decision != InputDecision.ALLOW:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "input_guardrails_failed",
                "decision": decision.value,
                "checks": [c.model_dump() for c in checks],
                "redacted_text": redacted,
            },
        )
    return redacted if redacted is not None else text
