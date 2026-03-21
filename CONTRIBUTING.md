# Contributing to AgentGuard

Thank you for your interest in contributing to AgentGuard. This guide covers setup, development workflow, and pull request guidelines.

## Development Setup

```bash
git clone https://github.com/MANIGAAA27/agentguard.git && cd agentguard
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

## Running the Application

```bash
make dev
```

The API is available at `http://localhost:8000/docs`.

## Running Tests

```bash
make test
```

All tests must pass before submitting a PR. CI runs `make lint` and `make test` on push/PR.

### Git history

Prefer **small, focused commits** with clear messages. The project benefits from reviewable history (especially for security-adjacent code). See [open issues](https://github.com/MANIGAAA27/agentguard/issues); issues labeled **good first issue** are entry points for new contributors.

## Code Quality

```bash
make lint       # ruff check
make format     # ruff format
make typecheck  # mypy
```

## Pull Request Guidelines

1. **Branch from `main`** and use descriptive branch names: `feat/add-toxicity-ml-check`, `fix/pii-regex-false-positive`.
2. **Write tests** for new checks, policies, or endpoints.
3. **Update docs** if you add or change API endpoints, configuration, or module behavior.
4. **Keep PRs focused** -- one feature or fix per PR.
5. **Follow existing patterns** -- new guardrail checks should implement the `async def check() -> CheckResult` interface.

## Adding a New Guardrail Check

See [docs/guides/adding-a-check.md](docs/guides/adding-a-check.md).

## Code Style

- Python 3.11+, type hints required
- Ruff for linting and formatting (config in `pyproject.toml`)
- Pydantic models for all API contracts
- Async functions for all check implementations
- Structured logging via `structlog`

## Project Structure

See the [README](README.md#project-structure) for the annotated directory tree.
