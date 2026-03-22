"""AgentGuard FastAPI application entrypoint."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from agentguard.action_governance.router import router as action_router
from agentguard.common.exceptions import AgentGuardError
from agentguard.common.middleware import CorrelationIdMiddleware, TenantContextMiddleware
from agentguard import __version__
from agentguard.config import settings
from agentguard.gateway.router import router as gateway_router
from agentguard.input_guardrails.router import router as input_router
from agentguard.observability.router import router as observability_router
from agentguard.output_validation.router import router as output_router
from agentguard.policy.router import router as policy_router
from agentguard.prompt_framework.router import router as prompt_router
from agentguard.retrieval.router import router as retrieval_router

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    logger.info("agentguard.startup", env=settings.app_env)
    yield
    logger.info("agentguard.shutdown")


app = FastAPI(
    title=settings.app_name,
    description=(
        "Heuristic, auditable LLM guardrails (input/output checks, policies, gateway). "
        "Not a full enterprise safety stack — see README limitations."
    ),
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- Middleware (order matters: outermost first) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TenantContextMiddleware)
app.add_middleware(CorrelationIdMiddleware)


# --- Exception handler ---
@app.exception_handler(AgentGuardError)
async def agentguard_error_handler(_request: Request, exc: AgentGuardError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.code, "message": str(exc)},
    )


# --- Routers ---
app.include_router(gateway_router)
app.include_router(input_router)
app.include_router(prompt_router)
app.include_router(retrieval_router)
app.include_router(output_router)
app.include_router(action_router)
app.include_router(policy_router)
app.include_router(observability_router)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok", "version": "0.1.0"}
