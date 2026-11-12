---
name: review
description: Single flagship adversarial review of a branch, PR or diff. Challenge behavior, assumptions and integration beyond repository guidelines; no swarm of angle-specific reviewers.
---

# Adversarial review

**One flagship reviewer, full scope.** Follow [flagship model choice](../how-we-work/SKILL.md#model-choice). Review directly when the main agent meets that requirement; otherwise invoke exactly one suitably capable reviewer, preferably with fresh context. Never split by lens, dispatch mini-reviewers or inherit the implementation model's tier. Do not claim a weaker pass satisfies this review if the required capability is unavailable.

1. Establish the request, intended behavior and exact diff/base. Read the complete diff plus affected callers, consumers, data model, tests and relevant runtime/dependency contracts. Use [discovery](../how-we-work/SKILL.md#discover-before-acting) for applicable local instructions.
2. Form an independent account of what the code actually does. Challenge the implementation and plan's assumptions, not just compliance. Repository guidelines are context, not the limit of review: a real bug needs no written rule to be a finding.
3. Trace plausible counterexamples end to end: permissions and tenant isolation, hostile inputs, state transitions, retries/races, partial failure, data migration/compatibility, realistic load, performance and operational recovery. Inspect unchanged code when needed to prove integration defects. Use [adversarial prompts](references/adversarial.md) as questions, not separate agent assignments.
4. Check whether better representation/ownership or existing framework behavior removes glue. Prefer the fewest clear lines that preserve the contract; never reward code golf or remove necessary safety. Enforce the explicit no UI/DOM test policy, including assertions hidden in request tests.
5. Try to disprove every candidate: inspect guards, actual callers, framework guarantees and existing coverage. Run proportionate safe reproductions/checks where useful. Report substantiated defects and consequential design risks, not speculative concerns or personal taste.

Return findings first, ranked by impact: `path:line`, concrete trigger and consequence, evidence and smallest remedy. Distinguish demonstrated defects, consequential tradeoffs and unverified questions; do not invent findings to fill a quota. Mention related pre-existing defects separately from introduced regressions. State scope, checks and material gaps; say plainly when no findings survive.

Review is read-only: no edits, commits, publishing or subreviewers. Standalone review ends with findings unless fixes were requested. During authorized implementation, route fixes through its work mode and have the same flagship reviewer recheck affected paths.
