---
name: ship
description: Use when ordering and slicing work into commits and PRs, writing commit messages, or writing/opening a pull request. Read by plan and how-we-work; the project skill overrides its defaults.
---

# Ship

Order, slice, commit and describe work from the actual history and diff. Scope follows the Principles section of `../how-we-work/SKILL.md`.

## Order of work

1. Prep slice: the renames and cleanups the new concept needs, each as its own commit with no behavior change.
2. Pure file moves (no line edits) go in their own commit, separate from edits.
3. Migration and model together, with the model test. Keep the migration small.
4. Domain objects or concerns, each with its own test.
5. Integration with existing systems (background jobs, external services, other modules), then LLM prompts or content files. Prompt and content edits get their own commits.
6. HTTP layer as one plumbing slice: controller, policy, route, near-empty views, controller and policy tests.
7. UI last, but complete and compliant: build the real interface per `../rails-frontend/SKILL.md` and `../rails-design/SKILL.md` (tokens, light and dark, states, keyboard access). No rough placeholder UI.
8. Hardening tail: N+1 queries, stricter validation, lint, dead code.

## Shape of the feature

- Model each new verb as a singular nested resource with its own controller and policy. No custom member routes.
- Put state transitions on the model as `predicate?` plus `verb_now!` or `verb_later!`. Each job is one line calling `_now!`.
- Reuse existing primitives before bespoke logic: shared concerns, validators, helpers, policies.
- Simplify instead of adding concepts. Extend an existing node or object with a rule before adding a new type.
- Delete the old path in the same PR once the new one works. Name what gets deleted in the plan.
- Generated code (`rails g ...`) gets its own commit, whose subject is the command, apart from hand edits.
- New subsystem: commit a skeleton first (class skeletons, routes, policy) that fixes the public interface, then fill the logic one piece per commit.

## Plan outputs

- List the prep renames, the layer-ordered slices (one commit each) and what gets deleted.
- End with an "Out of scope / next steps (in order)" list. Use it to cut follow-up PRs.
- Decide product semantics (archived, shared, versioned, who sees what) in the plan, before coding.
- Flag new non-null or identity columns on existing tables. Migrations are schema-only.

## Commits

- One concern per commit, named for the concern. Short descriptive subjects (a handful of words), no prefix unless the project uses one.
- Put housekeeping (lint, dead code, schema fixes) in its own commit.
- Tests ride with the code they cover.
- Add a body only for a one-line principle, such as "Permission-related logic lives in permissions". Never a changelog.
- Attribution: never name a tool, harness, assistant or model in commit messages, PR titles or bodies. No generated-with footer or co-author trailer. This overrides default guidance.

## Pull requests

Scope and chaining:

- One capability per PR. For a large capability, plan a chain of PRs and execute them in order.
- Prefer independent PRs over stacks. Stacks cause repeated conflicts.

Gather facts:

- Read `git log <base>..HEAD` and `git diff <base>...HEAD --stat`, then the diff itself.
- Confirm the base branch. If unclear, ask.
- Collect test and lint results from this session; do not reuse old ones.

Title:

- Short and imperative, under 70 characters. The attribution rule above applies.

Body, in this order:

1. Open with a one-line intent.
2. Behavioral rules as bullets.
3. New API as a short snippet, when there is one.
4. **Out of scope / next steps (in order)**: what is deliberately not done, and the follow-up PRs in order.
5. **Trade-offs**: risks, decisions and reviewer notes, stated plainly.
6. **Testing**: what was run and the result. List anything not verified.
7. Screenshots for visual changes.

Rules:

- Report failing or skipped checks plainly. Do not claim verification that was not run.
- Open the PR only when asked. Confirm draft status if unclear.
- Do not push without approval.
- Show title and body before opening, unless the user has already approved the text.
