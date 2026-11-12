---
name: how-we-work
description: Use at the start of repository work, including implementation, debugging, design, review and delivery. Load all applicable workflow and specialist skills before acting; coordinate work and verification.
---

# How we work

A shared framework for moving from a human goal to a verified project change. The main agent owns the result: it investigates, resolves routine choices, coordinates work and checks the evidence.

## Collaboration contract

The user sets the goal, scope and preferences. Ask when a missing decision materially changes scope or an irreversible outcome; ordinary planning is not an approval gate. Existing authorization persists. Commit, push or publish only within that authorization; [ship](../ship/SKILL.md) defines delivery boundaries.

Explain the intended result and why it matters in plain language. Default to a brief recommendation and a few plain-language steps; keep consequential assumptions, risks and tradeoffs visible. Do not paste the full internal implementation plan into the user explanation; expand technical detail only when requested or needed for a decision. Put exact commands and file ownership in briefs or supporting detail unless they help the user decide. Finish with what changed, what was checked and any material limits.

User instructions govern. Verified project facts override general defaults, not explicit user requirements. Preserve existing work and keep every edit within the request.

## Discover before acting

1. Inspect the workspace, working-tree state and repository instructions, including scoped instructions for touched files.
2. Locate this package in the skill catalog or `.agents/skills`, `.claude/skills`, `.codex/skills`, `skills/`; resolve symlinks. List names and frontmatter descriptions before reading selected bodies. Search configured skill roots if a path is stale.
3. Load only the matching `project-<repo>` skill, using repository identity rather than a worktree suffix. If absent, infer facts from source; creating a project skill is optional.
4. Build the **union** of applicable skills below from the requested outcome, affected behavior and actual files/callers, not just keywords or file extensions. Read their full `SKILL.md` bodies before the corresponding work. A catalog description or remembered summary is not a loaded skill.
5. Keep a short internal record of resolved paths read and why. Recheck before delegation, after discovering another layer, before verification/review/delivery and after context loss. Load newly relevant guidance before continuing; retain earlier applicable skills. Do not ask the user to choose skills.

| Work or affected responsibility | Add these skills |
|---|---|
| Technical implementation, debugging, refactor | [plan](../plan/SKILL.md) |
| Visual design, layout, interaction, accessibility | [rails-design](../rails-design/SKILL.md); Rails markup/interaction also [rails-frontend](../rails-frontend/SKILL.md) |
| Placement, namespaces, extraction, responsibility boundaries | [rails-structure](../rails-structure/SKILL.md) |
| Records, queries, domain rules, lifecycle, jobs/effects | [rails-models](../rails-models/SKILL.md) |
| HTTP actions, routes, params, form submission handling, responses | [rails-controllers](../rails-controllers/SKILL.md) |
| Permissions, ownership checks, roles, tenant isolation | [rails-authorization](../rails-authorization/SKILL.md) |
| Schema, indexes, foreign keys, defaults, data rollout | [rails-migrations](../rails-migrations/SKILL.md); affected record contracts also models |
| Behavior changes, regression fixes, verification choices, test changes or test review (including interface-only work) | [rails-tests](../rails-tests/SKILL.md) |
| Review or completed technical branch | [review](../review/SKILL.md), plus specialists selected from the full diff and affected callers |
| Commits, push, PR | [ship](../ship/SKILL.md), plus verification guidance for the change |

Rows accumulate: a form that changes who can update records needs frontend, controllers, authorization, models and tests; appearance changes also need design. Design and local presentation/interaction repairs proceed directly without a technical plan gate; changes to domain, persistence or access contracts use the technical mode for those pieces. Planning does not replace specialist guidance, and review/delivery do not erase earlier selections.

Read linked references only when their condition applies. For non-Rails projects, retain workflow, design and applicable verification policy; skip Rails implementation defaults and use matching stack skills from the available catalog. Search available roots when a required skill is missing; report an unresolved gap and its effect rather than pretending it was loaded.

## Work mode

| Mode | Main agent's responsibility | Delegation |
|---|---|---|
| Technical | Investigate, state a short plan, read the entire diff and verify | Bounded implementation with explicit ownership |
| Design | Make visual decisions and edit the interface directly | Bounded technical pieces after specifying their interface |
| Judgment | Own architecture, product semantics, tradeoffs and synthesis | Analysis or critique only to capable models |

When delegation is unavailable or prohibited, state the limitation briefly and work in the main thread. Do not stall or claim nonexistent delegates.

## Model choice

Choose from models the environment actually exposes before dispatch. Concrete mappings live here; other skills use capability tiers.

| Work | Required capability |
|---|---|
| Mechanical edits or bounded factual lookup | Haiku or an available lightweight model |
| Complex implementation, uncertain debugging, cross-layer work, concurrency, security, architecture or planning critique | Sonnet or an available mid-tier reasoning model, or stronger; use this tier when uncertain |
| Adversarial review | Opus or the strongest available frontier reasoning model; one whole-change pass |

Keep design decisions in the main agent. Never assign judgment to a lightweight model to save cost. Keep work yourself if no suitable delegate exists. Adversarial review runs in the main thread if it meets the flagship requirement, otherwise through exactly one reviewer; no angle-based swarm or weaker substitute. State a capability limit honestly.

After failure, sharpen the brief and raise capability where needed. Repeated failure calls for revisiting the approach rather than blind retries.

## Delegate and verify

### Brief

Start every subagent with fresh context (`fork_turns="none"`, `fork_context=false`, or the host equivalent); never fork the main conversation. Supply a self-contained brief and relevant file paths. If fresh context is unavailable, keep the work in the main thread and report the limitation.

| Brief field | Required content |
|---|---|
| Outcome | Goal, observable acceptance criteria, settled decisions and consequential assumptions |
| Responsibility | Role, exact allowed files and exclusions |
| Context | Relevant source examples, resolved applicable skill paths and an instruction to read their bodies before acting; parent-loaded skills are not inherited |
| Constraints | Scope, ownership, authorization and applicable specialist constraints; no unrelated cleanup, git writes or spawning |
| Evidence | Verification commands and expected report |

Read-only research and review briefs prohibit edits. Scoped delegates read the supplied skills and report which they used; they do not restart project-wide discovery or planning. If their slice crosses another responsibility, load that specialist too and report any scope conflict before editing outside their ownership. Claude custom agents may preload skills with `skills:`; otherwise explicitly read the resolved files in the fresh context.

### Integration

Parallelize independent work only when write ownership is disjoint; sequence dependencies. Inspect actual diffs against ownership and preserve user edits. Verify reports against source, run proportionate checks and integrate fixes. The main agent remains responsible for the complete outcome.

## Principles

### Think, simplify, scope, verify

Adapted from the [Karpathy-inspired guidelines](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md), a community distillation of his observations:

| Principle | Decision rule |
|---|---|
| Think | Inspect the real flow. Resolve routine choices; clarify consequential ambiguity before dependent work. Push back on unnecessary complexity. |
| Simplify | Implement the requested behavior without speculative flexibility. Fix representation or ownership before adding coordination. |
| Scope | Every edit serves the request. Preserve neighboring style and user work; remove leftovers your change creates, not unrelated code. |
| Verify | Define observable success before editing. Reproduce defects, fix causes and inspect affected callers. Continue until verified or a concrete blocker is explained. |

### Least necessary code

Apply the [Ponytail](https://github.com/DietrichGebert/ponytail) principle: use the fewest clear lines that preserve correctness and best practices. Check necessity, existing owners, the platform and installed dependencies before adding code. Prefer a direct expression or small method when sufficient. Remove redundant state, branches, knobs, wrappers and files; preserve readable control flow, validation, security, accessibility and useful boundaries. Simplify again before finishing.

### Contracts and ownership

Foundations implement small explicit contracts and enforce intrinsic invariants. Callers choose defaults, compose collaborators, apply product policy and start work explicitly. Dependencies point down; foundations do not recognize pages, workflows or caller identities.

Store explicit domain facts and derive technical representations. Choose representations and edit flows through the relevant domain and interface skills.

Share actual contracts; separate interactions that change for different reasons. Distinguish real types from independent options. Deterministic derivation is useful; caller-intent guessing is not. Keep genuine choices and invariants while removing redundant forwarding and configuration.

A meaningful boundary can have one caller; small duplication or a concrete feature view can beat a generalized abstraction. Avoid hidden workflow initialization, caller-specific validation bypasses and speculative registries. Read [foundations](references/foundations.md) when representation or composition is disputed.

Keep cross-cutting mechanics locally composable rather than propagating feature or transport flags through unrelated callers. Preserve framework defaults and intentional APIs; missing textual callers alone do not prove code dead. Read [review patterns](references/review-patterns.md) when evaluating these boundaries.

### Change boundaries

Prefer existing code, frameworks and standard libraries. New dependencies require user approval. Each rule, effect and failure has one owner. Log actionable failures once at that boundary; remove debug output.

Protect costly-to-reverse data shapes, permissions and public contracts with cheap deliberate choices. Defer hypothetical machinery with a concrete trigger.

## Project context

Keep project facts separate from shared guidance. For a new project skill, copy the [project template](references/project-skill-template.md) and record verified facts only.
