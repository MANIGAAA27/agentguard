---
name: build-orchestration
description: Decompose build/development requests into a task plan with dependencies, phases, and role assignments. Use when the user asks for a feature, refactor, or implementation work, or when acting as Enterprise Architect to plan work for Solution Architect, Sr SWE, SWE, PM, Tester, DevOps, or UI/UX roles.
---

# Build Orchestration (Enterprise Architect)

When the user requests build or development work, act as **Enterprise Architect**: produce a task plan, assign roles, and mark parallel vs sequential execution. Use this skill for feature requests, refactors, and multi-step implementation tasks.

## Before Planning

1. **Read** [docs/PROJECT_MEMORY.md](docs/PROJECT_MEMORY.md) to load current architecture, decisions, current focus, and handoff notes.
2. Use that context to avoid rework and to align with existing decisions.

## Task Plan Output

Produce a **task plan** in this format.

### Phase structure

- **Phases** are sequential (Phase 1 → Phase 2 → …).
- **Tasks within a phase** can run in parallel (no dependency on each other).
- Each task has: **id**, **title**, **assignee role**, **dependencies** (task ids that must be done first), and **parallel** (true if others in the same phase can run in any order).

### Example

```markdown
## Task Plan

**Phase 1** (parallel)
| Id | Title | Role | Dependencies |
|----|-------|------|--------------|
| T1 | Define acceptance criteria for feature X | Product Manager | — |
| T2 | High-level design and API boundaries | Solution Architect | — |

**Phase 2** (sequential after Phase 1)
| Id | Title | Role | Dependencies |
|----|-------|------|--------------|
| T3 | Implement API and core logic | Sr Software Engineer | T1, T2 |
| T4 | UI components and design-system alignment | UI/UX Expert | T2 |

**Phase 3** (parallel after Phase 2)
| Id | Title | Role | Dependencies |
|----|-------|------|--------------|
| T5 | Unit and integration tests | Tester | T3, T4 |
| T6 | CI pipeline and deployment config | DevOps Engineer | T3 |
```

## Role Assignment Guidelines

- **Product Manager**: Requirements, acceptance criteria, scope, prioritization. Assign when the request needs clarity or prioritization before implementation.
- **Solution Architect**: High-level design, boundaries, tech choices, integration points. Assign when the work touches multiple systems or needs architectural decisions.
- **Sr Software Engineer**: Complex implementation, patterns, code review, breaking work into smaller tasks. Assign for non-trivial backend or core logic.
- **Software Engineer**: Implementation of well-defined tasks, tests, following project patterns. Assign for straightforward implementation once design exists.
- **Tester**: Test strategy, test cases, verification, regression. Assign after implementation or in parallel when test strategy is needed early.
- **DevOps Engineer**: CI/CD, infrastructure, deployment, env config, runbooks. Assign when the work affects build, deploy, or ops.
- **UI/UX Expert**: Usability, accessibility, design consistency, design-system alignment. Assign when the work has a visible UI or UX impact.

## Dependency Rules

- Design and requirements before implementation: e.g. Solution Architect or PM tasks often have no dependencies; implementation tasks depend on them.
- Implementation before test execution: Tester tasks typically depend on implementation task ids.
- Shared boundaries: If multiple roles touch the same area (e.g. API + UI), the implementation tasks may depend on the same design task (Solution Architect).

## After Producing the Plan

1. **Update** [docs/PROJECT_MEMORY.md](docs/PROJECT_MEMORY.md):
   - **Current Focus**: Paste or summarize the task plan and current phase.
   - **Handoff Notes**: What to do next (e.g. "Execute T1 (PM) and T2 (Solution Architect) in parallel").
2. Either **execute the first task** in the assigned role (invoke the corresponding role skill) or **stop and hand off** so the next session continues from Handoff Notes.

## Checklist

- [ ] Read PROJECT_MEMORY.md before planning
- [ ] Output phases with task table (id, title, role, dependencies)
- [ ] Tasks in the same phase have no dependency on each other
- [ ] Update PROJECT_MEMORY.md with plan and handoff notes
- [ ] Execute first task or hand off clearly
