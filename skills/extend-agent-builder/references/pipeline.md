# Builder pipeline

## Ownership and stages

`Step#build_now!` owns entry into building state and parent-agent cleanup. `Builder::Base#build!` owns the staged build and step-level failure record.

The pipeline is intentionally explicit:

1. `Builder::Details` converts `step.prompt` into name and description, then sets `with_details`.
2. `Builder::Graph` replaces nodes/edges, orders nodes, promotes to `with_graph`, and asks `Builder::Judge` for semantic approval.
3. `Builder::Bodies` visits nodes in graph order, generates LLM/script bodies where applicable, and promotes the step and nodes to `ready`.

Each stage accepts `(base, step)`, delegates shared LLM/prompt/tool access to the base, returns the step, and lets the base pass the updated record forward. Do not hide stage ordering in callbacks.

On any stage error, `Builder::Base` resets the step to draft, stores `e.message` in logs, and re-raises. `Step#build_now!` ensures the parent agent returns to draft. Keep those responsibilities separate.

## Graph replacement and repair

`Builder::Graph#process_data` replaces nodes inside a transaction, maps external lowercase `kind` values to STI classes, maps edge node names to newly created IDs, creates edges, and topologically orders nodes.

The repair loop checks persisted graph validity before asking the LLM for another answer:

1. Run `syntactic_errors` by promoting to `with_graph`; model validations cover existence, cycles, connectivity, names, and shape coverage.
2. Only when syntax is valid, run `semantic_errors` through `Builder::Judge`.
3. Persist current errors in step logs.
4. Stop on an empty error string; otherwise send prompt, tools, request, current graph, and errors to the LLM for repair.
5. Raise with the last error after `MAX_RETRIES`.

The judge response must be a hash and an invalid result must include a useful error. Do not treat unstructured approval text as success.
