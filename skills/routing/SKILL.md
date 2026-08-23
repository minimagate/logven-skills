---
name: routing
description: Add or change Logven Rails routes, resource nesting, URL helpers, project-scoped modules, or operation endpoints. Use when mapping HTTP resources to controllers; keep routes resourceful and aligned with controller ownership.
---

# Routing

Keep `config/routes.rb` compact, resourceful, and readable from top to bottom. Inspect `bin/rails routes` and the affected controller/view helpers before changing it.

## Follow the current map

- Top-level authenticated navigation uses ordinary plural resources such as projects.
- Project-owned controllers live in the `Projects` module while URLs remain under `/projects/:project_id`; express this with `scope module: :projects` inside `resources :projects`.
- Use singular `resource` for one conceptual operation per parent, including build, commit, revision, step order, settings, session, and OAuth callback.
- Use plural `resources` for collections and member records such as agents, steps, runs, node runs, and project memberships.
- Declare `only:` for every resource. Do not expose unused Rails actions.
- Use `controller:` when the public resource name should differ from the implementation name, as project `members` maps to `ProjectMembershipsController`.
- Use `as:` sparingly to make nested operation helpers read naturally and avoid collisions.

## Model actions as resources

Do not add `member` or `collection` verbs to an already broad controller when a small operation resource gives the action its own policy and controller. Prefer `POST /agent/build` handled by a build resource over `POST /agent/build_now` handled by `AgentsController`.

Nest only when the parent is part of identity, authorization context, or navigation. When a route is nested, the controller must verify the child belongs to that parent; URL structure alone does not enforce it.

Keep route names in product language. Internal class names may differ through `module`, `scope`, `controller`, and `as` without leaking awkward implementation terms into URLs.

## Update consumers together

When changing a route, update controllers, redirects, `form_with` model arrays, `link_to`/`button_to`, Turbo templates, mailers, and controller tests in the same change. Prefer generated helpers over string URLs.

## Verify

Run `bin/rails routes` and inspect the exact verb, path, controller action, and helper. Then run the narrow controller tests that exercise the changed helpers and request contract.
