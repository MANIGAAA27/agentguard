# AI Slop Prevention Score

The AI Slop Prevention Score is a composite metric that quantifies the quality and trustworthiness of an AI response. It combines 6 weighted components into a single 0.0-1.0 score.

## Components

| Component | Weight | Range | Description |
|-----------|--------|-------|-------------|
| Grounding Coverage | 0.25 | 0=grounded, 1=ungrounded | Whether output is backed by evidence |
| Schema Compliance | 0.15 | 0=valid, 1=invalid | Whether output matches expected schema |
| Unsupported Claim Ratio | 0.20 | 0-1 | Ratio of claims not found in context |
| Genericity Score | 0.15 | 0=specific, 1=generic | Density of filler phrases |
| Policy Risk Score | 0.15 | 0-1 | Policy violation severity |
| Action Risk Score | 0.10 | 0-1 | Risk level of proposed actions |

## Formula

```
slop_score = 0.25 * grounding_coverage
           + 0.15 * schema_compliance
           + 0.20 * unsupported_claim_ratio
           + 0.15 * genericity_score
           + 0.15 * policy_risk_score
           + 0.10 * action_risk_score
```

## Decision Thresholds

| Score Range | Decision | Meaning |
|-------------|----------|---------|
| 0.0 - 0.3 | `pass` | Output is clean |
| 0.3 - 0.7 | `repair` | Output needs improvement |
| 0.7 - 1.0 | `reject` | Output is unacceptable |

Thresholds are configurable per tenant via `SLOP_SCORE_THRESHOLD_PASS` and `SLOP_SCORE_THRESHOLD_REPAIR`.

## Source

`src/agentguard/slop_score/`
