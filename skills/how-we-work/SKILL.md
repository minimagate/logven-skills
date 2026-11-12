---
name: how-we-work
description: Start every repository task here. Discover applicable skills, plan and delegate technical work, keep design in the main agent, choose model tiers, and verify results.
---

# How we work

Scoped delegates follow their brief and read only the linked principles and assigned layer skills; they do not restart discovery/planning, spawn agents or perform git writes. The workflow below is for the main agent.

## Discover before acting

1. Inspect the workspace, working-tree state and repository instructions, including scoped instructions for touched files. Preserve user changes.
2. Locate this package in the available skill catalog or `.agents/skills`, `.claude/skills`, `.codex/skills`, `skills/`; resolve symlinks. List skill names and frontmatter descriptions, not every full body. If a path is stale, search the configured skill roots before declaring it missing.
3. Load the matching `project-<repo>` skill if present (use repository identity, not a worktree suffix). Never load another project's skill. If absent, infer facts from the repository; creation is optional.
4. Use the routing table; read the selected skills before work and pass their resolved paths to delegates. Re-evaluate when scope changes. No need for the user to name a skill.

| Task or touched layer | Read |
|---|---|
| Technical implementation, bug, refactor | [plan](../plan/SKILL.md), then relevant layers below |
| Visual design, layout, interaction | [rails-design](../rails-design/SKILL.md); Rails markup also [rails-frontend](../rails-frontend/SKILL.md) |
| Placement, namespaces, abstractions | [rails-structure](../rails-structure/SKILL.md) |
| Records, domain logic, jobs | [rails-models](../rails-models/SKILL.md) |
| HTTP actions, routes, params | [rails-controllers](../rails-controllers/SKILL.md) |
| Permissions, tenant isolation | [rails-authorization](../rails-authorization/SKILL.md) |
| Schema, indexes, foreign keys | [rails-migrations](../rails-migrations/SKILL.md) |
| Tests, coverage, regressions | [rails-tests](../rails-tests/SKILL.md) |
| Review or completed technical branch | [review](../review/SKILL.md) |
| Commits, push, PR | [ship](../ship/SKILL.md) |

Read references only when their linked condition applies. Non-Rails projects skip Rails implementation defaults; design principles still apply. User instructions govern; project facts override general defaults, not explicit user requirements.

## Work mode

- **Technical:** main agent investigates, states a short plan, delegates implementation, reads the entire diff and verifies. Proceed within the request; plan approval is not a routine gate. Ask only for missing decisions that materially affect scope or irreversible outcomes.
- **Design:** main agent owns visual judgment and edits the design itself, without plan approval. For mixed work, retain design and delegate bounded technical pieces after specifying their interface.
- **Judgment:** main agent owns architecture, product semantics, tradeoffs and synthesis. Delegate analysis or critique only to capable models.
- If delegation is unavailable or prohibited, say so briefly and do the work in the main agent. Do not stall or claim nonexistent delegates.

## Explain work simply

Present plans, questions, tradeoffs, progress and results in plain language. Lead with what will change and why it matters, then explain the steps and how success will be checked. Prefer familiar words and concrete examples; avoid jargon, unexplained acronyms and unnecessary implementation detail. Explain any technical term needed for a decision. Keep precise paths, commands and architecture detail in delegate briefs or supporting detail when useful; do not make the user decode them to understand the plan.

## Model choice

Choose before dispatch, using the models the environment actually exposes:

- Mechanical, fully specified edits or bounded factual lookup: **Haiku (or an available lightweight model)**.
- Complex implementation, uncertain debugging, cross-layer changes, concurrency, security, architecture, planning critique or other judgment: **Sonnet (or an available mid-tier reasoning model) or stronger**. If uncertain, choose this tier immediately.
- **Adversarial review is a separate flagship task:** **Opus (or the strongest available frontier reasoning model)** handles the whole review, in the main thread if already on that model or through exactly one reviewer. No angle-based swarm; no Sonnet, Haiku, Fable-level or lightweight substitute. If flagship execution is unavailable, state the limitation rather than presenting a downgraded check as the requested review.
- The main agent keeps design decisions. Never route judgment to a lightweight model to save cost. If no suitable subagent exists, keep the task yourself.
- After failure, sharpen the brief and raise capability where needed. Repeated failures require revisiting the approach, not blind retries.

## Delegate and verify

Give each delegate: goal and observable acceptance criteria; settled decisions and consequential assumptions; role; exact allowed files and exclusions; relevant source examples; resolved skill paths; verification commands; expected report. Include: the shortest clear implementation that preserves the contract; no unrelated cleanup, dependency additions, commits/pushes or spawning; and **no UI/DOM tests** (see testing rule below). Read-only research/review briefs prohibit edits.

Parallelize only independent work with disjoint write ownership. Check actual diffs against ownership; do not discard user edits. Verify reports against source, run proportionate checks, and integrate fixes. Report changes, checks and material limits. Commit or publish only within existing authorization; see `ship`.

## Principles

### Think, simplify, scope, verify

Adapted from the [Karpathy-inspired guidelines](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md), a community distillation of his observations:

- **Think:** inspect the real flow; state consequential assumptions and tradeoffs. Resolve routine choices yourself; clarify material ambiguity before dependent work. Push back on unnecessary complexity.
- **Simplify:** implement the requested behavior without speculative flexibility. Fix the representation or owner before adding coordination code.
- **Stay surgical:** every edit serves the request. Preserve neighboring style and user work; remove leftovers your change creates, not unrelated pre-existing code.
- **Verify an outcome:** define observable acceptance criteria and checks before editing; reproduce defects, fix their cause and inspect affected callers. Continue until verified or a concrete blocker is explained. UI verification remains manual; do not generate forbidden tests.

### Least necessary code

Apply the [Ponytail](https://github.com/DietrichGebert/ponytail) principle: **write as few clear lines as possible while preserving correctness and best practices**. After reading the flow, check necessity, existing owners, standard library/platform/framework and installed dependencies before writing new code. Prefer a direct expression or small method when sufficient. Remove redundant state, branches, knobs, wrappers and files; do not compress formatting, hide control flow, weaken validation/security/accessibility or erase useful boundaries to lower a line count. Before finishing, simplify any solution that can meet the same contract with materially less code.

### Contracts and ownership

- Prefer existing code, framework and standard library. No new dependency without user approval; no npm/build pipeline added to Rails defaults. Remove superseded paths in scope.
- **Dumb foundations, opinionated composition:** a primitive implements a small explicit contract and enforces its own invariants. A caller chooses defaults, assembles collaborators, applies product policy and starts work explicitly. Dependencies point down; foundations do not recognize pages, workflows or caller identities.
- **Fix representation before adding glue:** store explicit domain facts and derive technical representations; use columns/child records for known structure and behavior, JSON for dynamic/opaque payloads. Prefer native assignment, validation and forms over parallel draft/synchronization protocols.
- Share actual contracts; separate interactions that change for different reasons. Distinguish a real type from an independent option. Remove redundant knobs and forwarding layers; deterministic derivation is useful, caller-intent guessing is not. Keep genuine user choices and invariants.
- Avoid hidden workflow initialization, caller-specific validation bypasses and speculative registries. A meaningful boundary can have one caller; small duplication or one concrete feature view can beat a generalized abstraction. Evidence and before/after examples: [Paul's sheets rewrites](references/foundations.md).
- Keep cross-cutting mechanics locally composable, not spread as feature/transport flags through unrelated callers. Preserve framework defaults and intentional APIs; missing textual callers alone do not prove code dead. More evidence: [recurring review corrections](references/review-patterns.md).
- Each rule, effect and failure has one owner. Log actionable failures once at their owning boundary; remove debug output.
- Protect costly-to-reverse data shapes, permissions and public contracts with cheap deliberate choices; defer hypothetical machinery with a concrete trigger.
- **No automated UI or DOM tests:** no rendered HTML/text/selector/class/template/component assertions, snapshots, system/browser tests, or equivalent tests hidden in request/helper tests. Test domain, policy and nonvisual HTTP contracts; inspect UI manually in the browser. Carry this rule into briefs and review acceptance criteria. Existing UI tests are not precedent; do not expand them. Full policy: [rails-tests](../rails-tests/SKILL.md).
- No tool/model attribution in commits or PRs. No automatic commits, pushes or unrelated cleanup.

For a new project skill, copy the [project template](references/project-skill-template.md); record verified project facts only.
