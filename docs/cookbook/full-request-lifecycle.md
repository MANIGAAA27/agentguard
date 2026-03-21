# Full Request Lifecycle

This walkthrough shows a complete request from user input to validated response, hitting every module in the pipeline.

## Scenario

A customer asks: "What is the refund policy?" using the RAG_QA prompt package.

## Step 1: Evaluate Input

```bash
curl -X POST http://localhost:8000/v1/guardrails/evaluate-input \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: default" \
  -d '{"text": "What is the refund policy?"}'
```

Response: `decision: "allow"` -- all 7 checks pass.

## Step 2: Search for Grounding Context

```bash
curl -X POST http://localhost:8000/v1/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{"query": "refund policy", "require_grounding": true}'
```

Response: Citations found with confidence scores. `grounded: true`.

## Step 3: Compile Prompt

```bash
curl -X POST http://localhost:8000/v1/prompts/compile \
  -H "Content-Type: application/json" \
  -d '{
    "package_name": "rag_qa",
    "user_message": "What is the refund policy?",
    "retrieved_context": "[1] Company Refund Policy (confidence: 0.667)\nRefunds are available within 30 days of purchase with a valid receipt."
  }'
```

Response: Compiled messages with system instructions, grounding, and refusal policy. Lint warnings (if any).

## Step 4: Call LLM (via Gateway)

The compiled messages are sent to the LLM provider through the gateway.

## Step 5: Validate Output

```bash
curl -X POST http://localhost:8000/v1/outputs/validate \
  -H "Content-Type: application/json" \
  -d '{
    "output_text": "Based on the company policy, refunds are available within 30 days of purchase with a valid receipt [1].",
    "context_text": "Refunds are available within 30 days of purchase with a valid receipt.",
    "require_citations": true
  }'
```

Response: `decision: "pass"` -- all checks pass, citations present, no hallucination.

## Step 6: Evaluate Policy

```bash
curl -X POST http://localhost:8000/v1/policies/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "policy_name": "default",
    "context": {"requires_grounding": true, "grounded": true}
  }'
```

Response: `decision: "allow"` -- grounding requirement satisfied.

## Result

The validated, grounded, policy-compliant response is returned to the user.
