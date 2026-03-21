# Project Memory

Single source of truth for project knowledge. Persists across chat sessions so context is preserved when the agent chat limit is reached or a new window is opened.

**Usage**: Agents read this file at the start of build/orchestration or role-specific work. Update it when making decisions, completing work that affects others, or handing off to the next session or role.

---

## Architecture

- **Platform**: Python 3.11+ / FastAPI, async-first, Pydantic-native
- **Pattern**: Pipeline architecture -- requests flow through configurable chain of checks
- **Modules**: AI Gateway, Input Guardrails (7 checks), Prompt Framework (6 framework types), Retrieval Grounding, Output Validation (7 checks), Action Governance, Policy Engine, Observability, Slop Score
- **State**: Stateless services; Redis for rate limiting, PostgreSQL for audit logs
- **Policy**: YAML policy-as-code with deterministic evaluation engine
- **Prompts**: Versioned YAML prompt packages with anti-pattern linting
- **Quality gate**: AI Slop Prevention Score (0.0-1.0 composite, configurable thresholds)
- **Docs**: MkDocs Material theme with full-text search, 9 module pages, 4 guides, 3 cookbook entries

---

## Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-07 | Python 3.11+ / FastAPI | Async-first, Pydantic-native, OpenAPI auto-generation |
| 2026-03-07 | Setuptools build backend | Hatchling had compatibility issues with Python 3.13 |
| 2026-03-07 | Pipeline pattern | Configurable per-tenant check chains, easy to extend |
| 2026-03-07 | Policy-as-code (YAML) | Deterministic, testable, versionable; no runtime code injection |
| 2026-03-07 | Check interface pattern | Every check: `async def check() -> CheckResult` with decision enum |
| 2026-03-07 | Slop Score formula | Weighted composite of 6 components, thresholds configurable per tenant |
| 2026-03-07 | MkDocs Material for docs | Full-text search, navigation tabs, code copy, auto-generated API docs |

---

## Current Focus

MVP v0.1.0 is complete with all 8 modules, 7 REST endpoints, 67 passing tests, 3 prompt packages, 3 example policies, full architecture document, comprehensive README, and MkDocs documentation site.

---

## Handoff Notes

- All modules implemented and tested (67/67 tests passing)
- Next steps for v0.2.0: ML-backed checks (replace regex heuristics), dashboard UI, SDK clients
- Redis and PostgreSQL backends are interface-ready but MVP uses in-memory stores
- Retrieval module uses demo documents; needs pluggable backend integration
- Action governance idempotency uses in-memory set; needs Redis/DB backing for production

---

## Open Questions

- Which ML models to use for toxicity/injection detection in v0.2.0?
- Should the docs site be deployed to GitHub Pages or a custom domain?
- Need to decide on database migration strategy (Alembic?) for audit log schema
