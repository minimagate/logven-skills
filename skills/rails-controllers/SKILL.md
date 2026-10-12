---
name: rails-controllers
description: Use when adding or changing Rails controllers, routes, strong params, responses or Turbo Stream templates. Hands off policies to rails-authorization, domain logic to rails-models and views to rails-frontend.
---

# Rails Controllers

Keep controllers thin: load, authorize, call the model and render, following the [Principles](../how-we-work/SKILL.md) section.

Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs, it wins.

## Controllers stay thin

- Load nested records through the parent, as rails-authorization (Scoping) describes. Route nesting is not authorization.
- Authorize every action; `index` also calls `policy_scope` (rails-authorization).
- Use base controllers for shared loading (`Accounts::BaseController` sets the account).
- Keep controllers short (a screen or so) and extract to the model. The view gets one object (`@summary`) built from model methods (rails-models), not many ivars.
- One success path, one failure path: `if @approval.update` redirects with a short notice, otherwise `render :edit, status: :unprocessable_entity`.
- No `respond_to` scaffolding or format forks.

## Params

- Permit through one private `*_params` built on `params.expect(model: [...])`; `new` reuses it.
- Declare nested arrays and hashes explicitly. Never use `permit!`.
- Keep param keys identical across sibling forms.

## Routes

- Give every `resources` and `resource` an `only:` option. Use plain id URLs: no slugs, no clever constraints.
- Model each state change as a singular resource with its own controller and policy: `resource :approval, only: %i[create]`.
- No `member`, `collection` or extra custom actions on a broad controller.
- Put parent-owned controllers in a matching module (`Billing::InvoicesController`). Use `controller:` or `as:` sparingly.
- Reuse the existing page and form before adding a route. A different operation gets its own controller, not a conditional inside `update`.
- A route change updates controllers, redirects, `form_with` arrays, links, Turbo templates and tests in the same change.

## Responses

- Redirect for ordinary flows.
- In-place updates use Turbo Stream templates named after the action (`create`, `update`, `destroy`) that render the same `_show` and `_form` partials as the full pages.
- Place templates under the resource they render: `billing/invoices/approvals/_form`, not `billing/invoices/_approval_form`.
- Do not log params or records. The owning boundary logs a failure once.

## Verify

- `bin/rails routes` to confirm route names, nesting and `only:` options.
- `bin/rails test test/controllers/<path>` for each touched controller.
- The project's linter on the changed files.
