# Changelog

All notable changes to AgentGuard are documented in this file.

## [0.1.0] - 2026-03-07

### Added

- AI Gateway with AuthN/AuthZ, tenant isolation, rate limiting, and model provider abstraction
- Input Guardrails with 7 checks: prompt injection, jailbreak, toxicity, PII detection, secret detection, restricted topics, data exfiltration
- Prompt Framework with versioned packages, 6 framework types, compiler, and anti-pattern linter
- Retrieval Grounding with citation packaging, confidence scoring, and query rewriting
- Output Validation with 7 checks: schema validity, citation presence, hallucination proxy, policy violations, unsafe language, confidence threshold, genericity detection
- Action Governance with tool allowlist, risk scoring, HITL approval workflow, dry-run mode, and idempotency protection
- Policy Engine with YAML policy-as-code, tenant/use-case/role/channel scoping, and condition operators
- Observability with request tracing, metrics collection, audit trail, and evaluation suite runner
- AI Slop Prevention Score with 6-component weighted composite model
- 3 example prompt packages: rag_qa, tool_use, structured_summary
- 3 example policy sets: healthcare, finance, general
- 67 passing tests covering all modules
- Docker and Docker Compose configuration
- MkDocs documentation site with Material theme
- Comprehensive README with architecture diagrams, API reference, and usage examples
