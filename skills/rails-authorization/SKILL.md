---
name: rails-authorization
description: Use for Pundit policies, policy scopes, authorize calls, roles and permissions, and who can see or do what in Rails code. Hands request flow, routes and strong params to rails-controllers.
---

# Rails Authorization

Pundit rules: every action is authorized, each rule has one owner, and policies hold all permission logic. Request flow belongs to rails-controllers; shared rules are in the [Principles](../how-we-work/SKILL.md) section.

Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs, it wins.

## Never skipped

- `ApplicationController` enforces `verify_authorized`, and `verify_policy_scoped` on `index`. Only unauthenticated entry points opt out (such as the sessions and passwords controllers from Rails' authentication generator, listed in the project skill).
- Never add `skip_authorization` or widen a skip to make an action pass. Fix the policy.
- `ApplicationPolicy` denies by default; every permission is an explicit opt-in method.

## Right policy, right action

- Authorize with the matching action: `new` is checked with `new?`. Prefer plain `authorize @record`.
- Give an operation with different rules its own policy via `policy_class:` (`InvoiceApprovalPolicy`). Delegate to the closest related rule (`InvoicePolicy#update?`) and add only its domain predicate (`approvable?`).
- Make rules state-aware: an invoice is editable only while it is a draft.
- Actions that change state, send or charge something, or are destructive need more than `show?`: use `update?` or a dedicated policy.

## One source of truth

- Keep each rule in its policy method. Views reuse it: disable the form when `policy(invoice).update?` is false.
- Do not re-check what the context already guarantees, such as `policy(invoice).show?` inside an already-scoped list. Policies must not contradict each other or check the same thing twice.
- Keep permission logic out of model validations, controllers and plain Ruby objects. No hand-rolled `case record.class` checks.

## Scoping

- Load nested records through the authorized parent, then `authorize`: `@account.invoices.find(params[:id])`, never `Invoice.find`.
- Skip `policy_scope` when `authorize` plus association scoping already covers the lookup. Use it in `index`.
- Build multi-hop access with `has_many :through` on the parent, not hand-written joins.

## Meaning before code

- Before a permission change, write the product semantics in the plan: archived records, sharing, who sees which records, and what in-flight work does when its owner changes.
- Change the rule, not the symptom.

## Verify

- `bin/rails test test/policies`
- `bin/rails test test/controllers/<path>` for each touched controller, covering the unauthorized and authorized paths of the changed action.
