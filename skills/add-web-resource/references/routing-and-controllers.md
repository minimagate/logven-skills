# Routing and controllers

## Resource selection

Start by naming the state or operation as a resource. Logven has repeatedly replaced custom verb actions with small controllers whose action is ordinary CRUD:

- `agent_build` → `AgentBuildsController#create`
- `agent_commit` → `AgentCommitsController#create`
- `agent_revision` → `AgentRevisionsController#create`
- `step_build` → `StepBuildsController#create`
- nested `node_runs` → `NodeRunsController#update`

Use `resource` when the parent has one conceptual operation instance and no child ID is needed. Use `resources` when individual persisted children are addressed. Add only the actions required through `only:`. Keep nesting shallow and use `as:` only when it produces the established concise helper, such as `agent_build_path`.

Before adding `resume`, `publish`, `complete_node`, or similar member routes, ask whether the operation is automatic domain progression or a resource with `create`, `update`, or `destroy`. Node completion became `NodeRun#update`; run resume became automatic after paused node work completed.

## Controller shape

Keep an action linear:

1. Load the record or construct the proposed record.
2. Authorize it.
3. Call one domain method or persistence operation.
4. Redirect, render, or allow the matching Turbo Stream template to render.

Use a policy scope for every `index`; `ApplicationController` verifies this. Use eager loading where the action/view traverses known associations, as `AgentRunsController#index` and `#show` do.

Prefer `params.expect` in new or touched Rails 8.1 code:

```ruby
def step_params
  params.expect(step: %i[name description prompt])
end
```

Existing `require(...).permit(...)` call sites may remain when unrelated. Do not broaden accepted fields for convenience.

Use `save`/`update` branches when invalid input should re-render. Use bang persistence when the request represents an invariant-backed command and failure is exceptional. Return `:unprocessable_entity` for ordinary invalid forms; preserve an existing `:unprocessable_content` contract where the action is accepting structured completion content.

Do not add a `respond_to` block when Rails can select the `.turbo_stream.erb` template directly. Add explicit HTML/Turbo branches only when the two formats intentionally have different behavior, such as redirecting HTML while returning `head :no_content` to a sortable Turbo submission.

## Tests

Use `generate-tests`. Controller tests should prove status/redirect, persistence or side effects, enqueueing, and owner boundaries. Do not assert templates, partials, text, selectors, CSS classes, or rendered Turbo markup.
