---
name: plan
description: Plan technical implementation, debugging, or refactoring before delegation. Resolve ordinary choices and proceed; design work belongs to the main agent without a plan-approval gate.
---

# Plan technical work

Turn the request into a small, verifiable implementation contract. Follow [work modes and discovery](../how-we-work/SKILL.md); design requests go directly to [rails-design](../rails-design/SKILL.md).

## Establish the outcome

Read relevant owners, callers, tests and repository instructions. Establish the requested behavior and current failure. Define observable success, consequential assumptions and the decisions that affect scope. Resolve routine choices yourself; ask only for a missing material decision or requested approval.

Present a brief recommendation and a few simple steps: what changes, why and how it will be checked. Keep material decisions and risks visible. Put detailed schema, routes, file ownership and check commands in the internal work plan or delegate brief; do not turn a user-facing proposal into a full implementation specification unless asked.

## Define ownership

Separate intrinsic invariants from product choices: who validates, chooses defaults, composes and starts effects? Give each responsibility one explicit owner. Before adding glue, check whether the representation, ownership or edit flow is wrong. Derive technical schemas from domain facts and prefer native framework contracts.

Distinguish a shared lifecycle from different interactions. Name the entity each list represents and its ownership context. Include structural edits and error recovery in acceptance criteria where relevant.

## Sequence the work

Choose the least code that satisfies the contract. Define ordered slices with file ownership, a check per slice and superseded paths to remove. Exclude speculative options and adjacent cleanup.

Choose capability before dispatch using [model choice](../how-we-work/SKILL.md#model-choice). Complex work and judgment start at mid-tier or stronger. Independent slices get disjoint files; dependent slices run in sequence.

For costly schema/contracts, security, concurrency or a new subsystem, use bounded read-only exploration and critique when useful. Read [critics](references/critics.md) for relevant questions; do not run a fixed swarm. The main agent owns synthesis.

## Complete the plan

Proceed through the [delegation and verification loop](../how-we-work/SKILL.md#delegate-and-verify). A plan is ready when its outcome, owners, slices and checks are clear; it is complete when the full result is verified. Re-plan when evidence changes the approach or scope.

Checks cover nonvisual behavior; inspect UI in the browser. No UI/DOM tests. Dependencies require approval; [ship](../ship/SKILL.md) governs authorized commits and PRs.
