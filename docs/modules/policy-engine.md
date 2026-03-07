# Policy Engine

The Policy Engine evaluates request context against YAML-defined policy rules. It supports tenant-level, use-case-level, role-based, and channel-specific policies.

## Policy Structure

```yaml
name: policy_name
version: "1.0.0"
description: What this policy set does
tenant_id: optional-tenant-id
rules:
  - id: rule-id
    description: What this rule checks
    scope: global | tenant | use_case | channel | role
    condition:
      field: value
      field2: { "$gt": 100 }
    decision: allow | deny | warn | escalate
    priority: 10  # lower = higher priority
```

## Condition Operators

| Operator | Example | Meaning |
|----------|---------|---------|
| equality | `field: value` | Exact match |
| `$in` | `field: { "$in": ["a", "b"] }` | Value in list |
| `$gt` | `field: { "$gt": 100 }` | Greater than |
| `$lt` | `field: { "$lt": 50 }` | Less than |
| `$ne` | `field: { "$ne": "blocked" }` | Not equal |

## Example Policies

See `policies/examples/` for healthcare, finance, and general tenant policies.

## Endpoint

`POST /v1/policies/evaluate`

## Source

`src/agentguard/policy/`

See also: [Writing Policies](../guides/writing-policies.md)
