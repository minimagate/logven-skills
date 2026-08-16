---
name: extend-agent-runner
description: Change Logven agent execution. Use for `AgentRun`, `StepRun`, `NodeRun`, `Runner::*`, run lifecycle states, deterministic ordering, input/output merging, node-kind dispatch, MiniRacer or LLM execution, pause/resume, failure logs, artifacts, or execution tests.
---

# Extend Agent Runner

Preserve resumable, state-guarded execution across the run, step-run, and node-run hierarchy.

## Workflow

1. Trace the affected record hierarchy, runner class, node STI contract, graph order, background job, policy/controller entrypoint, and tests.
2. Decide whether behavior belongs to orchestration, a specific node runner, input/output aggregation, or lifecycle state.
3. Preserve completed-work reuse and state guards before adding new transitions.
4. Validate output at the `NodeRun` completion boundary so automated and human completion share the contract.
5. Use `add-background-work` for enqueueing changes, `add-agent-tool` for tool execution boundaries, and `use-turbo` for run progress delivery.
6. Always use `generate-tests` for state, dataflow, failure, and resumption behavior.

Read [`references/execution-and-resume.md`](references/execution-and-resume.md) before changing orchestration, dataflow, or pause/resume. Read [`references/node-runners.md`](references/node-runners.md) before changing a node runner, error mapping, output validation, or artifacts.

## Core Rules

- Execute steps and nodes deterministically from persisted order.
- Reuse completed step/node runs; retries must not repeat completed side effects.
- Propagate paused/failed child state and logs upward, then stop the pass.
- Keep each node kind in a focused runner and keep dispatch centralized.
- Resume only after all paused work at the current level has been completed.

## Do Not

- Do not restart a non-pending run through `start_now!`.
- Do not infer dataflow from record creation order or all preceding nodes; use step order and graph edges.
- Do not rescue a node error without persisting failed state and useful logs.
- Do not add UI-specific behavior to runner objects.
