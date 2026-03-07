# Deployment Guide

## Docker Compose (Recommended for Getting Started)

```bash
cp .env.example .env
# Edit .env with production values
docker compose up --build -d
```

This starts: AgentGuard app (`:8000`), Redis (`:6379`), PostgreSQL (`:5432`).

## Production Considerations

1. **Set `APP_ENV=production`** and `APP_DEBUG=false`
2. **Set a strong `JWT_SECRET`** -- do not use the default
3. **Configure model API keys** (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
4. **Use external Redis and PostgreSQL** -- not the Docker Compose instances
5. **Set `CORS_ORIGINS`** to your frontend domains
6. **Enable rate limiting** with Redis backend (`RATE_LIMIT_BACKEND=redis`)

## Scaling

AgentGuard services are stateless. Scale horizontally by running multiple instances behind a load balancer. State is stored in:

- **Redis**: Rate limit counters, session cache
- **PostgreSQL**: Audit logs, policy storage (future)

## Health Check

```
GET /health
```

Returns `{"status": "ok", "version": "0.1.0"}`.

## Monitoring

See [Observability](../modules/observability.md) for tracing, metrics, and audit trail configuration.
