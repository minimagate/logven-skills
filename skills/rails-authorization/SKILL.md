---
name: rails-authorization
description: Use for Pundit policies, policy scopes, authorize calls, roles and permissions, and who can see or do what in Logven Rails code, including workflows, runs and projects. Hands request flow, routes and strong params to rails-controllers.
---

# Rails Authorization

Pundit rules for Logven: every action is authorized, each rule has one owner, and policies are the only place permission logic lives.
Shared engineering rules are in [principles](../principles/SKILL.md). Request flow belongs to `rails-controllers`.

## Never skipped

- Rely on `ApplicationController` for `verify_authorized`, and for `verify_policy_scoped` on `index`. Only sessions, passwords and oauth_callbacks opt out.
- Do not add `skip_authorization` or widen a skip to make an action pass. Fix the policy.
- `ApplicationPolicy` denies by default. Every permission is an explicit opt-in method.

## Right policy, right action

- Authorize with the action that matches the request: `new` is checked with `new?`, not `create?`. Prefer plain `authorize @record`.
- Give an operation with different rules its own policy via `policy_class:`, such as `WorkflowBuildPolicy`, `WorkflowCommitPolicy` or `WorkflowSpecPolicy`.
- Delegate that policy to the closest related rule (`WorkflowPolicy#update?`, `ProjectPolicy`) and add only its domain predicate, such as `buildable_later?`.
- Make rules state-aware: a workflow is editable only while it is a draft.
- Starting a run spends credits, so require `update?`, not `show?`.
- Policies must not contradict each other or check the same thing twice.

## One source of truth

- Keep each action's rule in its policy method. Views reuse it: disable the form when `policy(workflow).update?` is false.
- Do not re-check what the context already guarantees, such as `policy(run).show?` inside a list of already-scoped runs.
- Keep permission logic out of model validations, controllers and plain Ruby objects.
- Do not bypass Pundit with hand-rolled `case record.class` checks.

## Scoping

- Look up members through the authorized parent and then `authorize`: `@project.node_runs.find(params[:id])`.
- Skip `policy_scope` when `authorize` plus association scoping already covers the lookup. Use `policy_scope` in `index`.
- Build multi-hop access with `has_many :through` on the parent, not hand-written joins.

## Meaning before code

- Before a permission change, decide the product semantics and write them in the plan. Cover archived records, sharing, who sees which runs, and what in-flight work does when its owner changes.
- Change the rule, not the symptom.

## Verify

- Every policy has a policy test. Run `bin/rails test test/policies`.
- Controller tests cover the unauthorized and authorized paths of the changed action. Run `bin/rails test test/controllers/<path>`.
