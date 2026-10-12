# Critics

## How every critic works

- Read the plan file, fact sheet and guideline paths you were given (AGENTS.md, CLAUDE.md, `rails-*`, `project-*`).
- Report observations only, in the Observation format below. Never rewrite the plan.
- Read-only: do not edit files, run git or change state. You have no conversation context.
- Falsify first against the requirement, the repo and the cited code. Drop what fails; if an observation survives, say what you checked.
- Stay in your lens.

## Simplicity

Lens: scope and machinery only. Find what the plan builds beyond the requirement.

Look for:
- Non-goals that the plan quietly brings back as steps or slices.
- Speculative options, config keys, hooks, feature flags or providers that no stated requirement uses.
- New layers, classes, services or concerns where an existing owner or a plain method would do.
- Slices that bundle unrelated work under one heading.
- Steps that exist only for hypothetical future needs.
- Gold-plating of edge cases the requirement does not mention.
- New dependencies (gems, npm packages, JavaScript build steps) without a reason that existing code, Rails or a small own implementation cannot meet. See `../../how-we-work/SKILL.md` (Principles, Dependencies).

Not an observation:
- Complexity the requirement demonstrably demands, such as a stated concurrency, security or integration constraint.
- A cheap hook that the Future-proofing lens would justify. Note the tension briefly in the observation rather than hiding it.
- A different but equally simple shape. Report only when the simpler form is clearly less machinery.

Report:
- For each observation, name the machinery or step, state why the requirement does not need it, and suggest the simpler direct form or the cut.
- Revision mode (bloat check): against the original requirement, flag anything triage added that the Triage rubric does not justify.

## Future-proofing

Lens: reversibility only. Find decisions that are expensive to reverse.

Look for:
- One-way doors in the plan, and whether each one is chosen deliberately.
- Cheap provisions that keep a door open: a nullable column, an index, a unique constraint, an explicit boundary, or a name that will not mislead later.
- Assumptions baked into data shape: single tenant, single currency, single provider, implied ordering, or a cardinality of "one" that may become "many".
- Things the plan couples that are likely to diverge, such as two concerns sharing one table.
- Migrations that would be painful on real existing data.

Not an observation:
- Speculative abstraction in cheap-to-change internal code.
- Building for futures with no plausible trigger.
- Any suggestion where the cost now is high and the likelihood of the future is low.
- A new dependency proposed as future-proofing. Dependencies are never a cheap hook (`../../how-we-work/SKILL.md`).

Report:
- State the cost now and the cost later honestly. For a two-way door the plan already treats as two-way, say it is safe to leave simple instead of raising it.
- Propose the smallest provision, or a deferral with its named trigger. Never propose machinery.
- Falsify: check the door is really one-way (not yet persisted, or cheaply migratable) and the trigger is plausible.

## Edge cases

Lens: failure modes and unusual states only. Find what the plan does not handle when inputs, timing or external systems go wrong.

Look for:
- Concurrency and races: two requests changing the same record, double submits, jobs or retries running twice.
- Idempotency of retries, jobs and webhooks.
- Partial failure across steps or external calls, where one step succeeds and the next does not.
- Empty, nil, huge and duplicate data.
- Ordering and timing assumptions, and time zones and dates.
- Permission and tenant boundaries: who can see or change what.
- Deletion, archiving and records referenced elsewhere.
- External service failure, timeouts and rate limits.
- Migration of existing data, and how the change behaves for existing records.

Not an observation:
- Implausible edge cases: drop anything that cannot reach a plausible state.
- Cases the plan already handles explicitly, or that the platform or framework guarantees.
- Hardening of internal paths that cannot be reached with the inputs the plan states.
- Handling that costs more than the failure it prevents, unless the plan should make that trade-off explicitly.

Report:
- Each observation names a concrete scenario: the state or inputs that cause the wrong outcome.
- Rank by plausibility times cost of failure.
- Suggest the smallest handling: a constraint, guard, transaction, idempotency key, or an explicit line in the plan accepting the risk.
- Falsify by checking whether the scenario can occur given the plan's flow and existing guards.

## Fit

Lens: repo fit only: placement, reuse, repo rules, and whether slices are ordered and sized to review and delegate. Read the plan and guidelines, then the sibling code it touches. Critique the plan, not the code.

Look for:
- New code placed where the repo does not put equivalent code.
- Existing code, patterns or helpers that the plan duplicates instead of reusing.
- Conflicts with rules in AGENTS.md, CLAUDE.md or repo docs. Quote the rule.
- A second way of doing something the repo already does one way.
- Naming and placement that differ from sibling files.
- Slices ordered so that one depends on a later slice.
- Slices too large to review as one commit, or slices touching overlapping files that prevent parallel delegation.
- A missing test plan relative to the repo's testing rules.

Not an observation:
- Taste without repo backing.
- Legacy patterns the repo is moving away from, whether documented or evident in recent code.
- Placement the plan explicitly justifies with a reason that holds.

Report:
- Every observation cites a repo `path:line` or a quoted rule.
- Name the existing code or rule, and suggest the placement, reuse or reordering that fits.
- Falsify by confirming the cited path and line still say what the observation claims, and that the pattern is not already superseded.

## Observation format

Return observations in this format only.

Fields, in this order:
- `lens`: `simplicity` | `future-proofing` | `edge-cases` | `fit`.
- `kind`: `cut` | `one-way-door` | `edge-case` | `fit` | `risk`.
- `plan_ref`: the plan section or slice it concerns, for example `Slices 2` or `Decisions: id format`.
- `claim`: one sentence stating the problem or the opportunity.
- `evidence`: `path:line` in the code, or quoted plan text.
- `cost_now`: `low` | `medium` | `high`, with a few words of reason.
- `cost_later`: what it costs to fix after shipping, `low` | `medium` | `high`, with a few words of reason.
- `likelihood`: `low` | `medium` | `high` that it matters.
- `suggestion`: the smallest action, or `none, plan is fine`.

Rules:
- Cite evidence for every claim. An observation without evidence is dropped.
- No praise and no restating the plan.
- If there is nothing to report, reply `No observations` and list what you checked.
- Cap at 12 observations, most important first.

Example:

```
- lens: future-proofing
  kind: one-way-door
  plan_ref: Slices 1 (schema)
  claim: The new `reports` table uses the auto-increment id as the public identifier, so it will leak row counts and cannot move to UUIDs later without breaking shared links.
  evidence: `db/migrate/20260901_create_reports.rb:4` uses the default integer primary key, and Slice 4 exposes `/reports/:id` publicly.
  cost_now: low, a `uuid` column and one index in the same migration.
  cost_later: high, public links would need a redirect table and a data migration.
  likelihood: medium, the plan makes reports shareable by link.
  suggestion: Add a non-null `uuid` with a unique index in Slice 1; route public links through it.
```

## Triage rubric

Every observation gets exactly one label.

Labels:
- **Adopt**: change the base plan. Use when the observation fixes a real defect or removes unneeded scope, and you have confirmed it against the code.
- **Cheap hook**: add a small provision now that keeps a door open (see Future-proofing). Use only when cost_now is low and cost_later is high.
- **Defer with trigger**: do not build it. Record it in the Deferred ledger. Use when cost_later is acceptable or likelihood is low.
- **Reject**: overengineering or out of scope. Give a one-line reason.

Decision test. Apply the rows in order; the first match wins.

| Order | Condition | Label |
|---|---|---|
| 1 | Verified defect, or unneeded scope the requirement does not need | Adopt |
| 2 | Out of scope, proposes machinery the requirement does not need, or an implausible edge case (likelihood low and the failure is minor) | Reject |
| 3 | cost_now low, cost_later high, likelihood not low | Cheap hook |
| 4 | One-way door with cost_now medium or high and likelihood medium or high | Defer with trigger, and list it under the user's decisions with your recommendation |
| 5 | Anything else | Defer with trigger |

One-way and two-way doors:
- **One-way door**: reversing it later is costly. The list is in `../../how-we-work/SKILL.md` (Principles, Future-proofing).
- **Two-way door**: everything else, such as internal structure and helpers.

Edge cases: implausible ones are rejected, not deferred, since deferring keeps them alive in the ledger for no reason. Plausible ones cheap to handle later are deferred with a trigger.

Default: when unsure, defer with trigger. Do not guess a Cheap hook or an Adopt without evidence.

Deferred ledger entry, one per deferred item:

```
- What: <the thing that is not being built>
  Why deferred: <cost_later is acceptable, or likelihood is low>
  Trigger: <the concrete condition that would make us build it>
```
