---
name: plan-feature
description: Multi-agent planning for big features the user confirms: new domain concept, schema change, external integration, public contract, or work across several areas. Runs parallel explorers and critics, triages to a lean plan, then hands off to delegate. Small changes use plan.
---

# Plan Feature

Plan a large feature with parallel read-only explorers and critics, then cut the result down to the simplest plan that meets the requirement.

## Core principle: future-proof means cheap options, not machinery

- Spend effort now only to avoid a costly reversal. One-way doors: schema and data shape, identifiers, public URLs and API contracts, events and external contracts, the permission model, names that leak into data.
- Also spend effort on a plausible, costly edge case, but only when the cost now is small.
- Anything cheap to change later (internal structure, helpers, abstractions) stays as simple as possible.
- Everything else is recorded as deferred, not built.
- Apply the test in `references/triage-rubric.md`.
- Follow `../principles/SKILL.md`; a new dependency is never a cheap hook.

## Flow

1. **Confirm.** Get the user's agreement to the multi-agent run, because it costs tokens. State what will run: how many explorers, how many critics, and which model tier. Do not start without a yes.

2. **Explore.** Dispatch several read-only explorers in parallel on the cheapest capable model (Claude: Haiku).
   - Give each a self-contained brief: one area to map (current code, callers, schema, tests, repo guidelines such as AGENTS.md or CLAUDE.md), the requirement, and a read-only instruction.
   - Explorers return facts with `path:line` and no opinions.
   - Merge the results into one fact sheet. Drop duplicates and any claim without a `path:line`.

3. **Base plan.** The orchestrator drafts the simplest plan that satisfies the stated requirement, in dialogue with the user.
   - Write it to `tmp/plans/<slug>.md` in the project. Keep it untracked.
   - Sections, in order: Goal, Non-goals, Decisions, Slices, Triage, Deferred ledger. Triage and Deferred ledger stay empty until step 5.
   - Each slice is commit-sized and lists its files. Slices must have disjoint files.
   - The slice order follows `../feature-sequencing/SKILL.md`: prep slice first, bottom-up layers, plumbing slice, UI last, and an Out-of-scope list.

4. **Critics.** Dispatch four read-only critics in parallel on the strongest available model (Claude: Opus), one per lens: `plan-simplicity`, `plan-future-proofing`, `plan-edge-cases`, `plan-fit`.
   - Brief each with: its lens skill, the plan file path, the fact sheet, repo guideline paths, a read-only instruction, and `references/observation-format.md`.
   - Critics return observations only. They never rewrite the plan.

5. **Triage.** Label every observation Adopt, Cheap hook, Defer with trigger, or Reject, using `references/triage-rubric.md`. Record each label in the plan's Triage section.
   - Spot-check doubtful observations against the code before accepting them.
   - Where critics conflict (usually simplicity against future-proofing), show both sides to the user with your recommendation. Never resolve it silently.
   - Write each deferred item into the Deferred ledger with its trigger.

6. **Bloat check.** Run one pass only. Send the revised plan to a `plan-simplicity` critic to catch plan creep introduced by triage. Apply or reject each cut and record the decision. Do not loop again.

7. **Present and gate.** Show the user the revised plan, the triage table, the deferred ledger, and the decisions that are theirs.
   - Wait for explicit agreement. Approval covers the plan as written.
   - If scope, files or decisions change after approval, re-plan and get agreement again.

8. **Hand off.** The approved slices become the briefs for `delegate`, one commit per slice. The plan file is the source for those briefs: copy from it, do not retype it.

## Briefs

- Every explorer and critic brief is self-contained. Subagents have no conversation context.
- Each brief names the exact files or directories to read, the requirement in full, and the read-only instruction.
- Each critic brief also names its lens skill and `references/observation-format.md`, and asks for that format and nothing else.
- Each explorer brief asks for facts with `path:line` and says that opinions will be discarded.
- Paste the same requirement text into every brief. Do not paraphrase it between agents.

## Presenting to the user

- Lead with the decisions that are theirs, each with your recommendation.
- Then the revised plan, the triage table (observation, label, one-line reason), and the Deferred ledger.
- Name the model tiers and the number of agents that ran, so cost is visible.

## Rules

- The orchestrator writes no code in this phase.
- Explorers and critics are read-only. Reject any output that edits files.
- Do not dump raw critic output on the user. Present the triaged result.
- Keep the plan short. If it grows past about one page, cut it before presenting it.
- Name the default for every open question you resolve yourself.
- Stop at one bloat pass, even if the critic finds more. Surface the rest as a user decision.
