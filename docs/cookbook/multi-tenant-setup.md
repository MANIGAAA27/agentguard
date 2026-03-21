# Multi-Tenant Setup

This guide shows how to configure AgentGuard for multiple tenants with different policies and rate limits.

## Tenant Identification

Tenants are identified by the `X-Tenant-ID` header. If missing, the `default` tenant is used.

```bash
curl -X POST http://localhost:8000/v1/guardrails/evaluate-input \
  -H "X-Tenant-ID: healthcare-org" \
  -H "Content-Type: application/json" \
  -d '{"text": "Patient John Doe, SSN 123-45-6789"}'
```

## Tenant-Specific Policies

Create a policy file in `policies/examples/`:

```yaml
# policies/examples/healthcare_tenant.yaml
name: healthcare_tenant
version: "1.0.0"
tenant_id: healthcare-org
rules:
  - id: hipaa-pii-block
    description: Block any request containing patient PII
    scope: tenant
    condition:
      has_pii: true
    decision: deny
    priority: 1
```

Evaluate with the tenant's policy:

```bash
curl -X POST http://localhost:8000/v1/policies/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "policy_name": "healthcare_tenant",
    "context": {"has_pii": true}
  }'
```

## Tenant-Specific Rate Limits

Tenant rate limits are configured in the tenant registry. The default is 60 RPM. Override per tenant in the gateway configuration.

## Tenant-Specific Slop Score Thresholds

Configure `SLOP_SCORE_THRESHOLD_PASS` and `SLOP_SCORE_THRESHOLD_REPAIR` per tenant for stricter or more lenient quality gates.
