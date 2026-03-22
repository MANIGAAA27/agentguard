"""Model provider abstraction and routing."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

import httpx

from agentguard.config import settings


class ModelProvider:
    """Abstraction over LLM provider APIs."""

    def __init__(self, provider: str, model: str, api_key: str):
        self.provider = provider
        self.model = model
        self.api_key = api_key

    async def complete(self, messages: list[dict[str, str]], **kwargs: Any) -> dict[str, Any]:
        """Send a completion request to the configured provider."""
        if self.provider == "openai":
            return await self._openai_complete(messages, **kwargs)
        if self.provider == "anthropic":
            return await self._anthropic_complete(messages, **kwargs)
        return self._local_stub(messages)

    async def _openai_complete(
        self, messages: list[dict[str, str]], **kwargs: Any
    ) -> dict[str, Any]:
        kwargs = {k: v for k, v in kwargs.items() if k != "stream"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model, "messages": messages, **kwargs},
                timeout=60.0,
            )
            resp.raise_for_status()
            return resp.json()  # type: ignore[no-any-return]

    async def iter_openai_chat_sse(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> AsyncIterator[bytes]:
        """Stream raw OpenAI chat.completions SSE chunks (``data: {...}\\n\\n``)."""
        kwargs = {k: v for k, v in kwargs.items() if k != "stream"}
        body: dict[str, Any] = {"model": self.model, "messages": messages, "stream": True, **kwargs}
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=body,
                timeout=120.0,
            ) as resp:
                resp.raise_for_status()
                async for chunk in resp.aiter_bytes():
                    yield chunk

    async def _anthropic_complete(
        self, messages: list[dict[str, str]], **kwargs: Any
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                },
                json={"model": self.model, "messages": messages, "max_tokens": 4096, **kwargs},
                timeout=60.0,
            )
            resp.raise_for_status()
            return resp.json()  # type: ignore[no-any-return]

    @staticmethod
    def _local_stub(messages: list[dict[str, str]]) -> dict[str, Any]:
        """Stub for local/test model that echoes the last user message."""
        last = messages[-1]["content"] if messages else ""
        return {
            "choices": [{"message": {"role": "assistant", "content": f"[stub] {last}"}}],
            "model": "local-stub",
        }


def get_model_provider(
    provider: str | None = None,
    model: str | None = None,
) -> ModelProvider:
    """Factory for model providers based on config or overrides."""
    p = provider or settings.default_model_provider
    m = model or settings.default_model_name
    key_map = {
        "openai": settings.openai_api_key,
        "anthropic": settings.anthropic_api_key,
        "local": "",
    }
    return ModelProvider(provider=p, model=m, api_key=key_map.get(p, ""))
