---
name: plan-edge-cases
description: Use when critiquing a plan before implementation for failure modes and unusual states it does not handle, such as races, double submits, retries, partial failure, deletion, tenant boundaries, time zones and existing records. Covers only failure and edge states.
---

# Plan Edge Cases

Find failure modes and unusual states the plan does not handle, and name the smallest handling or the explicit decision to accept the risk.

## Scope

- This lens covers only failure modes and unusual states: what happens when inputs, timing or external systems go wrong or are unusual.
- Leave scope creep, reversibility of data decisions, repo fit and naming to the other plan lenses and do not report them.
- Read the plan file, the fact sheet and the repo guidelines (AGENTS.md, CLAUDE.md or equivalent) you were pointed to before critiquing.

## What to look for

- Concurrency and races: two requests changing the same record, double submits, and jobs or retries running twice.
- Idempotency of retries, jobs and webhooks.
- Partial failure across steps or external calls, where one step succeeds and the next does not.
- Empty, nil, huge and duplicate data.
- Ordering and timing assumptions, and time zones and dates.
- Permission and tenant boundaries: who can see or change what.
- Deletion, archiving and records referenced elsewhere.
- External service failure, timeouts and rate limits.
- Migration of existing data, and how the change behaves for existing records.

## What is NOT an observation

- Implausible edge cases. Rank by plausibility times cost of failure, and drop anything that cannot reach a plausible state.
- Cases the plan already handles explicitly, or that the platform or framework guarantees.
- Hardening of paths that are internal and cannot be reached with the inputs the plan states.
- Handling that costs more than the failure it prevents, unless the plan should make that trade-off explicitly.

## Report

- Return observations exactly as specified in `../plan-feature/references/observation-format.md`. Observations only; never rewrite the plan.
- Each observation includes a concrete scenario: the state or inputs that lead to the wrong outcome. Rank observations by plausibility times cost of failure.
- Suggest the smallest handling: a constraint, guard, transaction, idempotency key, or an explicit line in the plan accepting the risk.
- Stay read-only: do not edit files, run git, or change state. Work from the plan file, fact sheet and repo guidelines only, without any conversation context.
- Try to falsify each observation first by checking whether the scenario can actually occur given the plan's stated flow and existing guards. Drop it if it cannot.
