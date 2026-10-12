---
name: principles
description: Use when planning, implementing, delegating or reviewing any change, to apply the shared engineering philosophy: minimalism, no unnecessary dependencies, the smallest coherent change and cheap-option future-proofing. Cite this skill rather than restating it.
---

# Principles

Shared engineering philosophy for Logven. Cite this file rather than restating it.
Every other skill that touches design, scope or dependencies defers to these rules.

## Minimalism

- Prefer the platform, Rails, the standard library and what the repo already has.
- Build the simplest thing that meets the current requirement.
- Prefer direct, readable code over indirection, DSLs, registries, generic wrappers and one-method objects.
- Give each rule, query, presentation decision, side effect and failure one owner.
- Prefer deletion over addition. Remove superseded code, aliases and compatibility paths in the same change.

## Dependencies

- The default is no new dependency. Any new dependency is an explicit user decision, listed under Open decisions with: what it replaces, why a small amount of own code is not enough, and its maintenance and security cost.
- No npm and no JavaScript build step. If a browser dependency is truly unavoidable, use importmap pins or a vendored file.
- Prefer a small own implementation over a package for narrow needs.
- Treat lockfile changes (`Gemfile.lock`, importmap pins) as a signal to check.
- A subagent never adds a dependency on its own. It stops and reports, and the orchestrator brings the question to the user.

## Future-proofing

- Use cheap options, not machinery.
- Spend effort only to avoid a costly reversal: one-way doors such as schema and data shape, identifiers, public URLs and API contracts, events, the permission model, and names that leak into data.
- Also cover a plausible costly edge case, but only when the cost now is small.
- Everything else is deferred with a named trigger. See `../plan-feature/references/triage-rubric.md`.
- Before adding a provision, ask whether the door is really one-way. If not, keep it simple.

## Logging and tests

- Log an actionable failure once, at the boundary that owns it.
- Do not log the same failure again at every layer above it.
- Leave no debug output behind.
- Test meaningful behavior at its narrowest public boundary.
- Never test framework behavior or the same contract twice. See `../rails-tests/SKILL.md`.

## Conflicts

- When minimalism and future-proofing disagree, show both sides to the user with a recommendation.
- Do not resolve the conflict silently in either direction.
