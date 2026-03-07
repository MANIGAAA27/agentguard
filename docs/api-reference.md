# API Reference

All endpoints accept and return JSON. Authentication is via `X-API-Key` header. Tenant is identified via `X-Tenant-ID` header.

Interactive documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc) when the server is running.

## Endpoints

| Method | Endpoint | Module | Description |
|--------|----------|--------|-------------|
| POST | `/v1/guardrails/evaluate-input` | Input Guardrails | Evaluate user input for safety |
| POST | `/v1/prompts/compile` | Prompt Framework | Compile a versioned prompt package |
| POST | `/v1/retrieval/search` | Retrieval Grounding | Search with citation packaging |
| POST | `/v1/outputs/validate` | Output Validation | Validate LLM output quality |
| POST | `/v1/actions/authorize` | Action Governance | Authorize an agent action |
| POST | `/v1/evals/run` | Observability | Run an evaluation suite |
| POST | `/v1/policies/evaluate` | Policy Engine | Evaluate policy rules |
| GET | `/v1/gateway/complete` | AI Gateway | Send completion through trust layer |
| GET | `/v1/prompts/packages` | Prompt Framework | List available prompt packages |
| GET | `/v1/evals/metrics` | Observability | Get metrics snapshot |
| GET | `/v1/evals/audit` | Observability | Get audit log entries |
| GET | `/health` | System | Liveness probe |

## Common Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Content-Type` | Yes | `application/json` |
| `X-API-Key` | Production | API key for authentication |
| `X-Tenant-ID` | No | Tenant identifier (defaults to `default`) |
| `X-Correlation-ID` | No | Correlation ID for tracing (auto-generated if missing) |

## Decision Enums

### Input Decisions

`allow` | `redact` | `block` | `escalate` | `safe-complete-only`

### Output Decisions

`pass` | `repair` | `reject` | `escalate`

### Action Decisions

`allow` | `deny` | `require-approval` | `dry-run` | `escalate`

### Policy Decisions

`allow` | `deny` | `warn` | `escalate`

For detailed request/response schemas, see the interactive Swagger UI at `/docs`.
