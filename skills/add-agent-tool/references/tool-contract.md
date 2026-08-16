# Tool contract

## Class and metadata

Add a named subclass beneath `app/models/tools/<provider>/`. The class inherits `Tools::Base` and declares:

- globally unique snake-case `tool_name`;
- optional human `display_name`;
- `brand` when tools should group under a provider asset;
- concise model-facing `description`;
- `input_shape` and `output_shape` using the Logven shape language;
- `run!` returning the declared output object.

Instances receive `user:` and string-keyed `input:`. Use the user to resolve credentials through owned associations. Do not store mutable registration data on instances.

`tool_name` registers the class. `Tools::Base` eagerly requires tool files, then validates named registered classes at boot. Validation requires the name, description, both shapes, and valid shape syntax. Preserve fail-fast boot behavior; do not defer invalid metadata until an agent run.

Named classes may not take another named class's tool name. Anonymous test classes may replace registrations so isolated tests can create fake tools. Use `fake_tool_class` rather than adding fake production files.

## Shapes

Use string keys and repository primitives (`string`, `number`, `bool`). Suffix optional input keys with `?`; use a one-element array for homogeneous lists. Output must match its shape when the `NodeRun` completes.

Tool nodes read shapes from the registry and ignore assigned/generated shapes. When changing a tool contract, update tool metadata, any builder prompt/example implications, stored node compatibility assumptions, runner/API tests, and the development seed if it uses the tool.

## Tests

Use `generate-tests`. Test metadata/registration through `Tools::Base`, tool behavior through the named tool test, and external calls by stubbing the API boundary. Assert returned plain data and material error behavior, not private extraction helpers.
