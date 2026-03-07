# AI Gateway

The AI Gateway is the single entry point for all LLM and agent requests. It handles authentication, tenant isolation, rate limiting, and model provider routing.

## Responsibilities

- **AuthN/AuthZ**: API key and JWT validation
- **Tenant isolation**: Per-tenant configuration, rate limits, and model access
- **Rate limiting**: Token bucket algorithm with configurable RPM per tenant
- **Model routing**: Abstraction over OpenAI, Anthropic, and local/stub providers

## Endpoint

`POST /v1/gateway/complete`

## Source

`src/agentguard/gateway/`

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY_HEADER` | Header name for API key | `X-API-Key` |
| `JWT_SECRET` | JWT signing secret | (required in production) |
| `TENANT_HEADER` | Header for tenant ID | `X-Tenant-ID` |
| `DEFAULT_MODEL_PROVIDER` | Default LLM provider | `openai` |
| `DEFAULT_MODEL_NAME` | Default model name | `gpt-4o` |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | Per-tenant RPM | `60` |
