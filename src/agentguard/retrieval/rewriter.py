"""Query rewriting with safety controls."""

from __future__ import annotations

import re

_UNSAFE_QUERY_PATTERNS = [
    re.compile(r"ignore\s+(?:all\s+)?(?:previous|safety)", re.IGNORECASE),
    re.compile(r"(?:delete|drop|truncate)\s+", re.IGNORECASE),
]


def rewrite_query(query: str) -> tuple[str, bool]:
    """Rewrite a query for retrieval, stripping unsafe patterns.

    Returns (rewritten_query, was_modified).
    """
    cleaned = query.strip()
    modified = False

    for pattern in _UNSAFE_QUERY_PATTERNS:
        if pattern.search(cleaned):
            cleaned = pattern.sub("", cleaned).strip()
            modified = True

    return cleaned, modified
