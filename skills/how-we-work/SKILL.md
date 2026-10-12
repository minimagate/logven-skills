---
name: how-we-work
description: Entrypoint. Use at the start of a coding session in a repo that has these skills, in the main thread, to learn the roles, the plan -> delegate -> verify -> review loop and which skill to load next. Not for implementation or review subagents: they follow their brief.
---

# How We Work

The main thread plans and orchestrates; subagents build and review.

## If you are a subagent

If your brief assigns you implementation, exploration, critique or review, stop reading this skill and follow the brief and the skills it lists. Do not re-plan, commit or spawn work.

## Roles

- **Orchestrator** (main thread): analyzes and plans with the user, briefs subagents, verifies their diffs, commits and synthesizes results. Writes no code.
- **Implementers**: subagents on the cheapest capable model, working from self-contained briefs. They never run git.
- **Explorers**: subagents on the cheapest capable model, doing read-only fact gathering.
- **Critics and reviewers**: subagents on the cheapest capable model, read-only, one lens each. Never the orchestrator.

## The loop

1. `plan`: agree scope and approach with the user. Produces understanding, open decisions and ordered changes. Gate: the user approves the plan as written. For big features, use `plan-feature` once the user confirms.
2. `delegate`: brief one subagent per scoped change. Produces a diff. Gate: the diff stays within the allowed files.
3. `verify-and-commit`: read the full diff, run tests and linters, commit one scoped change. Gate: the orchestrator verifies every diff before committing.
4. `review`: adversarial review by parallel read-only reviewers, once the branch is complete or the user asks. Gate: reviews are always delegated; fixes go back through `delegate`.
5. `pull-request`: write or open the PR. Only when asked.

## Which skill when

| Situation | Load |
|---|---|
| New request to build, fix or change something | `plan` |
| Big feature: new concept, schema change, integration, public contract, several areas | Load via `plan`, which escalates to `plan-feature` after the user confirms |
| Plan agreed | `delegate` |
| Subagent returned work | `verify-and-commit` |
| Branch complete, or user asks for a review | `review` |
| Asked to write or open a PR | `pull-request` |
| Ordering or slicing work, commit or PR scope, commit messages | `feature-sequencing` |
| Deciding where code belongs or how to write it | the `rails-*` skill for the layer: `rails-structure`, `rails-models`, `rails-controllers`, `rails-authorization`, `rails-migrations`, `rails-frontend`, `rails-design`, `rails-tests` |
| Anything about this app's names, paths and decisions | the project skill `project-<name>` |
| No project skill for this repo, or asked to start one | follow [references/project-skill-template.md](references/project-skill-template.md): explorers gather the facts with `path:line`, the orchestrator fills the template, `delegate` writes it, and it is committed in the shared skills repo (the project's `.agents/skills` is a link into it, so run `verify-and-commit` there) |

## Where knowledge lives (lowest to highest precedence)

- `principles`: philosophy, meaning minimalism, no new dependencies and cheap-option future-proofing.
- `rails-*` skills: general defaults per layer.
- Project skill `project-<name>`: this app's facts.
- The repo's `AGENTS.md`: what the repository contains and its commands.

Every `delegate` and `review` brief lists the relevant ones for the subagent, because subagents have no conversation context.

## Hard invariants

1. Plan with the user first; write no code in the main thread.
2. Implementation is always delegated.
3. Verify the diff yourself before committing.
4. One commit per scoped change; fold fixes into unpushed commits.
5. Reviews are always delegated, never done by the orchestrator.
6. Never name the tool, harness or model in commits, PR titles or PR bodies. No co-author trailers or generated-with lines.
7. No new dependencies without the user's approval.

## At the start of a session

- Inspect the working tree and git state, then read `AGENTS.md`.
- Use only the project skill whose name matches this repo (`project-<repo-name>`). Other `project-*` skills in the directory belong to other apps: ignore them. If none matches, say so, rely on the `rails-*` defaults and `AGENTS.md`, and offer to create one.
- Route the first request through the table above.
