# Output Validation

The Output Validation module runs 7 parallel quality checks on LLM-generated output. Each check returns a decision; the engine aggregates to the most restrictive.

## Checks

| Check | Detects | Decision on Fail |
|-------|---------|-----------------|
| Schema Validity | Invalid JSON or schema mismatch | `repair` |
| Citation Check | Missing citations when required | `repair` |
| Hallucination Proxy | Claims not found in context | `repair` or `reject` |
| Policy Check | Disclosure patterns, policy violations | `repair` |
| Unsafe Language | Harmful instructions in output | `reject` |
| Confidence Threshold | Excessive hedging language | `escalate` |
| Genericity Detector | Generic filler phrases ("AI slop") | `repair` |

## Decision Priority

`reject` > `escalate` > `repair` > `pass`

## Endpoint

`POST /v1/outputs/validate`

## Source

`src/agentguard/output_validation/`
