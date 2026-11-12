---
name: plan
description: Plan technical implementation, debugging, or refactoring before delegation. Resolve ordinary choices and proceed; design work belongs to the main agent without a plan-approval gate.
---

# Plan technical work

Follow [work modes and discovery](../how-we-work/SKILL.md). Design requests go directly to [rails-design](../rails-design/SKILL.md).

Present the user-facing plan in simple words: the intended result, what changes, why, and how you will check it. Use short steps; explain necessary technical terms and include implementation detail only when it helps the user make a decision. Keep exact file ownership and commands in the delegation brief or supporting detail.

1. Read the relevant owners, callers, tests and repository instructions. Establish the requested behavior and current failure.
2. State a short plan: observable outcome, consequential assumptions, important decisions, ordered slices with file ownership, a check per slice and superseded code to remove. Choose the least code that fulfills those criteria; do not plan speculative options or adjacent cleanup. Resolve routine choices yourself. Do not require plan approval unless requested or a material user decision is missing.
3. Separate primitive contracts from product choices: who validates, who chooses defaults, who composes, who initiates side effects? Give each one an explicit owner. Before adding glue, check whether the stored representation, ownership or edit flow is wrong: derive technical schemas from domain facts and use native framework contracts. Distinguish shared lifecycle from genuinely different interactions. Name the entity each list represents and the explicit ownership context; include structural edits and error recovery in applicable acceptance criteria.
4. Choose delegate capability before dispatch using [model choice](../how-we-work/SKILL.md#model-choice). Complex work and judgment start at mid-tier or stronger. Give independent slices disjoint files; sequence dependent slices.
5. Implement through the delegation loop, then verify the full result. Re-plan only when new evidence changes the approach or scope.

For costly schema/contracts, security, concurrency or a new subsystem, use bounded read-only exploration and critique when useful. Load [critics](references/critics.md) for their lenses; do not run a fixed agent swarm or ask permission merely to plan. Keep the main agent's synthesis decisive.

Test plans cover nonvisual behavior only: no UI/DOM tests. UI changes use browser inspection. Dependencies need approval; follow [ship](../ship/SKILL.md) for authorized commits and PRs.
