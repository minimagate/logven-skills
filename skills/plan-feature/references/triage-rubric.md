# Triage Rubric

Every observation gets exactly one label. Record the label and a one-line reason in the plan's Triage section.

## Labels

- **Adopt**: change the base plan. Use when the observation fixes a real defect or removes unneeded scope, and you have confirmed it against the code.
- **Cheap hook**: add a small provision now that keeps a door open, such as a nullable column, an index, a constraint, a name, or an explicit boundary. Use only when cost_now is low and cost_later is high.
- **Defer with trigger**: do not build it. Record it in the Deferred ledger. Use when cost_later is acceptable or likelihood is low.
- **Reject**: overengineering or out of scope. Give a one-line reason.

## Decision test

Apply the rules in order. The first match wins.

| Order | Condition | Label |
|---|---|---|
| 1 | Verified defect, or unneeded scope the requirement does not need | Adopt |
| 2 | Out of scope, proposes machinery the requirement does not need, or an implausible edge case (likelihood low and the failure is minor) | Reject |
| 3 | cost_now low, cost_later high, likelihood not low | Cheap hook |
| 4 | One-way door with cost_now medium or high and likelihood medium or high | Defer with trigger, and list it under the user's decisions with your recommendation |
| 5 | Anything else | Defer with trigger |

## One-way doors and two-way doors

- **One-way door**: reversing it later is costly. Schema and data shape, identifiers, public URLs and API contracts, events and external contracts, the permission model, and names that leak into data.
- **Two-way door**: everything else. Internal structure, helpers and abstractions can change cheaply later.

## Edge cases

- Rank each edge case by plausibility times cost of failure.
- Implausible edge cases are rejected, not deferred. Deferring them keeps them alive in the ledger for no reason.
- Plausible edge cases that are cheap to handle later are deferred with a trigger.

## Default

When unsure, defer with trigger. Do not guess a Cheap hook or an Adopt without evidence.

## Deferred ledger entry

One entry per deferred item, in this form:

```
- What: <the thing that is not being built>
  Why deferred: <cost_later is acceptable, or likelihood is low>
  Trigger: <the concrete condition that would make us build it>
```
