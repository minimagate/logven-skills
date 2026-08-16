# Authorization and authentication

## Default contract

`ApplicationController` requires authentication, includes `Pundit::Authorization`, verifies `authorize` after every action, and verifies `policy_scope` after `index`. New authenticated controllers inherit that contract without opting out.

- Call `authorize record` after loading or constructing it.
- Use `policy_class:` when an operation resource authorizes a domain record through a specialized policy, as build/commit/revision controllers do.
- Implement policy predicates in terms of both ownership and allowed lifecycle state. Controllers should not duplicate those eligibility checks.
- Add a policy scope when a collection or scoped child lookup must be restricted by user ownership.

Use `policy_scope(...).find(...)` when not-found behavior is the intended isolation contract, as with `NodeRun`. Loading then authorizing is also established for ordinary owner resources such as `Agent` and `Step`; preserve the nearest resource's existing contract rather than changing 403/404 behavior incidentally.

Views may use policies to decide whether to display actions, but the controller policy remains authoritative.

## Explicit exceptions

Only authentication, password recovery, and external callback entrypoints currently bypass the default hooks:

- Declare `allow_unauthenticated_access` narrowly.
- Pair a truly public controller with `skip_after_action :verify_authorized` because there is no signed-in Pundit user.
- Keep sign-in and password-reset submission rate limits.
- Treat OAuth callback state as authorization context: verify signed state, allowlist the credential base class before constant use, and handle invalid signatures without persisting credentials.

Do not skip authorization merely to satisfy the verification callback. Do not load another user's credential through an unscoped global finder; use the current user's association or an ownership policy scope.
