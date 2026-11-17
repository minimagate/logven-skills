---
name: atlas-review
description: Review a logven branch or diff the way Paul (psguazz) would, against Atlas: invariants, extension points, active decisions, conventions and his review patterns. Use when asked for an Atlas review or a Paul-style review.
---

# Atlas review

Read the [atlas](../atlas/SKILL.md) skill first for addresses, statuses and evidence types.

1. `atlas review <branch|file.diff>` gives the brief for each touched subsystem: invariants, extension points, active decisions, conventions, Paul's patterns and mechanical flags (added code comments).
2. Read the full diff against `origin/main`. Run `atlas show <path>` for touched files and `atlas show D-…` for any decision you rely on.
3. For every hunk that rewrites or deletes existing lines, run `atlas why <path>:<from>-<to>` on the old line numbers (they are main's). If a commit message or decision gives a reason for those lines, check that the change still honours it or deliberately overturns it. Undoing a stated choice without saying so is a finding.
4. Report findings, most severe first: `file:line` · what · why (address and source URL, stated/inferred) · fix. Keep breakages of invariants or decisions apart from "Paul would likely flag". Say plainly when nothing is wrong.
5. If the branch intentionally changes a decision, recommend `atlas pending add … --supersedes D-…`.
