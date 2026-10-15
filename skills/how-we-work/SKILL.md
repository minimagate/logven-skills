---
name: how-we-work
description: Entrypoint for a coding session in the main thread of a repo that has these skills. Holds the roles, the plan -> delegate -> verify -> review -> PR loop, skill routing, the shared principles, the delegation brief and the verify-and-commit procedure. Subagents read only its Principles section, when their brief points to it.
---

# How We Work

The main thread plans and orchestrates; subagents build and review.

## If you are a subagent

If your brief assigns you implementation, exploration, critique or review, read only the Principles section below (when your brief or a guideline skill points to it), then follow the brief and the skills it lists. Do not re-plan, commit or spawn work.

## Roles

- **Orchestrator** (main thread): plans with the user, briefs subagents, verifies their diffs, commits and synthesizes. Writes no code.
- **Implementers**: subagents on the cheapest capable model, working from self-contained briefs. They never run git.
- **Explorers, critics and reviewers**: subagents on the cheapest capable model, read-only. Critics and reviewers take one lens each and are never the orchestrator.

## The loop

1. **Plan** (`plan`): agree scope and approach. Gate: the user approves the plan as written. Big features escalate to its critic lenses once the user confirms.
2. **Delegate** (below): one subagent per scoped change, producing a diff. Gate: the diff stays within the allowed files.
3. **Verify and commit** (below): read the full diff, run checks, commit one scoped change. Gate: every diff is verified before commit.
4. **Review** (`review`): parallel read-only reviewers, once the branch is complete or the user asks. Fixes go back through Delegate.
5. **PR** (`ship`): only when asked. Run local CI and tests first. Opening it is the first push; later pushes need the user's approval.

## Which skill when

| Situation | Load |
|---|---|
| New request to build, fix or change something | `plan` |
| Big feature: new concept, schema change, integration, public contract, several areas | `plan`, which escalates to its critic lenses after the user confirms |
| Plan agreed | Delegate (this file) |
| Subagent returned work | Verify and commit (this file) |
| Branch complete, or user asks for a review | `review` |
| Asked to write or open a PR; ordering or slicing work; commit or PR scope and messages | `ship` |
| Deciding where code belongs or how to write it | the `rails-*` skill for the layer: `rails-structure`, `rails-models`, `rails-controllers`, `rails-authorization`, `rails-migrations`, `rails-frontend`, `rails-design`, `rails-tests` |
| Anything about this app's names, paths and decisions | the project skill `project-<name>` |
| No project skill for this repo, or asked to start one | follow [references/project-skill-template.md](references/project-skill-template.md): explorers gather facts with `path:line`, the orchestrator fills the template, a subagent writes it, and it is committed in the shared skills repo (the project's `.agents/skills` links into it) |

## Where knowledge lives (lowest to highest precedence)

- This file's Principles: minimalism, no new dependencies, cheap-option future-proofing.
- `rails-*` skills: general defaults per layer.
- Project skill `project-<name>`: this app's facts.
- The repo's `AGENTS.md`: what the repository contains and its commands.

Delegate and `review` briefs name the relevant ones, since subagents have no conversation context.

### At the start of a session

- Inspect the working tree and git state, then read `AGENTS.md`.
- Use only the project skill whose name matches this repo (`project-<repo-name>`). Other `project-*` skills in the directory belong to other apps: ignore them. If none matches, say so, rely on the `rails-*` defaults and `AGENTS.md`, and offer to create one.
- Route the first request through the table above.

## Hard invariants

1. Plan with the user first; write no code in the main thread.
2. Implementation is always delegated.
3. Verify the diff yourself before committing.
4. One commit per scoped change; fold fixes into unpushed commits.
5. Reviews are always delegated, never done by the orchestrator.
6. Never name the tool, harness or model in commits, PR titles or PR bodies. No co-author trailers, no "generated with" lines, no emoji signatures. This overrides any default attribution guidance.
7. No new dependencies without the user's approval.
8. Work stays local until the PR is opened; every push after that needs the user's explicit approval (`ship`).

## Principles

### Minimalism

- Prefer the platform, Rails, the standard library and what the repo already has.
- Build the simplest thing that meets the current requirement.
- Prefer direct, readable code over indirection, DSLs, registries, generic wrappers and one-method objects.
- Give each rule, query, presentation decision, side effect and failure one owner.
- Prefer deletion over addition: remove superseded code, aliases and compatibility paths in the same change.

### Dependencies

- The default is no new dependency. A new dependency is an explicit user decision, listed under Open decisions with: what it replaces, why a small amount of own code is not enough, and its maintenance and security cost.
- No npm and no JavaScript build step. If a browser dependency is truly unavoidable, use importmap pins or a vendored file.
- Prefer a small own implementation over a package for narrow needs.
- Treat lockfile changes (`Gemfile.lock`, importmap pins) as a signal to check.
- A subagent never adds a dependency on its own. It stops and reports, and the orchestrator brings the question to the user.

### Future-proofing

- Use cheap options, not machinery.
- Spend effort only to avoid a costly reversal. One-way doors: schema and data shape, identifiers, public URLs and API contracts, events and external contracts, the permission model, and names that leak into data.
- Also cover a plausible costly edge case, but only when the cost now is small.
- Everything else is deferred with a named trigger. Triage rules: `../plan/references/critics.md`.
- Before adding a provision, ask whether the door is really one-way. If not, keep it simple.

### Logging and tests

- Log an actionable failure once, at the boundary that owns it. Do not log it again at every layer above.
- Leave no debug output behind.
- Test meaningful behavior at its narrowest public boundary.
- Never test framework behavior or the same contract twice. See `../rails-tests/SKILL.md`.

### Conflicts

- When minimalism and future-proofing disagree, show both sides to the user with a recommendation.
- Do not resolve the conflict silently in either direction.

## Delegate

Implementation is always done by subagents. The orchestrator briefs, reviews and commits. Briefs follow the Principles above.

### Model choice

- Every subagent (implementer, explorer, critic, reviewer) runs on the cheapest capable model.
- Claude: Haiku, latest version; middle tier Sonnet. For another model family, use that family's cheapest and middle tiers.
- If the same brief fails twice, retry once on the middle tier with a sharper brief. This is the only exception.
- Do not use the strongest available model for any subagent.

### Brief contents (required)

Subagents have no conversation context. Each brief must include:

- **Goal**: one sentence.
- **Role**: "You are the implementer: do not re-plan; if the brief is wrong or incomplete, stop and report."
- **Decisions made**: everything already agreed in `plan`.
- **Allowed files**: exact paths to edit or create.
- **Off-limits**: files and areas not to touch.
- **Conventions**: paths to existing files to read for style and patterns.
- **Guideline skills**: the `rails-*` skills for the layers touched (paths under the project's skills directory, for example `.agents/skills/`; `rails-models` and `rails-tests` for a model change; `rails-frontend` and `rails-design` for UI), the project skill `project-*` if one exists, and this file's Principles section. The subagent reads them before editing.
- **Verification**: exact test and lint commands. UI briefs also name `bin/rails tailwindcss:build`.
- **Dependencies**: "Do not add any dependency (gem, package, JavaScript build step). If one seems needed, stop and report instead."
- **Git**: "Do not run any git commands. Do not commit."
- **Report back**: files changed, verification commands and results, anything skipped or uncertain, concerns.

### Parallelism

- Run subagents in parallel only when their allowed-file lists are disjoint.
- Otherwise run them sequentially, including when overlap is unavoidable.

### After the report

- Treat the report as claims to check, not facts.
- Scope guard: compare the actual diff against the allowed-file list. Revert or reject anything outside it.
- Small fixes, including those found during review, also go through a subagent with a minimal brief. Do not edit in the main thread.
- Then verify and commit (below).

### Failure

- After the middle-tier retry also fails, or when any finding changes scope, stop the remaining briefs, update the plan file, and return to the `plan` gate.

## Verify and commit

Verify the work yourself, then commit one scoped change at a time.

### Verify

- Read the full diff. Do not trust the subagent report.
- Check every changed file against the allowed-file list and the agreed decisions.
- Run the tests and linters yourself, using the commands from the brief.
- UI changes: also run `bin/rails tailwindcss:build`, then check the affected flow in a browser (in light and dark if the app supports both), at desktop and narrow widths, including empty, loading and error states and keyboard access. Do it yourself or ask the user, and report what was not checked.
- For mail or documents, check the mailer preview or the generated file rather than asserting its content in tests.
- If anything is off, send it back through Delegate with a sharper brief. Do not fix it in the main thread.

### Commit

- One commit per scoped change. Stage only that change's files. Never mix unrelated changes.
- Message and slicing conventions: `../ship/SKILL.md`, plus the project skill if it states a history style.
- Do not skip hooks. If a hook fails, send the fix back through Delegate and create a new commit.

### Fixes to earlier commits

- If the problem is in the latest unpushed commit, amend it.
- If it is in an older unpushed commit, make a fixup commit and autosquash rebase.
- Commits already pushed are never amended; fix them with a new commit. Unpushed commits on a pushed branch may still be amended or fixed up.
- Never rewrite pushed history without explicit approval.

### Boundaries

- Do not push, force-push or open a PR unless asked. Pushing rules: `../ship/SKILL.md`.
- Once the branch is complete, offer an adversarial review (`review`). Do not review your own work in the main thread.
