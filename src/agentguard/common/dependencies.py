"""FastAPI dependency injection helpers."""

from __future__ import annotations

from fastapi import Depends, Request, Security
from fastapi.security import APIKeyHeader

from agentguard.common.exceptions import AuthenticationError
from agentguard.common.models import RequestContext
from agentguard.config import settings

_api_key_scheme = APIKeyHeader(name=settings.api_key_header, auto_error=False)


async def verify_api_key(api_key: str | None = Security(_api_key_scheme)) -> str:
    """Validate the API key. In development mode, allow empty keys."""
    if settings.app_env == "development":
        return api_key or "dev-key"
    if not api_key:
        raise AuthenticationError("Missing API key")
    return api_key


async def get_request_context(
    request: Request,
    _api_key: str = Depends(verify_api_key),
) -> RequestContext:
    """Build a RequestContext from the current request state."""
    return RequestContext(
        correlation_id=getattr(request.state, "correlation_id", "unknown"),
        tenant_id=getattr(request.state, "tenant_id", settings.default_tenant_id),
        channel="api",
    )
