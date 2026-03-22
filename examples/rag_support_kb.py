#!/usr/bin/env python3
"""Customer-support style flow: input guardrails → demo KB retrieval → gateway completion.

Prerequisites: AgentGuard API running (e.g. ``uvicorn agentguard.main:app`` on port 8000).

Run::

    export AGENTGUARD_URL=http://127.0.0.1:8000
    python examples/rag_support_kb.py

Uses the in-repo demo documents (refund policy, etc.) via ``POST /v1/retrieval/search``.
Set ``OPENAI_API_KEY`` on the server and drop ``model_provider`` below to use a real model.
"""

from __future__ import annotations

import asyncio
import os
import sys

import httpx

DEFAULT_BASE = "http://127.0.0.1:8000"


async def run(base_url: str, question: str) -> None:
    async with httpx.AsyncClient(base_url=base_url.rstrip("/"), timeout=60.0) as client:
        ev = await client.post("/v1/guardrails/evaluate-input", json={"text": question})
        ev.raise_for_status()
        inp = ev.json()
        print("input_guardrails:", inp["decision"])
        if inp["decision"] != "allow":
            print("Stopped: input not allowed.")
            sys.exit(1)

        ret = await client.post(
            "/v1/retrieval/search",
            json={
                "query": question,
                "collection": "default",
                "top_k": 3,
                "min_confidence": 0.2,
                "require_grounding": True,
            },
        )
        ret.raise_for_status()
        grounding = ret.json()
        print("retrieval grounded:", grounding["grounded"], "citations:", len(grounding["citations"]))
        ctx = grounding["context_text"] or "(no KB hits — still calling gateway for demo)"

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a support assistant. Answer using only the context below. "
                    "If context is insufficient, say you do not have that information.\n\n"
                    + ctx
                ),
            },
            {"role": "user", "content": question},
        ]
        gw = await client.post(
            "/v1/gateway/complete",
            json={
                "messages": messages,
                "model_provider": "local",
                "metadata": {"example": "rag_support_kb"},
            },
        )
        gw.raise_for_status()
        out = gw.json()
        print("gateway model:", out["model"])
        choices = out["output"].get("choices") or []
        if choices:
            print("assistant:", choices[0].get("message", {}).get("content"))
        else:
            print("raw output keys:", list(out["output"].keys()))


def main() -> None:
    base = os.environ.get("AGENTGUARD_URL", DEFAULT_BASE)
    question = os.environ.get(
        "SUPPORT_QUESTION",
        "What is your refund policy?",
    )
    asyncio.run(run(base, question))


if __name__ == "__main__":
    main()
