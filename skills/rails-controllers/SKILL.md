---
name: rails-controllers
description: Use when adding or changing Rails controllers, routes, strong params, responses or Turbo Stream templates. Hands off policies to rails-authorization, domain logic to rails-models and views to rails-frontend.
---

# Rails Controllers

Keep Rails controllers thin: load, authorize, call the model and render, following [principles](../principles/SKILL.md).
Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs from this skill, it wins.

## Controllers stay thin

- Load nested records through the parent: `@account.invoices.find`, never `Invoice.find`.
- Route nesting is not authorization. See `../rails-authorization/SKILL.md`.
- Authorize every authenticated action with its matching action. `index` also calls `policy_scope`.
- Use base controllers for shared loading: `Accounts::BaseController` sets the account.
- Keep controllers short (a screen or so); extract to the model.
- Move derived data into a model method and give the view one object (`@summary`), not many instance variables.
- Use one success path and one failure path: `if @approval.update` redirects with a short notice, otherwise `render :edit, status: :unprocessable_entity`.
- Do not add `respond_to` scaffolding or format forks.

## Params

- Permit through one private `*_params` method built on `params.expect(model: [...])`.
- Declare nested arrays and hashes explicitly. Never use `permit!`.
- Have `new` reuse the same params method as `create`.
- Keep param keys identical across sibling forms.

## Routes

- Give every `resources` and `resource` an `only:` option.
- Use plain id URLs. No slugs and no clever constraints.
- Model each state change as a small singular resource with its own controller and policy: `resource :approval`, with `only: %i[create]`.
- Do not add `member` or `collection` verbs, or extra custom actions, to a broad controller.
- Put parent-owned controllers in a matching module (`Billing::InvoicesController`). Use `controller:` or `as:` sparingly.
- Reuse the existing page and form before adding a page or route. A different operation gets its own controller, not a conditional inside `update`.
- When a route changes, update controllers, redirects, `form_with` arrays, links, Turbo templates and tests in the same change.

## Responses

- Redirect for ordinary flows.
- For in-place updates, name Turbo Stream templates after the action (`create`, `update`, `destroy`). They render the same `_show` and `_form` partials as the full pages.
- Place templates under the resource they render: `billing/invoices/approvals/_form`, not `billing/invoices/_approval_form`.
- Do not log params or records. Let the owning boundary log a failure once.

## Verify

- `bin/rails routes` to confirm route names, nesting and `only:` options.
- `bin/rails test test/controllers/<path>` for each touched controller.
- The project's linter on the changed files.
