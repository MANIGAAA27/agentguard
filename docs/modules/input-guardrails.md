# Input Guardrails

The Input Guardrails module runs 7 parallel safety checks on user input before it reaches the LLM. Each check returns a decision; the engine aggregates to the most restrictive.

## Checks

| Check | Detects | Decision on Fail |
|-------|---------|-----------------|
| Prompt Injection | Instruction override attempts | `block` |
| Jailbreak | DAN mode, role-play exploits | `block` |
| Toxicity | Violent, abusive, harmful content | `block` |
| PII Detection | SSN, email, phone, credit card, IP | `redact` |
| Secret Detection | AWS keys, GitHub tokens, JWTs, private keys | `block` |
| Restricted Topics | Illegal activities, exploitation | `block` |
| Data Exfiltration | Training data extraction, system prompt leaks | `block` |

## Decision Priority

`block` > `escalate` > `safe-complete-only` > `redact` > `allow`

## Endpoint

`POST /v1/guardrails/evaluate-input`

## Source

`src/agentguard/input_guardrails/`

## Extending

To add a new check, see [Adding a Check](../guides/adding-a-check.md).
