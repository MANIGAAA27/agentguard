# AI Gateway

The AI Gateway is the single entry point for all LLM and agent requests. It handles authentication, tenant isolation, rate limiting, and model provider routing.

## Responsibilities

- **AuthN/AuthZ**: API key and JWT validation
- **Tenant isolation**: Per-tenant configuration, rate limits, and model access
- **Rate limiting**: Token bucket algorithm with configurable RPM per tenant
- **Model routing**: Abstraction over OpenAI, Anthropic, and local/stub providers

## Endpoint

`POST /v1/gateway/complete`

### Non-streaming (default)

JSON body with `messages`; response is `application/json` (`GatewayResponse`).

### Streaming (`stream: true`)

When **`stream`** is `true` and **`model_provider`** is **`openai`**, the response is **`text/event-stream`** (OpenAI SSE passthrough). **Output validation** and **`quality_risk_score`** are not run on that response; buffer the assistant text and call **`POST /v1/outputs/validate`** afterward. See [ADR-001](../adrs/adr-001-streaming-output-validation.md).

Other providers return **400** `streaming_not_supported` until implemented.

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
