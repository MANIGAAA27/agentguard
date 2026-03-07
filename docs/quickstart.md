# Quickstart

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional, for containerized setup)

## Option 1: Local Development

```bash
# Clone and install
git clone <repo-url> && cd AgentGuard
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Configure
cp .env.example .env

# Run
make dev
```

The API is now available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Option 2: Docker Compose

```bash
cp .env.example .env
docker compose up --build -d
```

Services: app on `:8000`, Redis on `:6379`, PostgreSQL on `:5432`.

## Verify

```bash
# Health check
curl http://localhost:8000/health

# Evaluate input safety
curl -X POST http://localhost:8000/v1/guardrails/evaluate-input \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the refund policy?"}'
```

Expected response:

```json
{
  "correlation_id": "...",
  "decision": "allow",
  "checks": [...],
  "redacted_text": null,
  "metadata": {}
}
```

## Next Steps

- Browse the [API Reference](api-reference.md) for all endpoints
- Read the [Architecture](architecture.md) for system design
- Try the [Full Request Lifecycle](cookbook/full-request-lifecycle.md) cookbook
