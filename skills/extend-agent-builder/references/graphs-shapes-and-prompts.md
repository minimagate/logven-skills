# Graphs, shapes, and prompts

## Graph and shape contracts

Graphs operate on plain hashes from `Node#to_h` and `Edge#to_h`. Keep deterministic cycle detection, connectivity counting, and topological ordering under `Graphs`; do not embed them in prompts or controllers.

Shapes are the repository's compact contract language:

- root objects are hashes;
- primitives are `"string"`, `"number"`, and `"bool"`;
- arrays contain exactly one element shape;
- an optional hash key ends in `?`;
- runtime values use string keys.

`Shapes::Base` composes structure validation, runtime instance validation, inference, and subshape coverage. Add behavior to the focused validator/inference object rather than growing the facade.

Params nodes derive output shape from parsed JSON and cannot receive graph inputs. Tool nodes derive both shapes from the registered tool. Their shape writers intentionally ignore LLM-provided values. Preserve these computed contracts when changing graph ingestion.

LLM and Script nodes persist their shapes and require downstream input shapes to be covered by step input plus incoming-node output.

## Prompt boundary

Prompts live beside their subsystem under `app/models/builder/prompts/` and are loaded with `Llm::Prompt`. Keep them concise and align examples with the exact JSON contract accepted by `process_data`.

- System messages define the stage contract.
- User messages provide tools, the original step prompt, current step JSON, and repair errors as separate messages where the current builder does so.
- Do not duplicate model validations as sprawling prompt prose; the repair loop returns precise validation errors.
- Change prompt and parser/validator together when the wire shape changes.

## Tests

Use `with_llm` with an exact response queue. It fails on both extra requests and unused responses; keep that strictness because it proves retry behavior. Cover stage state, persisted graph/body results, repair feedback, retry exhaustion, computed Params/Tool shapes, and transaction rollback. Use direct graph/shape unit tests for deterministic algorithms.
