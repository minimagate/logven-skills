---
name: rails-authorization
description: Implement or review Pundit policies, scopes, roles, ownership boundaries and state-aware permissions.
---

# Rails Authorization

Apply the [shared principles](../how-we-work/SKILL.md#principles). Policies own permission decisions; domain objects own intrinsic validity.

## Enforce permissions

Deny by default in `ApplicationPolicy`; explicitly opt into permissions. Enforce `verify_authorized` and `verify_policy_scoped` on indexes. Only established unauthenticated entry points opt out; never widen a skip to make an action pass.

Authorize the matching action (`new?` for `new`), normally with `authorize @record`. A state-changing, destructive, sending or charging action requires its write permission, never merely `show?`.

Give a distinct operation a dedicated policy when its rules differ. Delegate shared access rules to the related policy and add only the operation's predicate. Make permissions sensitive to meaningful lifecycle state.

## Scope access

Load nested records through the authorized parent, then authorize the result: `@account.invoices.find(params[:id])`. Use `policy_scope` for indexes; do not repeat scoping where association ownership and authorization already cover a lookup. Model multi-hop relationships with associations.

Keep permission composition short and explicit: reuse established scoped guarantees and predicates instead of parallel permission state or redundant checks. Brevity never removes enforcement or tenant isolation.

Serve protected files through the established authorized path; possession of a signed/blob URL alone does not establish application permission. Check the actual delivery boundary.

## Keep one permission contract

Views consult the same policy methods; disabling a control does not replace server authorization. Keep permission branches out of controllers, validations and utility objects. Avoid class-switch dispatch and duplicate checks for guarantees already established by the context.

Before changing access, resolve sharing, archived records, ownership transfer and in-flight behavior relevant to this request. Record the chosen semantics; fix the rule rather than bypassing its symptoms.

## Verification

Verify the meaningful allow/deny matrix and tenant isolation using policy and narrow request tests. See [controllers](../rails-controllers/SKILL.md) for request flow and [tests](../rails-tests/SKILL.md) for non-visual assertions.
