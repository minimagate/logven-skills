---
name: change-domain-model
description: Add or change Logven Active Record models or namespaced domain objects. Use for associations, STI nodes or credentials, validations, string-backed statuses, lifecycle commands, graph-related transactions, locking and ordering, revisions, soft deletion, callbacks, or extracting cohesive logic under `app/models`.
---

# Change Domain Model

Put behavior with the object that owns the invariant, and preserve the existing aggregate and lifecycle boundaries.

## Workflow

1. Trace the model's associations, policies, controllers/jobs, state predicates, callbacks, schema, and nearest tests.
2. Identify the owning invariant and put the operation on that record or an existing namespaced domain object.
3. Preserve explicit lifecycle eligibility, conditional validation, ownership, and transaction boundaries.
4. Keep controllers/jobs as callers. Use `add-web-resource` or `add-background-work` when those delivery layers also change.
5. Use the narrower `extend-agent-builder`, `extend-agent-runner`, or `add-agent-tool` skill when changing those subsystems.
6. Always use `generate-tests` for observable domain behavior and failure boundaries.

Read [`references/records-and-namespaces.md`](references/records-and-namespaces.md) for Active Record/STI and plain-object placement. Read [`references/lifecycles-and-transactions.md`](references/lifecycles-and-transactions.md) before changing status transitions, promotion, revision, ordering, callbacks, or multi-record operations.

## Core Rules

- Prefer the smallest Rails-native model or plain Ruby object; do not create a generic service layer.
- Keep persisted statuses as strings and display labels in the model's status map.
- Guard commands so stale calls and async retries do no work.
- Validate contracts at the lifecycle point where they become required.
- Use public effects and errors as the test contract; do not test private helpers or incidental query shape.

## Do Not

- Do not move domain decisions into controllers, jobs, views, or Stimulus.
- Do not bypass validation with column updates except for a narrow, already-established internal operation such as locked reordering or seed timestamps.
- Do not use callbacks for a workflow that needs explicit sequencing, retries, or error ownership.
- Do not clone unrestricted attribute hashes across revisions or STI records.
