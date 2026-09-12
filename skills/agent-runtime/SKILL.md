---
name: agent-runtime
description: Change Logven worker compilation, node execution, run state machines, jobs, manual input pauses, artifacts, or shape contracts. Use for UltraBuilder/Runner/Graphs/Shapes and Worker, Step, WorkerRun, StepRun, or NodeRun lifecycle work.
---

# Agent Runtime

Preserve the distinction between definitions and executions:

- `Worker -> Step -> Nodes::Base/Edge` defines an ordered, typed workflow.
- `WorkerRun -> StepRun -> NodeRun` records one user's execution, status, logs, and node output.
- `Artifact` records named run-level deliverables.

Read the entire affected transition path before changing it: model command, builder or runner object, job, policy, controller, Turbo broadcast consumer, and tests.

## Compile the whole worker incrementally

`UltraBuilder::Compiler` authors a complete worker node by node. Steps are ordered execution groups assigned during compilation; never restore independently authored step prompts, step build jobs, graph judges, or body-generation phases.

- Keep the original worker request authoritative. `UltraBuilder::Context` snapshots exact tools, project sheet schemas and data actions, creates an acceptance brief, and supplies typed available outputs plus remaining requirements to each construction call. Preserve global constraints and fixed values in later nodes.
- Explicitly use `poolside/laguna-xs-2.1` for building. Runtime LLM nodes use `LLM_MODEL` independently.
- `WorkerBuildJob` is the single build job. Claim under the worker lock, call the provider outside transactions, and check the durable token when publishing. Worker statuses are draft, pending, building, ready, and failed. Expired claims can resume.
- Save each accepted complete node, its edges and the worker `build_context` checkpoint in one transaction. Retry only the rejected candidate with a small explicit budget. Never delete accepted nodes for local repair or repeat completed construction after resuming.
- Candidate acceptance owns exact node, tool, data and handoff validation; `Step#finalize!` owns connected acyclic graph validation and ordering. Steps and nodes are draft or ready, without intermediate build phases.
- Ready worker requests are immutable. Revisions copy valid graph definitions, remap edges, retain data bindings and copy compilation context without claims. If copied definitions no longer validate against current project data, only the new revision starts with an empty graph and fresh context. Changing a draft request resets that draft's graph and context for a new compilation.
- Use `bin/rails runner evals/ultra_builder.rb` for live fidelity and latency evaluation. Mocked tests establish application behavior, not model quality. Keep live evaluation external effects isolated.

## Preserve execution semantics

`WorkerRun#start_now!` checks pending state and queued execution uses Solid Queue concurrency controls. Preserve those guards and completed-work skipping; do not assume queue controls serialize direct model calls or `perform_now`.

Runner behavior is ordered and resumable:

1. Iterate worker steps in their explicit order.
2. Find or create one `StepRun` per worker run and step.
3. Iterate nodes in topological order and find or initialize one `NodeRun` per step run and node.
4. Skip completed work so retries and resumes do not repeat it.
5. Propagate paused or failed status and logs upward; complete parents only while still running.

Input nodes pause. `NodeRun#complete_with!` casts and validates human input against the node output shape, completes the node, and resumes only when no paused child remains. Preserve this handshake across policy scope, form parameters, runner state, and broadcasts.

## Keep node contracts exact

- `params` nodes have no inputs and infer output from a JSON object body.
- `input` nodes have no inputs or executable body and require a non-empty output shape.
- `tool` nodes derive input/output shapes from the registered tool and any server-normalized resource configuration; configuration is copied through revisions and revalidated at execution.
- `llm` and `script` nodes require their declared input shape to be covered by upstream outputs and require a valid non-empty output shape.
- Edges stay within one step; ready graphs remain connected and acyclic.

Changes to a node kind must update its STI class, kind/type maps, builder prompts, runner dispatch, shape validation, serialization, UI labels/tones if affected, and focused tests.

## Handle failures at the right boundary

Let a node runner translate subsystem-specific failures into a useful exception. `Runner::Base` records the failure on the `NodeRun`; compiler recovery records the error, marks the worker failed and preserves accepted work. Do not silently mark failed work complete or rescue errors so broadly that status/log updates are skipped.

## Keep runtime code lean

- Extend the nearest existing model command, builder, runner, or node implementation. Do not add a second orchestration layer, generic event bus, or abstraction for hypothetical workflow kinds.
- Keep execution flow linear and ownership explicit: jobs enqueue and delegate, runners coordinate, node runners execute, and models protect transitions. Do not duplicate status propagation or lifecycle branching across those layers.
- Add only the tests needed for the changed transition or invariant. Do not multiply every status, node kind, and retry combination when one boundary test plus focused lower-level coverage proves the behavior.
- Record only operator-actionable lifecycle facts, once, at the boundary that owns the state change. Do not add per-node-loop chatter, duplicate parent/child messages, debug traces, prompts, secrets, or full input/output payloads.

## Verify

Test successful execution, invalid outputs, pause/resume, duplicate job claims, completed-work skipping, step/node uniqueness, failure propagation, build recovery, revision copying, and graph/shape invariants as applicable. Use queued `with_llm` responses instead of live LLM calls.
