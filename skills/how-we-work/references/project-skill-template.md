---
name: project-<name>
description: Project facts for <name> only; load alongside the workflow and relevant layer skills when working in this repository.
---

# Project <name>

Copy into `skills/project-<name>/SKILL.md`; replace placeholders and remove unused sections. Keep verified facts with source paths, not repeated general rules. Add UI metadata using a neighboring skill as an example.

| Area | Verified facts |
|---|---|
| Identity | repository, purpose, stack, worktree naming. |
| Commands | setup, focused tests, lint, asset build, full local CI. |
| Domain | owners, namespaces, associations, lifecycle and permission semantics. |
| Existing mechanisms | reusable primitives, explicit composition points, helpers and legacy patterns to avoid. |
| Frontend | established components, tokens/palette, themes, density and asset paths. Link a design reference only if it exists. |
| Tests | existing fixtures/builders, authentication and provider stubs. No UI/DOM tests by default. |
| History | commit and PR conventions differing from package defaults. |

Specific project facts override general defaults; explicit user instructions remain authoritative. Do not add standing approval gates or broaden task scope.
