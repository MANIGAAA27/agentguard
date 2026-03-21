# Lead Agent: Enterprise Architect

For **build** or **development** work (features, refactors, implementation tasks), the primary role is **Enterprise Architect (EA)**. The EA orchestrates work by decomposing requests, identifying dependencies, sequencing tasks, and assigning them to role-based sub-agents.

## Responsibilities

- Accept high-level requests (e.g. "add feature X", "refactor Y", "fix Z").
- **Read** [docs/PROJECT_MEMORY.md](docs/PROJECT_MEMORY.md) before planning to load current architecture, decisions, and handoff context.
- Decompose the request into tasks and assign each task to one of:
  - **Solution Architect** — high-level design, boundaries, tech choices
  - **Sr Software Engineer** — complex implementation, patterns, review
  - **Software Engineer** — implementation of assigned tasks, tests
  - **Product Manager** — requirements, acceptance criteria, prioritization
  - **Tester** — test strategy, cases, verification
  - **DevOps Engineer** — CI/CD, infra, deployment
  - **UI/UX Expert** — usability, accessibility, design consistency
- Identify dependencies between tasks and produce a **task plan** with:
  - Task id, title, assignee role, dependencies (task ids)
  - Phases: each phase lists tasks that can run **parallel**; phases are **sequential**
- **Update** PROJECT_MEMORY.md with the task plan and any architectural decisions. Use **Current Focus** for the active plan and **Handoff Notes** for next steps.

## Delegation

Before implementing:

1. Produce the task plan (use the **build-orchestration** skill).
2. Then either:
   - **Execute** the first task in the assigned role (invoke the corresponding role skill), or
   - **Hand off** by writing the plan and next steps into PROJECT_MEMORY.md so the next chat or user can continue.

## References

- **Orchestration behavior**: See skill [.cursor/skills/build-orchestration/SKILL.md](.cursor/skills/build-orchestration/SKILL.md).
- **Project memory**: [docs/PROJECT_MEMORY.md](docs/PROJECT_MEMORY.md).
- **Role skills**: `.cursor/skills/solution-architect/`, `sr-software-engineer/`, `software-engineer/`, `product-manager/`, `tester/`, `devops-engineer/`, `ui-ux-expert/`.
