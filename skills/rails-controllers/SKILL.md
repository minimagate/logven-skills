---
name: rails-controllers
description: Use when adding or changing Rails controllers, routes, strong params, responses or Turbo Stream templates. Hands off policies to rails-authorization, domain logic to rails-models and views to rails-frontend.
---

# Rails Controllers

Keep Logven's Rails controllers thin: load, authorize, call the model and render, following [principles](../principles/SKILL.md).

## Controllers stay thin

- Load nested records through the parent: `@project.workflows.find`, never `Workflow.find`.
- Route nesting is not authorization. See `../rails-authorization/SKILL.md`.
- Authorize every authenticated action with its matching action. `index` also calls `policy_scope`.
- Use base controllers for shared loading: `Projects::BaseController` sets the project, `Workflows::BaseController` sets the workflow.
- Use the `ApplicationController` macros (`navigation`, `section`, `assistant_context`) instead of ad-hoc matching.
- Keep each controller under 80 lines.
- Move derived data into a model method and give the view one object (`@summary`), not many instance variables.
- Use one success path and one failure path: `if @build.update` redirects with a short notice, otherwise `render :edit, status: :unprocessable_entity`.
- Do not add `turbo_frame_request?` forks or `respond_to` scaffolding.

## Params

- Permit through one private `*_params` method built on `params.expect(model: [...])`.
- Declare nested arrays and hashes explicitly. Never use `permit!`.
- Have `new` reuse the same params method as `create`.
- Keep param keys identical across sibling forms.

## Routes

- Give every `resources` and `resource` an `only:` option.
- Use plain id URLs. No slugs and no clever constraints.
- Model each state change as a small singular resource with its own controller and policy: `resource :build`, `:commit`, `:revision`, `:rerun`, each with `only: %i[create]`.
- Do not add `member` or `collection` verbs, or extra custom actions, to a broad controller.
- Put parent-owned controllers in a matching module with `scope module: :projects`. Use `controller:` or `as:` sparingly.
- Reuse the existing page and form before adding a page or route. A different operation gets its own controller, not a conditional inside `update`.
- When a route changes, update controllers, redirects, `form_with` arrays, links, Turbo templates and tests in the same change.

## Responses

- Redirect for ordinary flows.
- Return `head :no_content` for autosave.
- For in-place updates, name Turbo Stream templates after the action (`create`, `update`, `destroy`). They render the same `_show` and `_form` partials as the full pages.
- Place templates under the resource they render: `steps/_form`, not `agents/_step_form`.
- Do not use Turbo Frames in Logven.
- Do not log params or records. Let the owning boundary log a failure once.

## Verify

- `bin/rails routes` to confirm route names, nesting and `only:` options.
- `bin/rails test test/controllers/<path>` for each touched controller.
- `bin/standardrb` on the changed files.
