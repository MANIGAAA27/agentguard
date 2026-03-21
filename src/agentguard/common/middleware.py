"""FastAPI middleware for correlation IDs and tenant context."""

from __future__ import annotations

from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from agentguard.config import settings

_CORRELATION_HEADER = "X-Correlation-ID"


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Attach or propagate a correlation ID on every request/response."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        correlation_id = request.headers.get(_CORRELATION_HEADER, uuid4().hex)
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers[_CORRELATION_HEADER] = correlation_id
        return response


class TenantContextMiddleware(BaseHTTPMiddleware):
    """Extract tenant ID from header and attach to request state."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        tenant_id = request.headers.get(settings.tenant_header, settings.default_tenant_id)
        request.state.tenant_id = tenant_id
        response = await call_next(request)
        return response
