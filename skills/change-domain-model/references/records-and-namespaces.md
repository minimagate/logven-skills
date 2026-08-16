# Records and domain namespaces

## Active Record structure

Declare relationships explicitly, including `class_name`, `foreign_key`, `source`, and `inverse_of` where namespacing or graph edges make inference ambiguous. Put ownership at the top of each aggregate and use dependent behavior intentionally.

Logven uses STI for `Nodes::Base` on `nodes.type` and `Credentials::Base` on `credentials.type`. Add variants beneath the existing namespace and extend the base type/label maps. Do not introduce a parallel `kind` persistence column; node `kind` is the external lowercase projection of STI `type`.

Status maps pair persisted string values with human labels, then define string-backed enums:

```ruby
STATUSES = {
  "draft" => "Draft",
  "ready" => "Ready"
}

enum :status, STATUSES.keys.index_with(&:itself), default: "draft"
```

Reuse the owning status vocabulary where run layers share it. Do not add integer-backed status values or scatter display labels through views.

Use Discard and `default_scope -> { kept }` only for aggregates that deliberately support archival. Tests must distinguish visible count from `unscoped` persistence.

## Plain domain objects

Place cohesive non-record logic in a descriptive namespace under `app/models/`, matching `Builder`, `Runner`, `Graphs`, `Shapes`, `Llm`, `Tools`, and `Apis`. Do not add a generic `services/` layer.

- Initialize with the record or plain inputs the object operates on.
- Expose one clear operation such as `build`, `run`, `compute`, `validate`, or `infer`.
- Return plain values or the updated owning record.
- Keep deterministic algorithms independent of controllers and views.
- Inject boundary options where tests need control, such as runner timeout or LLM configuration.

If work belongs specifically to building, running, or tools, use the narrower `extend-agent-builder`, `extend-agent-runner`, or `add-agent-tool` skill.
