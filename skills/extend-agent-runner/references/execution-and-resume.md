# Execution and resume

## Hierarchy

`Runner::Base` executes one `AgentRun`, creating/reusing a `StepRun` per ordered agent step and a `NodeRun` per ordered node.

- Start only a pending agent run, then mark it running.
- Visit steps in the association order derived from `steps.order`.
- Reuse `find_or_create_by!` step runs and `find_or_initialize_by` node runs.
- Skip already completed work so retry/resume does not duplicate effects.
- Mark each layer running before work and completed only if it remains running after its children.
- When a child pauses or fails, copy its status/logs to the parent and stop the current pass.
- Complete the agent run only if it remains running after all steps.

Node dispatch belongs in one `case` on `node_run.kind`, with a focused runner object per kind. A node exception marks that node failed and records its message; parent propagation happens through the normal loop.

## Resume

Pause/resume is automatic domain progression, not a separate controller command.

`NodeRun#complete_with!` accepts structured output only while paused, validates the completed output, then asks its step run to resume. `StepRun#resume!` waits until no paused node runs remain, marks itself pending, and schedules the agent run. `AgentRun#resume_later!` requires `resumable?`, returns the run to pending, and enqueues it.

Preserve these guards so concurrent or repeated human completions cannot restart work incorrectly. Do not add a manual run-resume route unless it represents a new product action distinct from completing paused work.

## Data flow

Step input merges outputs from prior ordered steps. A node input starts with step input, then merges outputs from graph predecessors ordered by node order. Later merges win for duplicate keys; tests document that contract.

A step output merges only terminal-node (`output?`) run outputs. Keep graph flow based on persisted edges and ordered nodes, not incidental node-run creation order.
