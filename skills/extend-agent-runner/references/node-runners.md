# Node runners and outputs

## Params

Parse the node body JSON and complete with that object. Params body validation and inferred output shape belong to `Nodes::Params`; the runner should not duplicate them.

## Script

Execute JavaScript in `MiniRacer::Context` with the configured millisecond timeout. Evaluate the body, call the function named after the node with JSON input, and store the returned value. Preserve distinct timeout, runtime, and parse error messages because they surface in node/run logs.

Do not interpolate untrusted function identifiers beyond the validated node-name contract without revisiting validation. Do not remove the timeout.

## LLM

Send the runner system prompt, node input, expected output shape, and node body as separate messages. Use `Llm::Chat#request_json` so invalid JSON is repaired before updating the node run to completed. Change prompt and output contract together.

## Tool

Resolve the class from `Tools::Base.find(node_run.body)`, instantiate it with the run user and merged input, call `run!`, then store its output. Tool metadata and credential/API behavior belong to `add-agent-tool`.

## Output validation and artifacts

`NodeRun` validates output against `output_shape` only when completed. Failed or paused runs may have no valid output. Keep validation at the record transition so every runner and human completion shares the same contract.

Artifacts are named run-level outputs associated with `AgentRun`; they are not a substitute for node dataflow. Preserve optional format metadata and run-dependent cleanup.

## Tests

Use `generate-tests`. Cover deterministic output, status, logs, timeout/error mapping, input merge, skipped completed work, pause/resume enqueueing, and shape rejection. Stub only external/nondeterministic boundaries; use real Params/Script execution where practical and `with_llm` for LLM nodes.
