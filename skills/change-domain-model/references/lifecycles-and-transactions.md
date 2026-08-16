# Lifecycles and transactions

## State-owned methods

Put a lifecycle operation on the record whose state it changes. Controllers and jobs call that method; they do not reproduce transitions.

- Name command methods with `!` when they persist or may raise.
- Start with an eligibility guard, returning without work when the state is stale or already handled.
- Expose predicate methods such as `buildable?`, `steps_ready?`, and `resumable?` for policies and callers.
- Use `ensure` for parent cleanup that must happen after both success and failure.
- Store stage-specific errors at the stage that can explain them.

Conditional validations enforce the contract of the state being entered. Draft records may be incomplete; promotion to `with_graph` or `ready` activates graph, shape, body, name, and description invariants. Do not weaken validation to make orchestration pass.

## Multi-record changes

Use a transaction when one operation creates or promotes several associated records, such as agent revision, graph replacement, or node promotion. Build explicit ID maps when copying graph edges so new edges never retain source IDs.

Use `with_lock` when concurrent mutations would otherwise lose ordering or state. `Agent#reorder_steps!` locks the aggregate, rearranges the loaded ordered list, then updates only positions that changed.

Keep copy contracts explicit through methods such as `revision_attributes`. Do not use unrestricted `attributes` cloning: omit IDs, timestamps, status, ownership, and lineage unless the operation explicitly sets them.

Use after-commit callbacks for Turbo delivery because the persisted change is already authoritative. Avoid callbacks for orchestration when an explicit command method can express sequencing and error handling more clearly.
