# Action Governance

The Action Governance module controls what actions AI agents can take. It validates tools against an allowlist, scores risk, and enforces approval workflows for sensitive operations.

## Features

- **Tool allowlist**: Only pre-approved tools can be invoked
- **Parameter validation**: Required parameters checked before execution
- **Risk scoring**: Composite score based on tool, action, and parameters
- **HITL approval**: High-risk actions require human approval
- **Dry-run mode**: Evaluate without executing
- **Idempotency**: Replay protection via idempotency keys

## High-Risk Action Examples

- `delete_record` -- Permanent data deletion
- `refund_approval` -- Financial authorization
- `bulk_update` -- Mass data mutation
- `customer_entitlement_override` -- Access control changes

## Endpoint

`POST /v1/actions/authorize`

## Source

`src/agentguard/action_governance/`
