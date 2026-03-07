"""Custom exception classes for AgentGuard."""

from __future__ import annotations


class AgentGuardError(Exception):
    """Base exception for all AgentGuard errors."""

    def __init__(self, message: str, *, code: str = "INTERNAL_ERROR", status_code: int = 500):
        super().__init__(message)
        self.code = code
        self.status_code = status_code


class AuthenticationError(AgentGuardError):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="AUTH_ERROR", status_code=401)


class AuthorizationError(AgentGuardError):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, code="AUTHZ_ERROR", status_code=403)


class RateLimitExceeded(AgentGuardError):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, code="RATE_LIMIT", status_code=429)


class TenantNotFound(AgentGuardError):
    def __init__(self, tenant_id: str):
        super().__init__(f"Tenant not found: {tenant_id}", code="TENANT_NOT_FOUND", status_code=404)


class PolicyViolation(AgentGuardError):
    def __init__(self, message: str, *, policy_id: str = "unknown"):
        super().__init__(message, code="POLICY_VIOLATION", status_code=403)
        self.policy_id = policy_id


class InputBlocked(AgentGuardError):
    def __init__(self, message: str, *, check_name: str = "unknown"):
        super().__init__(message, code="INPUT_BLOCKED", status_code=400)
        self.check_name = check_name


class OutputRejected(AgentGuardError):
    def __init__(self, message: str):
        super().__init__(message, code="OUTPUT_REJECTED", status_code=422)


class ActionDenied(AgentGuardError):
    def __init__(self, message: str, *, action: str = "unknown"):
        super().__init__(message, code="ACTION_DENIED", status_code=403)
        self.action = action
