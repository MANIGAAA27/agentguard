"""Optional response headers for guardrail wall-clock timing (issue #9)."""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from agentguard.config import settings


class GuardrailLatencyHeaderMiddleware(BaseHTTPMiddleware):
    """Append ``X-AgentGuard-Latency-Ms`` when endpoints set ``request.state`` timings."""

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        if not settings.expose_guardrail_latency_header:
            return response
        parts: list[str] = []
        st = request.state
        if getattr(st, "agentguard_input_guardrails_ms", None) is not None:
            parts.append(f"input_guardrails={float(st.agentguard_input_guardrails_ms):.3f}")
        if getattr(st, "agentguard_output_validation_ms", None) is not None:
            parts.append(f"output_validation={float(st.agentguard_output_validation_ms):.3f}")
        if parts:
            response.headers["X-AgentGuard-Latency-Ms"] = ";".join(parts)
        return response
