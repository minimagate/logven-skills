---
name: plan-simplicity
description: Use when critiquing a plan before implementation for scope and machinery beyond the stated requirement, such as non-goals creeping in, speculative options or layers, bundled slices and new dependencies. Covers only scope and machinery.
---

# Plan Simplicity

Find scope and machinery in the plan that the stated requirement does not justify, and name the simpler direct form or the cut.

## Scope

- This lens covers only scope and machinery: what the plan builds beyond the requirement, and the layers, options and dependencies it adds to do so.
- Leave failure modes, reversibility, repo fit and naming to the other plan lenses and do not report them.
- In revision mode, the lens also runs a one-pass bloat check: compare the revised plan against the original requirement and flag anything triage added that `../plan-feature/references/triage-rubric.md` does not justify.
- Read the plan file, the fact sheet and the repo guidelines (AGENTS.md, CLAUDE.md or equivalent) you were pointed to before critiquing.
- Apply `../principles/SKILL.md`, especially its Dependencies section.

## What to look for

- Non-goals that the plan quietly brings back in as steps or slices.
- Speculative options, config keys, hooks, feature flags or providers that no stated requirement uses.
- New layers, classes, services or concerns where an existing owner or a plain method would do.
- Slices that bundle unrelated work under one heading.
- Steps that exist only for hypothetical future needs.
- Gold-plating of edge cases the requirement does not mention.
- New dependencies (gems, npm packages, JavaScript build steps) without a stated reason that existing code, Rails or a small own implementation cannot do the job.

## What is NOT an observation

- Complexity the requirement demonstrably demands, such as a stated concurrency, security or integration constraint.
- A cheap hook that the future-proofing lens would justify. Note the tension briefly in the observation rather than hiding it.
- Preference for a different but equally simple shape. Only report when the simpler form is clearly less machinery.

## Report

- Return observations exactly as specified in `../plan-feature/references/observation-format.md`. Observations only; never rewrite the plan.
- For each observation, name the machinery or step, state why the requirement does not need it, and suggest the simpler direct form or the cut.
- Stay read-only: do not edit files, run git, or change state. Work from the plan file, fact sheet and repo guidelines only, without any conversation context.
- Try to falsify each observation first by checking the requirement and the repo for a real need. Drop it if one exists.
