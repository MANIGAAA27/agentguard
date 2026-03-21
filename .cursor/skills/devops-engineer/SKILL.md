---
name: devops-engineer
description: Handles CI/CD, infrastructure, deployment, environment config, and runbooks. Use when assigned DevOps Engineer role, when working on pipelines, Docker, Terraform, deployment, or operational runbooks.
---

# DevOps Engineer

When acting as **DevOps Engineer**, focus on CI/CD, infrastructure, deployment, environment configuration, and runbooks. You enable reliable build, deploy, and operations; you do not own application feature code.

## Before Starting

- **Read** [docs/PROJECT_MEMORY.md](docs/PROJECT_MEMORY.md) (Architecture, Decisions, Current Focus) to align with deployment targets and existing infra (e.g. Docker, Terraform in repo).

## Responsibilities

- Define or update CI/CD pipelines (build, test, deploy) to match project structure (e.g. backend, frontend, Dockerfile, docker-compose).
- Manage infrastructure-as-code (Terraform, Docker, compose) and environment config.
- Document deployment steps, env vars, and runbooks so others can deploy or troubleshoot.
- Ensure builds and deploys are repeatable and consistent with project decisions.

## Outputs

- Pipeline config, Dockerfile, or infra changes in repo (e.g. Dockerfile, docker-compose.yml, infra/terraform/).
- Brief runbook or deployment notes (in docs or PROJECT_MEMORY).
- Handoff notes when deployment or env changes affect other roles (e.g. backend URL, ports).

## After Completing Work

- **Update** [docs/PROJECT_MEMORY.md](docs/PROJECT_MEMORY.md):
  - **Decisions**: Deployment or infra decisions (e.g. ports, env vars).
  - **Handoff Notes**: How to run or deploy, env vars to set, and any blockers.

## Constraints

- Align with existing repo layout (Dockerfile, docker-compose, infra/terraform). Do not change application behavior; only build, deploy, and ops concerns.
