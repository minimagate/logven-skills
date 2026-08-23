---
name: agent-runtime
description: Change Logven agent building, step graphs, node execution, run state machines, jobs, manual input pauses, artifacts, or shape contracts. Use for Builder/Runner/Graphs/Shapes and Agent, Step, AgentRun, StepRun, or NodeRun lifecycle work.
---

# Agent Runtime

Preserve the distinction between definitions and executions:

- `Agent -> Step -> Nodes::Base/Edge` defines an ordered, typed workflow.
- `AgentRun -> StepRun -> NodeRun` records one user's execution, status, logs, and node output.
- `Artifact` records named run-level deliverables.

Read the entire affected transition path before changing it: model command, builder or runner object, job, policy, controller, Turbo broadcast consumer, and tests.

## Preserve the build pipeline

Agents and steps begin as drafts. `Builder::Base` advances a claimed building step through details, graph construction/judgment, body generation, validation, and promotion. Graph generation may retry against syntactic and semantic feedback; it must either produce a valid ready step or restore a useful draft/error state.

- Keep jobs thin: enqueue records, then call `build_now!` or `start_now!`.
- Claim work under the existing agent/step locks before external LLM work begins.
- Never allow a ready agent's immutable definition to be edited in place; revision creates a draft copy of the agent, steps, nodes, and remapped edges.
- When copying definitions, use the explicit `revision_attributes` contracts and rebuild edge references through a node map.
- Promotion validates the whole graph and reports stable, contextual errors before committing status changes.

## Preserve execution semantics

`AgentRun#claim_for_start!` is the atomic gate that prevents duplicate jobs from executing the same pending run. Do not replace it with a check followed by a separate write.

Runner behavior is ordered and resumable:

1. Iterate agent steps in their explicit order.
2. Find or create one `StepRun` per agent run and step.
3. Iterate nodes in topological order and find or initialize one `NodeRun` per step run and node.
4. Skip completed work so retries and resumes do not repeat it.
5. Propagate paused or failed status and logs upward; complete parents only while still running.

Input nodes pause. `NodeRun#complete_with!` casts and validates human input against the node output shape, completes the node, and resumes only when no paused child remains. Preserve this handshake across policy scope, form parameters, runner state, and broadcasts.

## Keep node contracts exact

- `params` nodes have no inputs and infer output from a JSON object body.
- `input` nodes have no inputs or executable body and require a non-empty output shape.
- `tool` nodes derive input/output shapes from the registered tool.
- `llm` and `script` nodes require their declared input shape to be covered by upstream outputs and require a valid non-empty output shape.
- Edges stay within one step; ready graphs remain connected and acyclic.

Changes to a node kind must update its STI class, kind/type maps, builder prompts, runner dispatch, shape validation, serialization, UI labels/tones if affected, and focused tests.

## Handle failures at the right boundary

Let a node runner translate subsystem-specific failures into a useful exception. `Runner::Base` records the failure on the `NodeRun`; builder recovery records the error and restores draft state. Do not silently mark failed work complete or rescue errors so broadly that status/log updates are skipped.

## Keep runtime code lean

- Extend the nearest existing model command, builder, runner, or node implementation. Do not add a second orchestration layer, generic event bus, or abstraction for hypothetical workflow kinds.
- Keep execution flow linear and ownership explicit: jobs enqueue and delegate, runners coordinate, node runners execute, and models protect transitions. Do not duplicate status propagation or lifecycle branching across those layers.
- Add only the tests needed for the changed transition or invariant. Do not multiply every status, node kind, and retry combination when one boundary test plus focused lower-level coverage proves the behavior.
- Record only operator-actionable lifecycle facts, once, at the boundary that owns the state change. Do not add per-node-loop chatter, duplicate parent/child messages, debug traces, prompts, secrets, or full input/output payloads.

## Verify

Test successful execution, invalid outputs, pause/resume, duplicate job claims, completed-work skipping, step/node uniqueness, failure propagation, build recovery, revision copying, and graph/shape invariants as applicable. Use queued `with_llm` responses instead of live LLM calls.
