---
name: plan-fit
description: Use when critiquing a plan before implementation for how it fits the existing repo, such as misplaced code, duplicated helpers, conflicts with AGENTS.md or CLAUDE.md rules, slice ordering and missing test plans. Covers only repo fit.
---

# Plan Fit

Check how the plan fits the existing repo: where its code belongs, what it duplicates, which repo rules it breaks, and whether its slices are ordered and sized to review and delegate.

## Scope

- This lens covers only repo fit: placement, reuse of existing code and patterns, repo rules, and how the plan slices and orders the work.
- Leave scope creep, failure modes and reversibility of data decisions to the other plan lenses and do not report them.
- Read the plan file, the fact sheet and the repo guidelines (AGENTS.md, CLAUDE.md or equivalent) you were pointed to before critiquing, then look at the sibling code the plan touches.

## What to look for

- New code placed where the repo does not put equivalent code.
- Existing code, patterns or helpers that the plan duplicates instead of reusing.
- Conflicts with rules in AGENTS.md, CLAUDE.md or repo docs. Quote the rule.
- A second way of doing something the repo already does one way.
- Naming and placement that differ from sibling files.
- Slices ordered so that one depends on a later slice.
- Slices too large to review as one commit, or slices touching overlapping files that prevent parallel delegation.
- A missing test plan relative to the repo's testing rules.

## What is NOT an observation

- Taste without repo backing.
- Legacy patterns the repo is moving away from, whether documented or evident in recent code.
- Placement that the plan explicitly justifies with a reason that holds.

## Report

- Return observations exactly as specified in `../plan-feature/references/observation-format.md`. Observations only; never rewrite the plan.
- Every observation cites a repo path:line or a quoted rule.
- For each observation, name the existing code or rule and suggest the placement, reuse or reordering that fits.
- Stay read-only: do not edit files, run git, or change state. Review the plan, not the code, without any conversation context.
- Try to falsify each observation first by confirming the cited path and line still say what the observation claims, and that the pattern is not already superseded. Drop it if not.
