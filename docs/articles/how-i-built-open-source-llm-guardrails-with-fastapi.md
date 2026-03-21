# How I built open-source LLM guardrails with FastAPI

*Cross-post friendly: copy this file to [dev.to](https://dev.to) or [Hashnode](https://hashnode.com). Suggested title above; adjust the intro to first person if you prefer.*

**Suggested title:** How I built open-source LLM guardrails with FastAPI  
**Suggested tags / topics:** `python`, `fastapi`, `llm`, `ai`, `opensource`, `machinelearning`, `security`

---

When you put an LLM behind a real product, you quickly need more than a system prompt. You need **LLM guardrails**: something that sits between users and the model to catch **prompt injection**, **PII**, bad outputs, and risky agent actions—without hiding everything in one unmaintainable blob of instructions.

I shipped **[AgentGuard](https://github.com/MANIGAAA27/agentguard)** as that layer: an **open-source FastAPI** service that runs **input checks**, **output validation**, **versioned prompt packages**, **policy-as-code**, and **action governance** (risk scoring and optional human approval) through a single HTTP API. It targets **platform engineers** who want **auditability**: the checks are **heuristic code** you can read and extend, not a black box.

## What “LLM guardrails” means here

In one request path, AgentGuard can:

- **Evaluate user input** before it hits the model—prompt injection heuristics (including a scored model to cut enterprise false positives), jailbreak patterns, PII regexes, secret-shaped tokens, and more.
- **Compile prompts** from versioned YAML “packages” so prompts are lintable and reviewable like code.
- **Validate LLM output**—schema fit, citations, lightweight grounding heuristics (literal overlap and bigram overlap vs context—honestly documented as *not* full hallucination detection).
- **Evaluate policies** from YAML and **authorize agent actions** with risk levels and HITL-style gates.

The README includes a straight **[Limitations](https://github.com/MANIGAAA27/agentguard#limitations)** section: these are **regex and keyword heuristics** for the most part, not a drop-in replacement for enterprise DLP or classifier stacks like LlamaGuard. That honesty matters for trust—and for knowing when to add your own checks or integrate a model later.

## Why FastAPI

FastAPI gives a **typed**, **documented** surface (`/docs` out of the box) that any stack can call. Teams can run AgentGuard as a **sidecar** or internal service, keep policies in git, and wire **tenant headers** and **correlation IDs** through the pipeline. The same codebase installs as a **Python package** (`pip install -e ".[dev]"` today; PyPI is on the roadmap).

## Try it in one minute

Clone and run:

```bash
git clone https://github.com/MANIGAAA27/agentguard.git && cd agentguard
pip install -e ".[dev]"
PYTHONPATH=src uvicorn agentguard.main:app --reload --host 0.0.0.0 --port 8000
```

Then hit the docs at `http://localhost:8000/docs`, or smoke-test guardrails:

```bash
curl -s -X POST http://localhost:8000/v1/guardrails/evaluate-input \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the refund policy?"}' | python -m json.tool
```

## Docs, comparison, and citations

- **Live docs (GitHub Pages):** [manigaaa27.github.io/agentguard](https://manigaaa27.github.io/agentguard/)  
- **How it compares** to Guardrails AI, NeMo Guardrails, LlamaGuard, Presidio, etc.: [comparison page](https://manigaaa27.github.io/agentguard/comparison/)  
- **Citing the project:** GitHub’s “Cite this repository” uses [`CITATION.cff`](https://github.com/MANIGAAA27/agentguard/blob/main/CITATION.cff).

## What I’d love from you

If this matches how you think about **LLM safety middleware**, a **star** on [github.com/MANIGAAA27/agentguard](https://github.com/MANIGAAA27/agentguard) helps discovery. Issues labeled **good first issue** are set up for small contributions (UK PII patterns, regression tests, Unicode edge cases). Feedback and PRs welcome.

---

*License: MIT. AgentGuard is independent tooling; all product names belong to their owners.*
