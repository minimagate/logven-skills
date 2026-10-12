---
name: plan
description: Use before writing or changing any code or design, whenever a request asks to build, fix, change or design something. Analyze and agree the plan with the user before handing off to delegate.
---

# Plan

Agree the scope and approach with the user before any code is written.

## Phase rules

- The main thread only analyzes and plans. Write no code and make no edits in this phase.
- Read the relevant code first: routes, models, callers, nearest tests, and repo guidelines (AGENTS.md, CLAUDE.md, CONTRIBUTING).
- Do not start implementation, scaffolding or "quick prototypes" to explore.

## Output (exactly three parts)

1. **Understanding**: current state and the goal, in a few sentences.
2. **Open decisions**: each with 2-3 options and your recommendation. Keep it short.
3. **Proposed changes**: an ordered list of scoped changes. Each becomes one commit and lists the files it touches.

## Guidelines

- Give a recommendation, not an exhaustive survey of options.
- Do not re-litigate decisions the user already made. Build on them.
- Ask only questions that are genuinely the user's to make. Resolve the rest from the code or sensible defaults and state the default you chose.
- Split work into independent scoped changes with disjoint files, so briefs can run in parallel later.
- Keep each change small enough to review as one commit.

## Escalate big features

- If the request introduces a new domain concept, changes the schema, adds an external integration or public contract, or spans several areas, say so.
- Offer `plan-feature` for multi-agent planning.
- Start it only after the user confirms, because it costs considerably more.

## Gate

- Wait for explicit agreement before moving to `delegate`.
- Approval covers only the plan as written. If scope, files or decisions change, re-plan and get agreement again.
- Do not treat silence or a partial "ok" as approval of new items.
