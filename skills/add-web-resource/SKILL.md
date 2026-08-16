---
name: add-web-resource
description: Add or change a Logven route, controller action, Pundit policy, authenticated endpoint, form submission, or request contract. Use for CRUD resources, state-changing agent or step actions, nested resources, controller authorization, strong parameters, redirects/renders, and their integration tests.
---

# Add Web Resource

Model state-changing behavior as a resource, keep the controller thin, and make authorization part of the endpoint contract.

## Workflow

1. Inspect `config/routes.rb`, the nearest controller and policy, the owning domain model, call sites, and controller tests.
2. Decide whether the request fits an existing CRUD action or deserves a singular/plural resource. Prefer a small resource controller over a custom verb action.
3. Load or build the record, authorize it, delegate behavior to the owning model, and return the smallest correct response.
4. Preserve authenticated-by-default behavior and the repository's global Pundit verification.
5. If the response updates part of a page, use the `use-turbo` skill. If markup is being extracted or reused, use `create-component`.
6. Always use `generate-tests` for the route's non-visual HTTP and authorization contract.

Read [`references/routing-and-controllers.md`](references/routing-and-controllers.md) before changing routes or controllers. Read [`references/authorization-and-authentication.md`](references/authorization-and-authentication.md) before adding or changing policies, ownership scopes, public access, sessions, password flows, credentials, or OAuth callbacks.

## Core Rules

- Restrict `resources`/`resource` with `only:` and keep nesting to the relationship needed by the helper and lookup.
- Use ordinary `index`, `show`, `new`, `create`, `edit`, `update`, and `destroy` actions. Extract operations such as build, commit, or revision into their own resource rather than growing a parent controller with verbs.
- Keep orchestration and lifecycle transitions in models or existing `Builder`/`Runner` objects. Controllers coordinate HTTP only.
- Prefer `params.expect` for new/touched parameter whitelists; do not rewrite unrelated legacy `require`/`permit` call sites.
- Authorize constructed records when permission depends on the proposed association or state, such as `Step.new(agent: agent)` or `AgentRun.new(agent:, user:)`.
- Do not add rendered-output tests. Verify UI behavior in the browser and HTTP behavior in integration tests.

## Do Not

- Do not add a custom member action before testing whether it is a resource or automatic domain progression.
- Do not bypass `verify_authorized`, `verify_policy_scoped`, or user ownership to make a request pass.
- Do not duplicate policy predicates in controllers or rely on hidden buttons as authorization.
- Do not add response formats that no caller requests.
