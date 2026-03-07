"""Retrieval grounding API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from agentguard.common.dependencies import get_request_context
from agentguard.common.models import RequestContext
from agentguard.retrieval.grounding import package_context, search_documents
from agentguard.retrieval.rewriter import rewrite_query
from agentguard.retrieval.schemas import RetrievalSearchRequest, RetrievalSearchResponse

router = APIRouter(prefix="/v1/retrieval", tags=["retrieval-grounding"])


@router.post(
    "/search",
    response_model=RetrievalSearchResponse,
    summary="Search for grounding context with citation packaging",
    description=(
        "Rewrites the query for safety, searches the document store, "
        "scores source confidence, and packages citations. "
        "When require_grounding is true, the grounded flag indicates "
        "whether sufficient evidence was found."
    ),
)
async def retrieval_search(
    body: RetrievalSearchRequest,
    ctx: RequestContext = Depends(get_request_context),
) -> RetrievalSearchResponse:
    cleaned_query, _ = rewrite_query(body.query)
    citations = search_documents(
        cleaned_query,
        collection=body.collection,
        top_k=body.top_k,
        min_confidence=body.min_confidence,
    )
    context_text = package_context(citations)
    grounded = len(citations) > 0

    return RetrievalSearchResponse(
        correlation_id=ctx.correlation_id,
        citations=citations,
        grounded=grounded,
        context_text=context_text,
    )
