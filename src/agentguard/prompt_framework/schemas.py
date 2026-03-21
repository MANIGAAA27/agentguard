"""Request/response schemas for the prompt framework."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PromptCompileRequest(BaseModel):
    """POST /v1/prompts/compile"""

    package_name: str = Field(..., description="Name of the prompt package to compile")
    package_version: str | None = Field(None, description="Version; defaults to latest")
    user_message: str = Field(..., description="The user's message")
    tenant_policy: str = Field("", description="Tenant-specific policy overlay")
    retrieved_context: str = Field("", description="Retrieved context for grounding")
    variables: dict[str, str] = Field(default_factory=dict, description="Template variables")


class PromptCompileResponse(BaseModel):
    correlation_id: str
    messages: list[dict[str, str]]
    output_schema: dict[str, Any] | None = None
    tool_definitions: list[dict[str, Any]] = Field(default_factory=list)
    lint_warnings: list[dict[str, str]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
