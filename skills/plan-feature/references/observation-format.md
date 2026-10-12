# Observation Format

Every critic returns a list of observations in this format and nothing else.

## Fields

Each observation has these fields, in this order:

- `lens`: the lens that produced it (`plan-simplicity`, `plan-future-proofing`, `plan-edge-cases` or `plan-fit`).
- `kind`: `cut` | `one-way-door` | `edge-case` | `fit` | `risk`.
- `plan_ref`: the plan section or slice it concerns, for example `Slices 2` or `Decisions: id format`.
- `claim`: one sentence stating the problem or the opportunity.
- `evidence`: `path:line` in the code, or quoted plan text.
- `cost_now`: `low` | `medium` | `high`, with a few words of reason.
- `cost_later`: what it costs to fix after shipping, `low` | `medium` | `high`, with a few words of reason.
- `likelihood`: `low` | `medium` | `high` that it matters.
- `suggestion`: the smallest action, or `none, plan is fine`.

## Rules

- Observations only. Do not rewrite the plan or draft a replacement section.
- Cite evidence for every claim. An observation without evidence is dropped.
- Try to falsify each observation before reporting it. Say what you checked if it survived.
- No praise and no restating the plan.
- If there is nothing to report, reply `No observations` and list what you checked.
- Cap at 12 observations. Most important first.

## Example

```
- lens: plan-future-proofing
  kind: one-way-door
  plan_ref: Slices 1 (schema)
  claim: The new `reports` table uses the auto-increment id as the public identifier, so it will leak row counts and cannot move to UUIDs later without breaking shared links.
  evidence: `db/migrate/20260901_create_reports.rb:4` declares `create_table :reports` with the default integer primary key, and the plan's Slice 4 exposes `/reports/:id` publicly.
  cost_now: low, a `uuid` column and one index in the same migration.
  cost_later: high, public URLs and any exported links would need a redirect table and a data migration.
  likelihood: medium, the plan makes reports shareable by link.
  suggestion: Add a non-null `uuid` column with a unique index in Slice 1 and route public links through it.
```
