#!/usr/bin/env python3
"""Agent action governance: allow low-risk tools; high-risk path returns **require-approval** (HITL).

Prerequisites: AgentGuard API running on ``AGENTGUARD_URL`` (default ``http://127.0.0.1:8000``).

Run::

    python examples/agent_with_hitl.py

This does **not** execute side effects — it shows how your agent runtime should call
``POST /v1/actions/authorize`` and branch on ``decision`` before calling a real tool API.
"""

from __future__ import annotations

import asyncio
import os
import uuid

import httpx

DEFAULT_BASE = "http://127.0.0.1:8000"


async def authorize(
    client: httpx.AsyncClient,
    *,
    action: str,
    tool: str,
    parameters: dict,
    dry_run: bool = False,
    idempotency_key: str | None = None,
) -> dict:
    r = await client.post(
        "/v1/actions/authorize",
        json={
            "action": action,
            "tool": tool,
            "parameters": parameters,
            "dry_run": dry_run,
            "idempotency_key": idempotency_key,
        },
    )
    r.raise_for_status()
    return r.json()


async def run(base_url: str) -> None:
    async with httpx.AsyncClient(base_url=base_url.rstrip("/"), timeout=30.0) as client:
        low = await authorize(
            client,
            action="answer_from_kb",
            tool="search_documents",
            parameters={"query": "refund policy"},
            dry_run=False,
            idempotency_key=f"demo-search-{uuid.uuid4()}",
        )
        print("1) Low-risk search_documents:", low["decision"], "|", low["reason"])

        dry = await authorize(
            client,
            action="refund_approval",
            tool="refund_approval",
            parameters={"order_id": "ord-123", "amount": 499.0},
            dry_run=True,
        )
        print("2) Dry-run refund:", dry["decision"], "|", dry["reason"])

        key = f"demo-refund-{uuid.uuid4()}"
        hitl = await authorize(
            client,
            action="refund_approval",
            tool="refund_approval",
            parameters={"order_id": "ord-123", "amount": 499.0},
            dry_run=False,
            idempotency_key=key,
        )
        print("3) Refund authorize:", hitl["decision"], "| risk:", hitl["risk_level"])
        print("   requires_approval:", hitl.get("requires_approval"), "|", hitl["reason"])
        if hitl["decision"] == "require-approval":
            print(
                "   → HITL: pause here; after human approves, your worker executes the refund "
                "and should use a new idempotency key for a different attempt."
            )


def main() -> None:
    base = os.environ.get("AGENTGUARD_URL", DEFAULT_BASE)
    asyncio.run(run(base))


if __name__ == "__main__":
    main()
