---
name: rails-controllers
description: Implement Rails request flow, resourceful routes, strong parameters, redirects and Turbo Stream responses.
---

# Rails Controllers

Apply the [shared principles](../how-we-work/SKILL.md#principles): load, authorize, invoke domain behavior, respond.

- Find nested records through their authorized parent. Authorize every action; scope indexes through Pundit ([authorization](../rails-authorization/SKILL.md)). Shared base controllers may load common context; route nesting alone grants no access.
- If controller glue grows, first question the model, constraints and request contract; fix the mismatch rather than add coercion, fallback branches or another adapter. Keep the happy/failure paths direct.
- Keep domain rules in [models](../rails-models/SKILL.md). Controllers may explicitly select defaults and compose request inputs without teaching primitives about this page. Expose a coherent object to the view instead of distributing computed state across many variables.
- Permit parameters through one private `*_params`, using `params.expect` on supported Rails versions. Declare nested arrays/hashes explicitly, never `permit!`; keep keys consistent across sibling forms. Use assignment, nested IDs and `_destroy` instead of manual reconciliation or delete/recreate loops.
- Use standard resources with explicit `only:`. A distinct state-changing operation gets a singular resource, controller and policy, rather than custom member/collection actions or conditional operation dispatch inside `update`.
- Match parent-owned controllers to route hierarchy. Put identity/ownership context in explicit resource URLs; sessions may remember a preference but must not silently select a different owner. Query parameters may carry filters, pagination/sort and transient form/view state; keep ownership context explicit. Use plain identifiers and avoid unnecessary `controller:`, `as:` or route constraints. Reuse an existing page/form.
- Consolidate genuinely shared resource lifecycles; split different use cases instead of adding caller flags. Preview with the real unsaved/assigned model and render its form; persist only on explicit save. Apply URL state in memory on GET without writes.
- Ordinary flows redirect; invalid submissions render the form with `:unprocessable_entity`. Add response formats only for real callers; use action templates rather than scattering pagination-specific frame/stream branches across unrelated controllers and components. In-place changes use action-named Turbo Stream templates reusing canonical record/form partials ([frontend](../rails-frontend/SKILL.md)).
- Route changes update redirects, links, forms, templates and relevant request tests together. Keep partials under the resource they render. Do not log request parameters or records.

Check `bin/rails routes`, narrow request contracts and lint. Follow [rails-tests](../rails-tests/SKILL.md): status, redirects, permissions and effects; no rendered-markup or DOM assertions.
