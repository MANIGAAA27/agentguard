# Guardrail latency (benchmarks & instrumentation)

Input and output checks run **in parallel** (`asyncio.gather`); wall-clock cost is
roughly **the slowest check**, not the sum of all seven.

## Reproduce locally

From the repo root:

```bash
python scripts/bench_guardrails.py
python scripts/bench_guardrails.py -n 80
```

Reported times are **ms per call** on your CPU — use for before/after comparisons,
not universal SLA numbers.

## HTTP instrumentation (optional)

| Env | Effect |
|-----|--------|
| `ENABLE_GUARDRAIL_TIMING_LOGS=true` | `structlog` event `input_guardrails.timing` / `output_validation.timing` with `duration_ms` |
| `EXPOSE_GUARDRAIL_LATENCY_HEADER=true` | Response header `X-AgentGuard-Latency-Ms` on routes that ran those engines (e.g. `input_guardrails=2.100`) |

## Source

[DEV — Conway Research](https://dev.to/conwayresearch/comment/35p1m) · GitHub [#9](https://github.com/MANIGAAA27/agentguard/issues/9).
