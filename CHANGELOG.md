# Changelog

All notable changes to AgentGuard are documented in this file.

## [0.1.2] - 2026-03-22

### Fixed

- **Tooling**: Ruff `target-version` and mypy `python_version` aligned with **`requires-python >=3.11`** (was 3.12-only)
- **Metadata**: Trove classifiers include Python 3.11 and 3.12; `authors` set for PyPI-style metadata

### Added

- **PR template** (`.github/pull_request_template.md`) for check scope, tests, and false-positive regression checklist
- **adding-a-check.md** Step 5: run `make lint` and `make typecheck` before opening a PR

### Changed

- **CONTRIBUTING**: CI runs tests only; editable-install note vs `PYTHONPATH`; maintainer note for applying **`good first issue`** labels

## [0.1.1] - 2026-03-21

### Fixed

- README and CONTRIBUTING clone URL: `https://github.com/MANIGAAA27/agentguard.git` (was placeholder `your-org`)
- **Prompt injection**: narrowed `system:` to line-start only; role phrase requires `you are now a/an <word>` (avoids substring match inside “able”); **critical vs scored** model with threshold to reduce enterprise false positives
- **Hallucination proxy**: documented limits; added **bigram-overlap** heuristic vs context for long outputs (still not full hallucination detection)

### Added

- **`register_pii_pattern()`** / **`get_pii_patterns()`** for tenant-specific PII regexes; engine redaction uses merged pattern map
- **GitHub Actions** CI (`.github/workflows/ci.yml`) — `pip install -e ".[dev]"`, `make test` on Python 3.11 and 3.12
- README **Limitations** section (honest scope of heuristics); enterprise-forward positioning; module-table warnings for PII / hallucination / injection
- Tests for enterprise phrasing, PII registration, hallucination overlap

### Changed

- `pyproject.toml` description and keywords aligned with LLM guardrails / governance discoverability

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
