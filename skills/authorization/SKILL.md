---
name: authorization
description: Design or change Logven Pundit policies, scopes, project roles, ownership checks, operation permissions, or authorization tests. Use for who may see or mutate data; do not put authorization rules only in views or controllers.
---

# Authorization

Treat policies as the single readable expression of access rules and scopes as the database-level expression of visible records.

## Start closed

`ApplicationPolicy` denies every action and requires every scope to implement `resolve`. Add only the permissions the resource needs. Rely on the inherited `new? -> create?` and `edit? -> update?` aliases unless the actions genuinely differ.

Every authenticated controller action must continue to satisfy `verify_authorized`. Every `index` action must also use `policy_scope` and satisfy `verify_policy_scoped`. A view-level `policy(...)` check controls presentation only; it never substitutes for controller authorization.

## Choose the right policy record

- Authorize an Active Record instance for record operations.
- Authorize the class for collection actions such as `index`.
- Use a headless symbol for singleton capabilities such as the dashboard or settings.
- Use a dedicated operation policy (`AgentBuildPolicy`, `StepOrderPolicy`, and peers) when the permission is about a domain command rather than generic CRUD. Pass `policy_class:` explicitly from the controller.

Keep policy inputs to `user` and `record`. If a rule appears to require unrelated request context, first select a better domain record.

## Compose existing authority

Project access is membership-based:

- Member access grants visibility.
- Owner or admin access grants project administration.
- Owner access grants destructive owner-only operations.
- The owner membership is immutable; policies must not offer transitions that the model rejects.

When a child resource derives permission from its project or agent, delegate to the owning policy instead of reimplementing the membership query. Keep small intent-revealing predicates such as `owned_by_user?`, `project_member?`, and `project_admin?` private.

Do not confuse creator ownership with project membership. Agent authoring and execution currently retain user ownership constraints even when the agent is attached to a shared project; preserve that distinction unless the product behavior is intentionally changed across policy, controller, model, and tests.

## Build safe scopes

- Return an `ActiveRecord::Relation`, not an array.
- Express visibility in SQL with joins, subqueries, `or`, and `distinct`; do not load records and filter in Ruby.
- Accept a class or relation so callers may scope through `@project` first.
- Reuse another policy scope when visibility is derived from it, as project membership, agents, runs, and manual node input do.
- Make scope and predicate agree. A record obtainable from a scope should pass its corresponding visibility predicate.

## Test the matrix

Policy tests should cover allowed and denied users, owner/admin/member distinctions, personal versus project records where relevant, lifecycle gates, and scope inclusion/exclusion. Test the actual boundary conditions; do not merely restate method names.
