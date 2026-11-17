---
name: review
description: Single adversarial review of a branch, PR or diff by one fresh-context reviewer subagent. Challenge behavior, assumptions and integration beyond repository guidelines; no swarm of angle-specific reviewers.
---

# Adversarial review

Find substantiated defects and consequential design risks in the complete change, including its integration. Repository guidelines inform the review; they do not limit what counts as a bug.

## Review contract

Use **one reviewer for the full scope**: a mid-tier subagent with fresh context, following [model choice](../how-we-work/SKILL.md#model-choice). The main agent that built or integrated the change never reviews it itself; it briefs the reviewer and records the findings. Never split by lens or dispatch mini-reviewers. State any capability limit; a lightweight-model pass does not satisfy this review.

Source review is read-only: no source edits, commits, publishing or subreviewers. Standalone review ends with findings unless fixes were requested.

Follow [tsk](../tsk/SKILL.md) for tracking and deferred findings. A read-only delegate returns findings with originating task IDs for the parent to record; board writes require an explicit allowance in its brief. The main agent records actionable out-of-scope issues as linked follow-ups without adding them to this PR.

## Establish actual behavior

Establish the request, intended behavior and exact diff/base. Read the complete diff, affected callers, consumers, data model, tests and relevant runtime/dependency contracts. Use [discovery](../how-we-work/SKILL.md#discover-before-acting) for applicable instructions.

Form an independent account of what the code does. Challenge the implementation and plan's assumptions rather than merely checking compliance.

## Challenge and falsify

Trace plausible counterexamples through permissions, tenant isolation, hostile inputs, state transitions, retries/races, partial failure, migration/compatibility, realistic load and recovery. Inspect unchanged code when needed to prove integration defects. Use [adversarial prompts](references/adversarial.md) as questions, not separate assignments.

Check whether better representation, ownership or existing framework behavior removes glue. Prefer the fewest clear lines preserving the contract; retain necessary safety. Assess verification against [rails-tests](../rails-tests/SKILL.md), including assertions hidden in other test layers.

Try to disprove each candidate using guards, callers, framework guarantees and coverage. Run proportionate safe reproductions when useful. Discard speculative concerns and personal taste.

## Deliver findings

Return findings first, ranked by impact. Each needs a `path:line`, concrete trigger and consequence, evidence and smallest remedy. Distinguish demonstrated defects, consequential tradeoffs and unverified questions; report related pre-existing defects separately from introduced regressions.

State scope, checks and material gaps. Say plainly when no findings survive; there is no quota. During authorized implementation, route fixes through its work mode and have the same reviewer recheck affected paths.
