---
name: domain-models
description: Implement or refactor Logven Active Record models and namespaced domain objects, including associations, validations, state transitions, STI nodes, graph/shape logic, and persistence invariants. Use for domain behavior; use agent-runtime for execution-specific changes.
---

# Domain Models

Keep domain behavior close to the data and contracts it protects. This repository intentionally uses Active Record models plus focused namespaced Ruby objects under `app/models/`; do not introduce a service-layer directory or a generic command framework.

## Select the existing boundary

- Active Record models own associations, persistence validation, lifecycle commands, transactions, locks, broadcasts, and revision attributes.
- `Nodes::*` uses STI over the `nodes` table. `Nodes::Base` defines the shared contract; each subtype owns only its kind-specific derived fields and validation.
- `Builder::*`, `Runner::*`, `Graphs::*`, `Shapes::*`, `Tools::*`, `Credentials::*`, `Apis::*`, and `Llm::*` are plain namespaced objects organized by domain responsibility.
- Jobs are thin asynchronous entry points that call a model command.

Extend the nearest existing namespace. Extract a new object only when it gives a coherent algorithm or adapter a clear home; do not extract a one-line wrapper around a model method.

## Model durable invariants

- Declare associations with explicit dependency behavior and `inverse_of` or `class_name` where Rails cannot infer it.
- Back uniqueness and relationship invariants with database indexes and foreign keys as well as model validation.
- Use string-backed enums because persisted status values are readable and shared across agent, step, and run state machines.
- Keep status labels in the model constants already used by the UI. When adding a state, update transitions, policies, jobs, UI tone mapping, and tests together.
- Keep discard behavior consistent for user-facing top-level records. Default kept scopes are established here; account for them explicitly when querying discarded data.
- Use transactions for multi-record invariants and `with_lock` or an atomic conditional update for competing transitions.
- Prefer command methods that leave the record in a valid observable state or raise. Make idempotent no-op guards explicit where jobs may run more than once.

## Preserve graph and shape contracts

An agent owns ordered steps. A step owns typed nodes and directed edges. Node names are unique within a step, edges connect nodes from that same step, ready graphs are non-empty, connected, acyclic, and topologically ordered.

Shapes are JSON-like contracts composed of hashes, homogeneous lists, and `string`, `number`, or `bool`; a trailing `?` marks an optional key. Use `Shapes::Base` for validation, coverage, casting, inference, and strong-parameter generation instead of duplicating shape traversal.

For STI nodes, derived attributes such as tool shapes or params output shapes remain derived. Do not persist caller-provided values by bypassing subtype readers/writers.

## Keep APIs narrow and legible

Use intent-revealing public methods such as `commit!`, `promote!`, `complete_with!`, and `revise_for`. Keep query helpers side-effect free. Keep serialization methods (`to_h`, `revision_attributes`) explicit so prompts, graphs, and copies do not accidentally expose new columns.

Avoid broad rescues. When translating an expected subsystem error, preserve a useful message or log; let unexpected failures reach the existing lifecycle recovery boundary.

## Keep domain code cohesive

- Make the smallest change in the nearest existing model or namespace. Do not add repositories, generic services, concerns, callbacks, metaprogramming, or value objects unless they give a real repeated invariant or coherent algorithm one clear owner.
- Keep public methods narrow, transitions explicit, and queries side-effect free. Prefer readable sequential code and small private predicates over callback webs, cross-model condition chains, and duplicated state logic.
- Test only changed invariants, transitions, and observable failure paths. Do not retest Rails associations, enum declarations, private helpers, or every combination already covered at another boundary.
- Log only actionable lifecycle or subsystem failures at the owner that handles them. Do not log routine saves, callback entry, full record attributes, or the same exception at multiple layers.

## Verify

Test the changed invariant or transition and its meaningful rejection path. Add rollback,
idempotency, concurrency, shape, ordering, or broadcast coverage only when the change touches that
contract. Use the attribute helpers in `test/test_helpers/attributes/` and the smallest suitable
`ActiveSupport::TestCase`.
