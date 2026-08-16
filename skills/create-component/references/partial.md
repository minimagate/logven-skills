# Partial mechanics

This reference applies once `create-component`'s decision tree has placed a request in the
Partial category: composed markup scoped to one controller's view family, where the fragment can
lean on the current request context when that keeps it truly one-action-local, but explicit
inputs should be the default once the fragment is shared or its dependencies stop being obvious.
If the fragment needs to be reusable outside that view family or tested in isolation, back up —
that's `references/view-component.md` instead.

## File layout & naming

- Location: alongside the views that use it, under `app/views/<controller>/`, prefixed with an
  underscore — `app/views/dashboards/_summary.html.erb` for a `DashboardsController` partial.
- A partial shared across multiple controllers' views (rare — if it's shared across *unrelated*
  controllers, prefer a ViewComponent instead) lives in `app/views/shared/` or
  `app/views/application/` for layout-level fragments like flash messages.
- Rendered with `<%= render "summary" %>` (relative to the same directory) or
  `<%= render "shared/flash" %>` (path relative to `app/views/`).

## Data: implicit vs explicit

- A partial automatically sees whatever instance variables the triggering controller action set
  (`@workflow`, `current_user`, etc.), but treat that as a convenience for one-action-local
  fragments rather than the default contract for shared markup.
- Prefer explicit `locals:` for anything not obviously implied by the controller action,
  especially when the same partial is rendered from more than one action:
  `<%= render "form", locals: {workflow: @workflow} %>`. This keeps the sharing intentional —
  a partial reused across two actions that both set `@workflow` is fine; one that silently
  depends on an ivar only *one* of its callers sets is a bug waiting to happen.
- Collection rendering: `<%= render @workflows %>` (looks up `_workflow.html.erb`, exposes each
  element as `workflow`), or the explicit form
  `<%= render partial: "workflow", collection: @workflows %>` when the collection's element
  class doesn't match the partial name.

## What NOT to do

- Don't use a partial for markup meant to be reused outside its view family, or that needs an
  explicit input contract — that's ViewComponent territory (see
  `references/view-component.md`).
- Don't let a partial hold business logic (querying, mutating state) — same rule as views
  generally; compute the result in the controller/model and pass it in.
- Don't keep growing a partial's `locals:` list or its call sites once it's showing up in
  unrelated controllers — that's the signal to promote it to a ViewComponent instead of adding
  another `locals:` entry.
- Don't write a dedicated or indirect rendering test for a partial. Verify it in the browser;
  controller tests in this repository cover HTTP and application behavior, not rendered markup.
