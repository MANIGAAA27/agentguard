"""Citation packaging and source confidence scoring."""

from __future__ import annotations

from agentguard.retrieval.schemas import Citation

# MVP: in-memory document store for demonstration.
_DEMO_DOCUMENTS: list[dict] = [
    {
        "source_id": "doc-001",
        "title": "Company Refund Policy",
        "content": "Refunds are available within 30 days of purchase with a valid receipt.",
        "url": "https://docs.example.com/refund-policy",
    },
    {
        "source_id": "doc-002",
        "title": "Data Retention Guidelines",
        "content": "Customer data is retained for 7 years per regulatory requirements.",
        "url": "https://docs.example.com/data-retention",
    },
    {
        "source_id": "doc-003",
        "title": "AI Usage Policy",
        "content": "AI-generated responses must be grounded in verified company data.",
        "url": "https://docs.example.com/ai-policy",
    },
]


def search_documents(
    query: str,
    collection: str = "default",
    top_k: int = 5,
    min_confidence: float = 0.3,
) -> list[Citation]:
    """Search for relevant documents. MVP uses keyword matching with simple scoring."""
    query_terms = set(query.lower().split())
    scored: list[tuple[float, dict]] = []

    for doc in _DEMO_DOCUMENTS:
        doc_terms = set(doc["content"].lower().split()) | set(doc["title"].lower().split())
        overlap = query_terms & doc_terms
        if overlap:
            confidence = min(len(overlap) / max(len(query_terms), 1), 1.0)
            if confidence >= min_confidence:
                scored.append((confidence, doc))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [
        Citation(
            source_id=doc["source_id"],
            title=doc["title"],
            content=doc["content"],
            confidence=round(conf, 3),
            url=doc.get("url"),
        )
        for conf, doc in scored[:top_k]
    ]


def package_context(citations: list[Citation]) -> str:
    """Package citations into a context string for prompt injection."""
    if not citations:
        return ""
    parts = []
    for i, c in enumerate(citations, 1):
        parts.append(f"[{i}] {c.title} (confidence: {c.confidence})\n{c.content}")
    return "\n\n".join(parts)
