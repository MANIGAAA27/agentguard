"""Minimal FastAPI app embedding AgentGuard's gateway (in-process).

Run from the repository root::

    cp .env.example .env   # set OPENAI_API_KEY for real OpenAI calls
    export PYTHONPATH=src
    uvicorn examples.minimal_gateway_openai:app --host 0.0.0.0 --port 8000

Then::

    curl -s http://localhost:8000/v1/gateway/complete \\
      -H "Content-Type: application/json" \\
      -d '{"messages":[{"role":"user","content":"Say hello in five words."}],"model_provider":"local"}'

Omit ``model_provider`` (or set ``openai``) when ``OPENAI_API_KEY`` is set in the environment.
"""

from __future__ import annotations

from fastapi import FastAPI

from agentguard.integrations import include_gateway_router, register_agentguard_middleware

app = FastAPI(
    title="AgentGuard minimal gateway",
    description="Embeds POST /v1/gateway/complete without running a separate sidecar.",
)
register_agentguard_middleware(app)
include_gateway_router(app)
