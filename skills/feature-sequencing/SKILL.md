---
name: feature-sequencing
description: Use when ordering or slicing a feature into commits and PRs, or writing Logven commit messages and PR descriptions. Read by plan, plan-feature and verify-and-commit for layer order, plumbing slices, commit naming and PR scope.
---

# Feature Sequencing

Order, slice and describe a feature the way Logven history does: bottom-up, one concern per commit, UI last. Follow `../principles/SKILL.md` for scope.

## Order of work

1. Prep slice: the renames and cleanups the new concept needs, each as its own commit with no behavior change.
2. Pure file moves (no line edits) go in their own commit, separate from edits.
3. Migration and model together, with the model test. Keep the migration small.
4. Domain objects or concerns, each with its own test.
5. Integration with existing systems (runner, builder, jobs), then prompts. Prompt `.md` edits get their own commits.
6. HTTP layer as one plumbing slice: controller, policy, route, near-empty views, controller and policy tests.
7. UI last and minimal. Say in the PR description when it is rough.
8. Hardening tail: N+1 queries, stricter validation, "Testing everything", lint, dead code.

## Shape of the feature

- Model each new verb as a singular nested resource with its own controller and policy. Do not add custom member routes.
- Put state transitions on the model as `predicate?` plus `verb_now!` or `verb_later!`. Each job is one line calling `_now!`.
- Reuse existing primitives before bespoke logic: Shapes, `Meterable`, chat helpers, `turbo_id`, policies.
- Simplify instead of adding concepts. Extend an existing node or object with a rule before adding a new type.
- Delete the old path in the same PR once the new one works. Name what gets deleted in the plan.
- Generated code (`rails g ...`) gets its own commit, whose subject is the command, kept apart from hand edits.
- When opening a new subsystem, commit a skeleton first (class skeletons, routes, policy) that fixes the public interface. Then fill the logic one piece per commit.

## Plan outputs

- List the prep renames, the layer-ordered slices (one commit each) and what gets deleted.
- End with an "Out of scope / next steps (in order)" list. Use it to cut follow-up PRs.
- Decide product semantics (archived, shared, versioned, who sees what) in the plan, before coding.
- Flag new non-null or identity columns on existing tables. Migrations are schema-only.
- For LLM features, write validation rules and clear messages first, then prompts, then evals outside CI.

## Commits

- One concern per commit, named for the concern. Subjects are short, 2-6 words, with no conventional-commit prefix.
- Put housekeeping (lint, dead code, schema fixes, brakeman) in its own commit.
- Tests ride in the same commit as the code they cover. A batch "Testing everything" commit after a plumbing slice is acceptable.
- Add a body only for a one-line principle, such as "Permission-related logic lives in permissions". Never a changelog.

## Pull requests

- One capability per PR. For a large capability, plan a chain of PRs and execute them in order.
- Prefer independent PRs over stacks. Stacks cause repeated conflicts.
- Open with a one-line intent, then the behavioral rules as bullets.
- Show the new API in a short snippet when there is one.
- Include "Out of scope" and "To do / next steps (in order)".
- State trade-offs plainly. Give test or eval results.
- Explain the problem, the resulting behavior and the validation. Add screenshots for visual changes.
