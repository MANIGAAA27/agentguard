"""Request/response schemas for retrieval grounding."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Citation(BaseModel):
    source_id: str
    title: str
    content: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    url: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class RetrievalSearchRequest(BaseModel):
    """POST /v1/retrieval/search"""

    query: str = Field(..., description="Search query")
    collection: str = Field("default", description="Document collection to search")
    top_k: int = Field(5, ge=1, le=50)
    min_confidence: float = Field(0.3, ge=0.0, le=1.0)
    require_grounding: bool = Field(True, description="Block answer if no evidence found")
    metadata: dict[str, Any] = Field(default_factory=dict)


class RetrievalSearchResponse(BaseModel):
    correlation_id: str
    citations: list[Citation]
    grounded: bool
    context_text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
