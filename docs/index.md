# AgentGuard — LLM guardrails (FastAPI)

**Open-source FastAPI LLM guardrails** for teams that need one HTTP control plane: **prompt injection** defense (heuristic), **PII** and secret checks, **LLM output validation**, versioned **prompt packages**, **policy-as-code**, retrieval **grounding**, and **agent** action governance with risk scoring and optional human approval.

AgentGuard is an **open-source FastAPI** service that sits between your application and any LLM provider. It applies **LLM guardrails** on input and output with **transparent heuristics** you can audit in code — not a black-box model. Python **3.11+**.

- [Quickstart](quickstart.md) — run locally in a few commands
- [Comparison](comparison.md) — vs Guardrails AI, NeMo Guardrails, LlamaGuard, Presidio, Rebuff
- [Architecture](architecture.md) — system design
- [GitHub repository](https://github.com/MANIGAAA27/agentguard) — source, issues, CI

## Key capabilities

| Module | Purpose | Endpoint |
|--------|---------|----------|
| [AI Gateway](modules/gateway.md) | AuthN/AuthZ, tenant isolation, rate limiting, model routing | `/v1/gateway/complete` |
| [Input Guardrails](modules/input-guardrails.md) | LLM guardrails on user input (7 checks) | `/v1/guardrails/evaluate-input` |
| [Prompt Framework](modules/prompt-framework.md) | Versioned prompt packages with linting | `/v1/prompts/compile` |
| [Retrieval Grounding](modules/retrieval-grounding.md) | Citation packaging and confidence scoring | `/v1/retrieval/search` |
| [Output Validation](modules/output-validation.md) | LLM output validation (7 checks) | `/v1/outputs/validate` |
| [Action Governance](modules/action-governance.md) | Tool allowlist, risk scoring, HITL approval | `/v1/actions/authorize` |
| [Policy Engine](modules/policy-engine.md) | Tenant/use-case/role/channel policies | `/v1/policies/evaluate` |
| [Observability](modules/observability.md) | Tracing, metrics, audit, evaluation suites | `/v1/evals/run` |

## Quick links

- [API Reference](api-reference.md)
- [Guides](guides/adding-a-check.md)
- [Middleware & control plane](guides/middleware-control-plane.md) — DIY vs managed vs self-hosted FastAPI
- [Quality risk score — monitoring](operations/quality-risk-score-monitoring.md) — thresholds & drift
- [Cookbook](cookbook/full-request-lifecycle.md)
- [LLM-oriented summary (`llms.txt`)](llms.txt)
