# Questions for one adversarial reviewer

Use these to challenge the whole change, without a rigid lens quota or additional agents. Read beyond the patch wherever a hypothesis requires it; this is not an unsolicited whole-repository audit.

- **Intent:** Does the code solve the actual request? Which assumptions or product decisions could be wrong even if every local convention is followed? Are omitted cases within the real contract?
- **Boundaries:** Can another tenant, unauthorized role or hostile input reach this path? Check indirect lookups, mass assignment, injection, secrets and sensitive logging; UI restrictions are not authorization.
- **Time and failure:** What happens twice, out of order, concurrently, after a timeout, between transaction and side effect, or during recovery? Prove whether existing locks, constraints and idempotency actually protect it.
- **Integration:** Do existing callers, external protocols, persistence and deployment sequencing still agree? Can old data or a partial rollout violate the new assumptions? Trace deletion and ownership chains.
- **Load:** Are memory, query count, latency and external calls reasonable for plausible usage? Name the workload; do not manufacture scale requirements.
- **Composition:** Does a new capability work through a local boundary, or force unrelated components to understand its transport? Are canonical typed controls reimplemented? Can add/remove/reorder or invalid unsaved input leave stale state? Can custom content drop mandatory controls?
- **Representation:** Does each query return the entity/cardinality the page represents, using canonical predicates/metrics? Are protocol variants unambiguous and defaults truthful? Does one fact have several mutable representations? Are known entities hidden in blobs? Would correcting ownership delete reconciliation? Are primitives choosing caller policy or callers duplicating intrinsic rules?
- **Complexity:** Can an existing API, native feature or direct method replace machinery? Are types/options, controllers, wrappers or configuration earning their place? Preserve meaningful single-caller boundaries and useful user choices.
- **Evidence:** Would the relevant tests catch this failure? Do not propose UI/DOM tests. Verify nonvisual logic and HTTP effects; inspect UI manually. Do not weaken a correct regression test to make checks pass.

A missing repository rule cannot dismiss a concrete correctness, security or reliability defect. Conversely, a guideline violation alone does not prove a catastrophic bug. Before declaring an API dead or a default wrong, check framework/dynamic callers and history. Rank by actual consequence, state uncertainty and show what was checked to falsify each finding. [Direct review evidence](../../how-we-work/references/review-patterns.md) supplies examples, not the limits of review.
