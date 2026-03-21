"""Authentication and authorization utilities."""

from __future__ import annotations

from jose import JWTError, jwt

from agentguard.common.exceptions import AuthenticationError
from agentguard.config import settings


def decode_jwt(token: str) -> dict:
    """Decode and validate a JWT token. Returns the payload dict."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload  # type: ignore[return-value]
    except JWTError as exc:
        raise AuthenticationError(f"Invalid token: {exc}") from exc


def validate_api_key(api_key: str) -> bool:
    """Validate an API key against known keys.

    MVP: accepts any non-empty key in development mode.
    Production should look up keys in a store.
    """
    if settings.app_env == "development":
        return bool(api_key)
    # TODO: look up in key store
    return bool(api_key)
