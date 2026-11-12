# Planning critique

Use only the lenses relevant to a consequential technical decision. This is optional planning analysis, not code review; code review uses one flagship under [review](../../review/SKILL.md). Critics are read-only and use mid-tier reasoning or stronger; each receives the requirement, plan, concrete source paths and applicable skills.

| Lens | Question |
|---|---|
| Simplicity | What exceeds the requirement? Can an existing owner or direct method replace it? |
| Reversibility | Which data shapes, identifiers, permissions or external contracts are expensive to change? What cheap provision is justified now? |
| Failure | What reachable input, race, retry, partial failure or tenant boundary breaks the plan? |
| Fit | Does placement, reuse, sequencing and verification match the repository? Do foundations own invariants while explicit callers own policy and defaults? |

Return only substantiated observations: lens, affected slice, claim, source `path:line`, concrete scenario, smallest remedy, cost now/later and likelihood. Check existing guards and callers to falsify each claim. Do not prescribe UI/DOM tests.

The main agent triages: adopt verified defects and scope cuts; add a cheap provision only when cost now is low and reversal costly; defer plausible nonessential work with a trigger; reject speculative machinery. Resolve routine tradeoffs; ask the user only for material product choices or irreversible scope decisions.
