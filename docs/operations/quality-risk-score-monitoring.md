# Monitoring `quality_risk_score` (thresholds & drift)

The composite **quality risk** score (JSON field `quality_risk_score`, internal module `slop_score`) summarizes heuristic output checks in **one number** from **0** (low risk) to **1** (high risk), plus a **`decision`**: `pass` | `repair` | `reject`.

Use it to:

- **Gate** responses (same thresholds as config: `SLOP_SCORE_THRESHOLD_PASS`, `SLOP_SCORE_THRESHOLD_REPAIR`)
- **Alert** when scores drift (e.g. model or prompt change)
- **Dashboard** distributions without joining seven separate check flags

## HTTP API

`POST /v1/outputs/validate` accepts **`include_quality_risk_score`** (boolean, default `false`). When `true`, the response **`metadata`** includes:

| Key | Type | Description |
|-----|------|-------------|
| `quality_risk_score` | float | Composite score |
| `quality_risk_decision` | string | `pass` / `repair` / `reject` |

Compute path uses the same `compute_slop_score()` as library code, with `grounded` inferred from non-empty `context_text` and `schema_valid` from the schema check when `expected_schema` is set.

## Optional in-process counters

Set **`ENABLE_QUALITY_RISK_METRICS=true`** to increment in-memory counters whenever `compute_slop_score()` runs (including via `include_quality_risk_score`):

| Metric key pattern | Meaning |
|--------------------|---------|
| `agentguard_quality_risk_total{bucket=low|mid|high,decision=...}` | One increment per scored output |

Inspect via existing **`GET /v1/evals/metrics`** snapshot (or your exporter if you wire `MetricsCollector` to Prometheus).

### Prometheus-style scraping (sketch)

Exporters typically map counters to:

```text
# HELP agentguard_quality_risk_total Observations by coarse score bucket and decision
# TYPE agentguard_quality_risk_total counter
agentguard_quality_risk_total{bucket="low",decision="pass"} 42
```

Histogram alternative: record `quality_risk_score` as a histogram bucket (`le=0.3`, `le=0.7`, `le=1.0`) in your own exporter by reading scores from logs or tracing.

## Drift ideas

- Track **weekly p50 / p95** of `quality_risk_score` per `use_case` or tenant (from your log pipeline).
- Alert when **reject** rate or **mid/high** bucket share jumps vs baseline.

## Source

Community feedback: [DEV comment — Conway Research](https://dev.to/conwayresearch/comment/35p1m) · GitHub [#8](https://github.com/MANIGAAA27/agentguard/issues/8).
