---
name: extend-agent-builder
description: Change Logven's agent-step build pipeline. Use for `Builder::*`, build lifecycle states, LLM builder prompts, graph generation or repair, judge behavior, node/edge ingestion, topological ordering, shape validation/inference, build logs, or strict queued LLM tests.
---

# Extend Agent Builder

Preserve the staged, validation-driven builder: the LLM proposes data, domain objects validate it, and precise errors drive bounded repair.

## Workflow

1. Read `Step`, `Builder::Base`, every affected stage, the relevant prompt, node STI variants, graph/shape objects, and their tests.
2. Identify whether the change belongs to details, graph/judge, bodies, a deterministic graph/shape contract, or the outer lifecycle.
3. Keep stage inputs/outputs and status promotion explicit. Change the narrowest stage or validator.
4. When changing generated JSON, update prompt, ingestion whitelist/mapping, validation, and tests as one contract.
5. Preserve computed Params and Tool shapes rather than accepting generated overrides.
6. Use `change-domain-model` for record invariants, `add-background-work` for scheduling, and `generate-tests` for coverage.

Read [`references/pipeline.md`](references/pipeline.md) before changing orchestration, stages, repair, or errors. Read [`references/graphs-shapes-and-prompts.md`](references/graphs-shapes-and-prompts.md) before changing nodes, edges, shapes, algorithms, prompts, or LLM test responses.

## Core Rules

- Run deterministic syntactic/domain validation before semantic judging.
- Replace a proposed graph transactionally and order it from graph dependencies.
- Keep error messages stable and actionable because they are both user logs and LLM repair input.
- Bound all LLM repair attempts and re-raise the final failure after recording it.
- Keep prompts smaller than the application contract; enforce correctness in Ruby.

## Do Not

- Do not trust LLM-provided node types, attributes, shapes, or edges outside the explicit mapping.
- Do not move graph or shape validation into prompt text.
- Do not make a partial build appear ready.
- Do not weaken `with_llm` when a changed call sequence exposes an unintended extra or missing request.
