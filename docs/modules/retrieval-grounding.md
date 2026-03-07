# Retrieval Grounding

The Retrieval Grounding module provides citation packaging, source confidence scoring, and query rewriting with safety controls. It enforces that grounded use cases cannot generate answers without evidence.

## Features

- **Query rewriting**: Strips unsafe patterns before retrieval
- **Document search**: Pluggable backend (MVP: keyword matching)
- **Confidence scoring**: Per-citation confidence based on query overlap
- **Citation packaging**: Formats citations as numbered context for prompt injection
- **Grounding enforcement**: `grounded` flag indicates whether sufficient evidence was found

## Endpoint

`POST /v1/retrieval/search`

## Source

`src/agentguard/retrieval/`
