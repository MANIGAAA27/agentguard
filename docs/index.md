# AgentGuard

**Production-grade AI Guardrails, Checks, and Validation platform to eliminate AI slop across enterprise applications.**

AgentGuard is a service-oriented platform that sits between your user-facing apps/agents and LLM providers. It prevents low-quality, hallucinated, unsafe, non-compliant, and ungrounded AI outputs through modular guardrails, policy-as-code, and a composite AI Slop Prevention Score.

## Key Capabilities

| Module | Purpose | Endpoint |
|--------|---------|----------|
| [AI Gateway](modules/gateway.md) | AuthN/AuthZ, tenant isolation, rate limiting, model routing | `/v1/gateway/complete` |
| [Input Guardrails](modules/input-guardrails.md) | 7 safety checks on user input | `/v1/guardrails/evaluate-input` |
| [Prompt Framework](modules/prompt-framework.md) | Versioned prompt packages with linting | `/v1/prompts/compile` |
| [Retrieval Grounding](modules/retrieval-grounding.md) | Citation packaging and confidence scoring | `/v1/retrieval/search` |
| [Output Validation](modules/output-validation.md) | 7 quality checks on LLM output | `/v1/outputs/validate` |
| [Action Governance](modules/action-governance.md) | Tool allowlist, risk scoring, HITL approval | `/v1/actions/authorize` |
| [Policy Engine](modules/policy-engine.md) | Tenant/use-case/role/channel policies | `/v1/policies/evaluate` |
| [Observability](modules/observability.md) | Tracing, metrics, audit, evaluation suites | `/v1/evals/run` |

## Quick Links

- [Quickstart](quickstart.md) -- Get running in 3 commands
- [Architecture](architecture.md) -- Full system design document
- [API Reference](api-reference.md) -- All endpoints with schemas
- [Guides](guides/adding-a-check.md) -- How to extend AgentGuard
- [Cookbook](cookbook/full-request-lifecycle.md) -- End-to-end examples
