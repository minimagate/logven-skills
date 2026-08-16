---
name: add-background-work
description: Add or change asynchronous Logven work implemented through Active Job. Use when introducing a job, moving an agent build or run off the request path, adding `*_now!`/`*_later!` entrypoints, changing enqueue-time status, or testing job delegation and resumability.
---

# Add Background Work

Keep the job as a delivery mechanism. Put the workflow and its state guards on the record that owns the operation.

## Workflow

1. Read the owning model, its policy/controller caller, the matching jobs, and their tests.
2. Define or preserve a synchronous bang entrypoint such as `build_now!` or `start_now!`. Guard it by the state from which work may start so retries and stale jobs become no-ops.
3. Define the asynchronous counterpart such as `build_later!` or `start_later!`. Guard it too, persist the visible queued state, then call `perform_later(self)`.
4. Make `perform` delegate directly to the synchronous entrypoint. Do not duplicate orchestration or status transitions in the job class.
5. Let the domain layer that owns a stage record its errors and cleanup. For example, `Builder::Base` resets the step and stores build logs, while `Step#build_now!` ensures the parent agent leaves its transient building state.
6. Use the `generate-tests` skill. Cover enqueueing and persisted state at the caller/model boundary, and cover that `perform_now` reaches the synchronous behavior. Do not assert Solid Queue internals.

## Repository Pattern

- `Agent#build_later!` sets the agent pending before enqueuing `AgentBuildJob`; the job calls `build_now!`.
- `Step#build_later!` sets both agent and step pending before enqueuing `StepBuildJob`; the job calls `build_now!`.
- `AgentRun#start_later!` enqueues `AgentRunJob`; the runner's pending guard owns start idempotency.
- Resume is domain-driven: completing paused node work calls `StepRun#resume!`, which advances state and schedules the owning run. Do not add a second manual resume route unless the product requires a distinct user-owned resource.

## Rules

- Persist state before enqueueing when the UI or policy depends on that state.
- Pass records through Active Job serialization; do not pass a graph of redundant scalar attributes.
- Keep external calls and long computation below the synchronous model entrypoint, not in controllers.
- Use after-commit Turbo broadcasts already owned by records for progress updates; do not make jobs manipulate page fragments.
- Add retry/discard policy only for a demonstrated failure mode. The current jobs intentionally inherit the default `ApplicationJob` behavior.

## Do Not

- Do not put business decisions in `perform`.
- Do not enqueue before persisting the transition that makes duplicate requests ineligible.
- Do not make a stale job restart completed, failed, or paused work.
- Do not rescue broadly in a job merely to hide a failure; store errors where the owning workflow can express them and let unexpected failures remain observable.
