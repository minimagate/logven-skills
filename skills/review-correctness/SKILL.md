---
name: review-correctness
description: Use when reviewing a diff for whether it behaves correctly and safely, covering logic errors, authorization gaps, injection, race conditions, data integrity, N+1 queries, risky migrations and weak tests. Each finding needs a concrete failing scenario.
---

# Review Correctness

Find code in the diff that produces wrong results, unsafe behaviour or lost data, and prove each one with a concrete scenario.

## Scope

- This lens covers only behaviour, safety, data integrity and performance on changed paths.
- Leave style, naming, conventions, abstraction size and hygiene to other lenses and do not report them.
- Read the repo guidelines (AGENTS.md, CLAUDE.md or equivalent) you were pointed to before reviewing.
- Review only the diff scope you were given, plus the code that the diff touches.

## What to look for

- Logic errors: wrong conditions, inverted checks, off-by-one, wrong operator precedence, wrong status codes or redirects.
- Nil, empty and blank inputs that reach code without a guard on the changed path.
- Missing authentication or authorization on new or changed actions, and record lookups not scoped to the current user or tenant.
- Mass assignment of unpermitted attributes, SQL or shell injection, and unsafe `html_safe` or raw rendering of user input.
- Secrets or credentials written into code, fixtures, logs or configuration.
- Race conditions and missing transactions around multi-step writes or read-then-write logic.
- Uniqueness enforced only by a validation with no database unique index.
- Callbacks or jobs with external side effects that run before the transaction commits.
- N+1 queries and unindexed lookups on paths the diff adds or changes.
- Migrations that drop or rewrite data without a backfill, or that are not reversible when the repo expects reversibility.
- Error paths that rescue and swallow failures, or that report success after a failed step.
- Tests that would still pass if the changed code were broken, that assert only the framework's behaviour, or that do not exercise the new branch.

## What is NOT a finding

- Hypothetical failures with no plausible input or state that reaches them.
- Style, naming, structure or formatting issues.
- Performance concerns on code paths that run once, on tiny bounded data, or outside the changed paths.
- Missing checks that a framework, a type or a documented caller contract already guarantees.
- Theoretical races where the code is already serialised by a lock, a queue or a single worker.

## Report

- Return findings exactly as specified in `../review/references/finding-format.md`.
- Every finding must include a concrete failing scenario: the exact inputs or state, and the wrong output or effect that follows.
- Cite the file and line range of the faulty code and, for test findings, the test that would still pass.
- Stay read-only: do not edit files, run git, run migrations, or change state.
- Try to falsify each finding first by tracing the scenario through the real code path, including callers and validations. Drop it if the scenario cannot happen.
