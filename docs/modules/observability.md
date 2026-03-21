# Observability and Evaluation

The Observability module provides request tracing, metrics collection, audit logging, and evaluation suite execution.

## Request Tracing

Every request gets a correlation ID (auto-generated or from `X-Correlation-ID` header). All log entries include `correlation_id`, `tenant_id`, and `endpoint`.

## Metrics

| Metric | Description |
|--------|-------------|
| `eval.case{suite,result}` | Evaluation case pass/fail counts |
| Validation pass/fail | Per-check pass rates |
| Hallucination proxy | Unsupported claim detection rate |
| Refusal rate | Percentage of blocked inputs |
| Escalation rate | Percentage of escalated decisions |

## Audit Trail

Every enforcement decision is logged with:

- Timestamp, audit ID, correlation ID
- Tenant ID, module, decision, reason
- Full metadata context

## Evaluation Suites

Run golden dataset regression tests and red-team evaluations through the API.

## Endpoints

- `POST /v1/evals/run` -- Run evaluation suite
- `GET /v1/evals/metrics` -- Metrics snapshot
- `GET /v1/evals/audit` -- Audit log entries

## Source

`src/agentguard/observability/`
