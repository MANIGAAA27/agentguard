# Prompt Framework

The Prompt Framework provides versioned prompt packages, a compiler that assembles prompts from components, and a linter that detects anti-patterns.

## Framework Types

| Type | Requires Grounding | Requires Schema | Requires Tools |
|------|-------------------|-----------------|----------------|
| `RAG_QA` | Yes | No | No |
| `TOOL_USE` | No | Yes | Yes |
| `STRUCTURED_SUMMARY` | No | Yes | No |
| `CLASSIFICATION` | No | Yes | No |
| `CRITIC_REPAIR` | No | Yes | No |
| `ACTION_EXECUTION` | No | Yes | Yes |

## Prompt Compilation Order

1. System instructions (from package)
2. Developer policy (from package)
3. Tenant policy (runtime)
4. Grounding instructions + retrieved context
5. Refusal policy
6. Output schema instructions
7. User message

## Linter Anti-Patterns

| Code | Description | Severity |
|------|-------------|----------|
| `VAGUE_ROLE` | System instructions too short | warning |
| `NO_REFUSAL_POLICY` | No refusal policy defined | error |
| `NO_GROUNDING` | Grounding required but missing | error |
| `MISSING_OUTPUT_SCHEMA` | Schema required but missing | error |
| `UNRESTRICTED_TOOL_ACCESS` | Tools required but not defined | error |

## Endpoints

- `POST /v1/prompts/compile` -- Compile a prompt package
- `GET /v1/prompts/packages` -- List available packages

## Source

`src/agentguard/prompt_framework/`

See also: [Creating Prompt Packages](../guides/creating-prompt-packages.md)
