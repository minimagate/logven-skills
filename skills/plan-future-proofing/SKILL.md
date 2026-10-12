---
name: plan-future-proofing
description: Use when critiquing a plan before implementation for decisions that are expensive to reverse, such as schema shape, identifiers, public URLs, API contracts, events, the permission model and names that leak into data. Covers only reversibility.
---

# Plan Future-Proofing

Find decisions in the plan that are expensive to reverse, and name the cheapest provision that keeps the door open, or say the door is two-way and should stay simple.

## Scope

- This lens covers only reversibility: schema and data shape, identifiers, public URLs and API contracts, events and external contracts, the permission model, and names that leak into data.
- Leave scope creep, failure handling, repo fit and naming conventions to the other plan lenses and do not report them.
- Read the plan file, the fact sheet and the repo guidelines (AGENTS.md, CLAUDE.md or equivalent) you were pointed to before critiquing.

## What to look for

- One-way doors in the plan, and whether each one is chosen deliberately.
- Cheap provisions that keep a door open at small cost now: a nullable column, an index, a unique constraint, an explicit boundary, or a name that will not mislead later.
- Assumptions baked into data shape: single tenant, single currency, single provider, implied ordering, or a cardinality of "one" that may become "many".
- Places the plan couples things that are likely to diverge, such as two concerns sharing one table, field or endpoint.
- Migrations that would be painful on real existing data.

## What is NOT an observation

- Speculative abstraction in cheap-to-change internal code.
- Building for futures with no plausible trigger.
- Any suggestion where the cost now is high and the likelihood of the future is low.
- A two-way door that the plan already treats as two-way. Say it is safe to leave simple instead of raising it.
- A new dependency proposed as future-proofing. Dependencies are never a cheap hook; see `../principles/SKILL.md`.

## Report

- Return observations exactly as specified in `../plan-feature/references/observation-format.md`. Observations only; never rewrite the plan.
- For each observation, state the cost now and the cost later honestly. Say when the answer is to leave it simple because it is a two-way door.
- Propose the smallest provision, or a deferral with its named trigger. Never propose machinery.
- Stay read-only: do not edit files, run git, or change state. Work from the plan file, fact sheet and repo guidelines only, without any conversation context.
- Try to falsify each observation first by checking whether the door is really one-way (for example, the data is not yet persisted or can be migrated cheaply) and whether the trigger is plausible. Drop it if not.
