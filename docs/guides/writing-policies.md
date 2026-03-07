# Writing Policies

Policies are YAML files that define rules evaluated by the Policy Engine. Each rule has conditions, a decision, and a priority.

## File Location

- Default policy: `policies/default.yaml`
- Tenant policies: `policies/examples/<tenant>.yaml`

## Policy Structure

```yaml
name: my_policy
version: "1.0.0"
description: What this policy set enforces
tenant_id: optional-tenant-id  # null for global policies
rules:
  - id: unique-rule-id
    description: Human-readable description
    scope: global  # global | tenant | use_case | channel | role
    condition:
      field_name: expected_value
    decision: deny  # allow | deny | warn | escalate
    priority: 10    # lower number = evaluated first
```

## Condition Operators

| Syntax | Meaning | Example |
|--------|---------|---------|
| `field: value` | Exact match | `channel: api` |
| `field: { "$in": [...] }` | Value in list | `role: { "$in": ["admin", "manager"] }` |
| `field: { "$gt": n }` | Greater than | `amount: { "$gt": 10000 }` |
| `field: { "$lt": n }` | Less than | `risk_score: { "$lt": 0.3 }` |
| `field: { "$ne": value }` | Not equal | `status: { "$ne": "approved" }` |
| `{}` | Always matches | Catch-all rules |

## Priority

Rules are evaluated in priority order (lowest number first). The most restrictive decision wins:

`deny` > `escalate` > `warn` > `allow`

## Example: Block High-Value Refunds

```yaml
rules:
  - id: high-value-refund-approval
    description: Require approval for refunds over $10,000
    scope: tenant
    condition:
      action: refund_approval
      amount:
        $gt: 10000
    decision: escalate
    priority: 5
```

## Testing

```bash
curl -X POST http://localhost:8000/v1/policies/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "policy_name": "default",
    "context": {"requires_grounding": true, "grounded": false}
  }'
```
