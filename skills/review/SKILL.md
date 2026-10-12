---
name: review
description: Run an adversarial multi-lens code review of a branch, diff, PR or named files. Use whenever the user asks for a review, or when a branch is complete. Dispatches parallel read-only reviewer subagents, one per lens, then verifies and synthesizes their findings.
---

# Review

Coordinate read-only reviewer subagents, one per lens, then verify and synthesize their findings. The orchestrator never reviews the code itself.

## Roles

- Reviews are done only by subagents on the strongest available model (Claude: Opus).
- Reviewers are read-only: no file edits, no git write commands.
- The orchestrator scopes, dispatches, verifies, filters and synthesizes.

## Scope

- Determine the exact diff: branch against its base, uncommitted changes, or the named files.
- Give every reviewer the same diff scope, as an exact command or file list.
- Give every reviewer the paths of the repo guideline files (contributor docs, style and architecture notes, agent instruction files).

## Lenses

Each lens is a skill that a reviewer reads and applies:
- `review-overengineering`
- `review-conventions`
- `review-cleanliness`
- `review-over-standardisation`
- `review-correctness`

Choose lenses by diff size and risk:
- Small diff (a few files, no logic change): conventions and cleanliness.
- Normal diff: all five.
- Large diff: all five, one reviewer per lens per area.

Dispatch one reviewer per lens in parallel. State which lenses ran and why.

## Reviewer brief

Reviewers have no conversation context, so each brief must be self-contained. Include:
- The lens skill to read and apply.
- The diff scope and the exact command that produces it.
- The guideline file paths.
- A read-only instruction: do not edit files or run git write commands.
- An instruction to try to falsify each finding before reporting it.
- The finding format from `references/finding-format.md`, and an instruction to return nothing else.

## Verification

- Spot-check every blocker and major finding, and every finding that looks doubtful, against the actual code.
- Check with a quick read yourself or a cheap subagent.
- Drop findings that do not hold up. Report how many were dropped.

## Synthesis

- Merge duplicate findings from several lenses into one, listing all lenses.
- Rank by severity. Group by file or theme.
- Surface conflicts between lenses explicitly. Example: overengineering says inline it, over-standardisation says keep it separate.
- Give a recommendation for each conflict, but leave the decision to the user.

## Output

1. Overview: verdict, counts by severity, top themes, lenses run and why.
2. Findings grouped by severity, each with `path:line`.
3. Conflicts between lenses.
4. Recommended action list.

## After the review

- Do not fix anything during review.
- Once the user picks findings, send the fixes through `delegate`.
- Re-review only the touched files, with only the relevant lenses.
- Never include tool, harness or model names in PR comments or commits.
