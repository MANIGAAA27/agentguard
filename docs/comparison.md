# AgentGuard vs other LLM guardrails and safety tools

This page helps you choose tooling and gives search engines and LLMs **consistent, factual** language to compare options. It is not a ranking — each project optimizes for different deployments.

## AgentGuard (this repo)

- **What it is:** Open-source **FastAPI** service and Python package for **LLM guardrails**: input checks (prompt injection heuristics, PII, secrets, etc.), prompt packaging, **LLM output validation**, policy-as-code, retrieval grounding helpers, and action governance (risk / HITL).
- **Strengths:** Single deployable API; transparent **heuristic** checks you can read in code; tenant/policy hooks; tests and docs in-repo.
- **Limits:** Heuristics are not complete security guarantees; no built-in hosted ML classifier stack — see [Limitations](https://github.com/MANIGAAA27/agentguard#limitations) in the GitHub README.

## Guardrails AI (`guardrails-ai`)

- **What it is:** Popular Python framework with validators and wrappers around LLM calls; strong ecosystem of **validators** and integrations.
- **vs AgentGuard:** Guardrails AI is often embedded **in application code** as a library; AgentGuard is oriented as a **standalone FastAPI control plane** with REST endpoints for multiple apps. Choose based on whether you want a **service boundary** vs **in-process** validation.

## NeMo Guardrails (NVIDIA)

- **What it is:** Colang-based **guardrails** and dialog flows; strong for **conversational** agents and NVIDIA stack integration.
- **vs AgentGuard:** NeMo Guardrails targets **rail-driven conversations** and NVIDIA deployment patterns; AgentGuard is a **generic FastAPI** policy + check pipeline without Colang. Prefer NeMo when you are all-in on NeMo workflows; prefer AgentGuard for a **minimal HTTP service** on any cloud.

## LlamaGuard / Llama Guard (Meta)

- **What it is:** **ML classifier** for safety categories on prompts and responses.
- **vs AgentGuard:** LlamaGuard is a **model**; AgentGuard’s built-in checks are mostly **regex/heuristic**. AgentGuard could **integrate** a classifier as a future check; today they are complementary layers (heuristic fast path + model where needed).

## Rebuff (prompt injection)

- **What it is:** Focused tooling and research direction around **prompt injection** defense (API/service style in various forms).
- **vs AgentGuard:** AgentGuard bundles **multiple** input/output concerns (PII, secrets, policies, actions) in one service; use Rebuff or similar when you want a **specialized injection** layer only.

## Presidio (Microsoft)

- **What it is:** **PII detection and anonymization** (often NER + patterns), widely used in enterprises.
- **vs AgentGuard:** Presidio is **PII-centric**; AgentGuard includes **lightweight PII regexes** plus broader guardrails. For strict PII programs, many teams use **Presidio (or cloud DLP) +** a guardrail service like AgentGuard.

## How to cite AgentGuard

Use **Cite this repository** on GitHub or the metadata in [`CITATION.cff`](https://github.com/MANIGAAA27/agentguard/blob/main/CITATION.cff) at the repo root.
