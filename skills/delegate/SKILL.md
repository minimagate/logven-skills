---
name: delegate
description: Use after a plan is agreed, for every implementation including small follow-up fixes. The orchestrator briefs a subagent with a self-contained brief; the subagent writes the code, and the result then goes to verify-and-commit.
---

# Delegate

Implementation is always done by subagents. The orchestrator briefs, reviews and commits.
Briefs must follow the philosophy in `../principles/SKILL.md`.

## Model choice

- Default to the cheapest capable model.
- If the same brief fails twice, retry once on the middle tier with a sharper brief.
- Never use the strongest available model for implementation. That tier is for review.
- (Claude: Haiku / Sonnet / Opus)

## Brief contents (required)

Subagents have no conversation context. Each brief must include:

- **Goal**: one sentence.
- **Decisions made**: everything already agreed in `plan`.
- **Allowed files**: exact paths to edit or create.
- **Off-limits**: files and areas not to touch.
- **Conventions**: paths to existing files to read for style and patterns.
- **Verification**: exact test and lint commands to run.
- **Dependencies**: "Do not add any dependency (gem, package, JavaScript build step). If one seems needed, stop and report instead."
- **Git**: "Do not run any git commands. Do not commit."
- **Report back**: files changed, verification commands and results, anything skipped or uncertain, concerns.

## Parallelism

- Run subagents in parallel only when their allowed-file lists are disjoint.
- Otherwise run them sequentially.
- If overlap is unavoidable, give each subagent an isolated worktree.

## After the report

- Treat the report as claims to check, not facts.
- Scope guard: compare the actual diff against the allowed-file list. Revert or reject anything outside it.
- Small fixes found during review also go through a subagent, with a minimal brief. Do not edit in the main thread.
- Hand the result to `verify-and-commit`.
