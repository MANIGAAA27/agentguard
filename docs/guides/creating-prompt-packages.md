# Creating Prompt Packages

Prompt packages are versioned YAML definitions that the Prompt Framework compiles into LLM-ready messages.

## Package Structure

```
prompt_packages/
└── your_package/
    ├── v1.0.0.yaml
    └── v1.1.0.yaml   # newer version
```

## YAML Schema

```yaml
name: your_package
version: "1.0.0"
framework: RAG_QA  # or TOOL_USE, STRUCTURED_SUMMARY, CLASSIFICATION, CRITIC_REPAIR, ACTION_EXECUTION
system_instructions: |
  Clear role definition for the model. Must be specific enough
  to pass the linter (minimum 20 characters).
developer_policy: |
  Rules the model must follow regardless of tenant.
refusal_policy: |
  When and how the model should refuse to answer.
  Required for all frameworks.
grounding_instructions: |
  How to use retrieved context. Required for RAG_QA.
output_schema:  # Required for TOOL_USE, STRUCTURED_SUMMARY, CLASSIFICATION, CRITIC_REPAIR, ACTION_EXECUTION
  type: object
  properties:
    answer:
      type: string
  required: [answer]
tool_definitions:  # Required for TOOL_USE, ACTION_EXECUTION
  - name: tool_name
    description: What the tool does
    parameters:
      param_name:
        type: string
        required: true
metadata:
  category: your-category
```

## Template Variables

Use `{{variable_name}}` in system instructions. Variables are passed at compile time:

```yaml
system_instructions: |
  You are an assistant for {{company_name}}.
```

## Linting

The compiler automatically lints your package against the framework requirements. Fix any `error`-severity warnings before deploying.

## Testing

Use the `/v1/prompts/compile` endpoint to test compilation:

```bash
curl -X POST http://localhost:8000/v1/prompts/compile \
  -H "Content-Type: application/json" \
  -d '{
    "package_name": "your_package",
    "package_version": "v1.0.0",
    "user_message": "Test question",
    "variables": {"company_name": "Acme Corp"}
  }'
```
