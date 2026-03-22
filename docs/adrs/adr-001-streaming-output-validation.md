# ADR-001: Streaming completions vs output validation

## Status

Accepted (implemented for **OpenAI** `stream=true` on `POST /v1/gateway/complete`).

## Context

- Output validation and `quality_risk_score` are defined over **full assistant text**.
- Users want **SSE streaming** for latency perception and UX.
- The gateway previously accepted `stream` on the request body but did not proxy streams.

## Decision

1. When `stream=true` and `model_provider` resolves to **openai**, the gateway returns **`text/event-stream`** and **proxies** OpenAI chat completion SSE bytes end-to-end.
2. **No** automatic output validation runs on that path inside the same HTTP response.
3. Callers that need guardrails on the final answer should **buffer** the assistant message client-side (or on a worker), then call **`POST /v1/outputs/validate`** (optionally with `include_quality_risk_score=true`).

## Alternatives considered

- **Buffer server-side, validate, then stream** — simpler for guarantees, higher TTFB; deferred.
- **Per-chunk heuristics** — weaker semantics; document separately if added later.

## Consequences

- Anthropic and `local` providers return **400** with `streaming_not_supported` when `stream=true`.
- Operators must ensure **`OPENAI_API_KEY`** is set for streaming.

## Source

Community question: [DEV — Conway Research](https://dev.to/conwayresearch/comment/35p1m) · GitHub [#10](https://github.com/MANIGAAA27/agentguard/issues/10).
