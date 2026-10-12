---
name: review-over-standardisation
description: Use when reviewing a diff for premature sharing, where code is extracted or unified across callers that should be free to diverge. Covers only coupling from shared abstractions and over-uniformity, and also reports real drift between copies.
---

# Review Over-Standardisation

Find shared abstractions and uniformity in the diff that couple things which should be free to diverge, and the rare case where a copy has real drift.

## Scope

- This lens covers only sharing and uniformity: shared bases, concerns, partials, helpers, components, utilities and common modules.
- This lens is meant to sometimes disagree with `review-overengineering`. Report both sides of a tension honestly instead of hedging.
- Leave pure machinery, correctness, conventions and hygiene to other lenses and do not report them.
- Read the repo guidelines (AGENTS.md, CLAUDE.md or equivalent) you were pointed to before reviewing.
- Review only the diff scope you were given, plus the code that the diff touches.

## What to look for

- Shared base classes, concerns, partials, helpers or components extracted from two or fewer real callers (rule of three).
- Shared code that gains flags, conditionals or optional parameters to serve its different callers.
- Look-alike code that belongs to different domains, changes for different reasons or is likely to diverge, such as two screens, two integrations or two policies.
- A cross-cutting change forced through one shared abstraction when each caller needs a different outcome.
- Renames or restructures done only to make things look uniform across the codebase.
- A "common" or "shared" module that many unrelated places now depend on.
- The opposite case: a copy that now exists three or more times in the repo and has started to drift in behaviour. Report it as under-sharing.

## What is NOT a finding

- A few lines of duplication that cost less than the coupling a shared helper would add.
- Sharing that the framework or the repo guidelines require.
- Two copies that are identical by design and are expected to change together, when the diff makes that explicit.
- Under-sharing where the copies are identical and have no drift and no third caller.
- Personal taste about whether a helper should exist, without a concrete divergence or coupling cost.

## Report

- Return findings exactly as specified in `../review/references/finding-format.md`.
- For each over-sharing finding, name the shared unit, list its callers, and state the concrete way they diverge or the flag they force.
- For each under-sharing finding, list every copy with its path and the specific drift.
- Stay read-only: do not edit files, run git, or change state.
- Try to falsify each finding first by checking whether the callers really diverge or whether the copies really drift. Drop it if they do not.
