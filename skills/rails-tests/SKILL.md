---
name: rails-tests
description: Plan, write, repair, or review tests for any Rails code change, including questions about coverage or regressions and deciding what belongs in Minitest. Enforce minimal logic and HTTP-contract tests; never add UI, DOM, rendered-markup, ViewComponent, system, or browser tests.
---

# Rails Tests

Write the smallest maintainable Minitest coverage that proves requested application behavior.
Mandatory rule: generated tests must use the minimum lines of code possible (the per-page and per-branch request tests are always required). Do not add setup,
helpers, assertions, cases, or abstractions that are not required to prove the contract.
Test logic and non-visual application contracts only. Never test presentation or browser behavior,
even when the request concerns UI code. Verify UI changes in the browser instead of encoding their
appearance or DOM structure in the test suite.
Protect the test's behavioral contract when diagnosing failures.

Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs from this skill, it wins.

## Workflow

1. Establish the intended behavior from the request, application code, and existing tests. Read
   `test/test_helper.rb`, the nearest related tests, and relevant helpers before writing code.
2. Run the narrow existing test file first when practical. Distinguish a pre-existing failure
   from one introduced by the change.
3. Decide whether the change has a non-visual behavioral contract worth testing. Purely visual,
   markup-only, CSS, and component-composition changes require no automated test. When a logic or
   HTTP contract exists, choose the narrowest layer that proves it:
   - Model, plain domain object, or policy: inherit
     `ActiveSupport::TestCase` and place the test under the matching `test/models/` or
     `test/policies/` path.
   - Policy tests should prove the meaningful permission matrix and policy-scope membership,
     including denial and isolation boundaries where they differ by role or ownership.
   - Controller or HTTP contract: inherit `ActionDispatch::IntegrationTest` under
     `test/controllers/`. Assert authentication, authorization, status/redirect, persistence,
     side effects, and other request-level functionality.
   - Mailer or job: use the matching Rails non-system test API and repository location.
     Job tests should assert delegation and resulting application state, not Active Job internals.
   - External provider and tool tests should isolate network boundaries and prove the relevant
     request/response contract. Never call a live provider from tests.
   - Controller tests must stop at the HTTP/application boundary: authentication, authorization,
     status or redirect, persistence, side effects, and response format where it is an API
     contract. Do not assert HTML response bodies, rendered text, selectors, CSS classes, DOM
     structure, templates, partials, or components.
   - Do not create `ApplicationSystemTestCase`, `ViewComponent::TestCase`, view, browser, or other
     render-based tests. If presentation code contains important business rules, move those rules
     to a non-presentation object when that is in scope and test the public logic there.
4. Arrange only the records and inputs required for the scenario, perform one meaningful action,
   and assert observable outcomes. Keep each test in its shortest clear form. Cover the requested happy path and material failure or
   authorization boundary without building a combinatorial suite.
5. Run the changed test file, then the smallest relevant directory or broader suite warranted by
   the change. Run the project's linter (for example `bin/standardrb` or `bin/rubocop`) on changed Ruby test files.

## Repository Conventions

- Use Minitest's `test "behavior" do` style and `require "test_helper"`.
- Mirror source namespaces and paths in `test/`.
- Use the project's record setup: fixtures by default in a fresh Rails app; builders or factories only if the
  project skill names them. Keep scenario-specific values in the test.
- Use the application's existing authentication helper for authenticated request tests.
- Stub external interactions with Minitest stubs or WebMock unless the project skill names a stubbing
  helper. Preserve any contract that rejects missing or unused stubbed responses.
- Prefer precise assertions such as `assert_difference`, `assert_no_difference`,
  `assert_changes`, `assert_raises`, `assert_predicate`, exact persisted values, and policy scope
  results. Assert public effects rather than private implementation details.
- Stub only true boundaries or nondeterminism, such as external services, time, or randomness.
  Do not stub the behavior under test.
- Reload records before asserting persisted state when persistence is part of the contract.
- Use `assert_enqueued_with` or `perform_enqueued_jobs` for asynchronous boundaries.
- Keep tests isolated and order-independent because the suite runs in parallel by processor
  count. Do not depend on fixed database IDs, wall-clock races, global ordering, records from
  another test, or shared mutable registries without cleanup.
- Test claim, resume, and idempotency behavior when concurrent or duplicate work could create
  duplicate children or repeat side effects.
- Every controller gets at least one request test per page and one per action branch (valid and invalid), even if it only does `get path; assert_response :ok`; this is the test that catches a missing template. Assert status, redirect, persistence, jobs and authorization, never HTML.
- One test file per class, mirroring the source path (`test/models/billing/invoice_test.rb` for `app/models/billing/invoice.rb`). An extracted plain Ruby object gets its own test in the same change, and a deleted feature's tests are deleted with it.
- Every policy has a policy test. Name test classes after their unit (`InvoicePolicyTest`, not a generic name), and reference app classes with a leading `::` inside nested test modules.
- Stub external calls (HTTP, mail delivery, payment/LLM providers) with Minitest stubs or WebMock unless the project skill names a stubbing helper; a test must never reach a live provider.
- Assert mail and jobs through `ActionMailer::TestHelper` and `ActiveJob::TestHelper` (enqueued, delivered, arguments); do not assert rendered bodies or PDF contents beyond a contract the model owns.
- Prefer explicit per-case assertions over data-driven graders.

## Keep test code hygienic

- Use the project's existing setup helper and the direct public API. Do not introduce a factory DSL, shared context,
  test harness, custom assertion, or helper abstraction unless repeated setup becomes materially
  shorter and clearer.
- Keep every test linear and legible: arrange, perform one meaningful action, and assert the
  contract. Avoid branching, loops, metaprogrammed cases, deep helper chains, and setup shared by
  unrelated scenarios.
- Never add production logging or instrumentation merely to make a test observable. Do not assert
  logs unless a log entry is itself an explicit operational contract, and remove temporary test
  output used during diagnosis.
- Prefer one strong boundary assertion over overlapping tests at multiple layers. Additional cases
  must protect a distinct failure mode, permission boundary, invariant, or regression.

## Failure Integrity

Treat a test that accurately expresses intended application behavior as the contract.

When it fails:

1. Re-read the requirement and reproduce the failure with the narrowest command.
2. Determine whether the cause is an application defect, an invalid test setup/assertion, an
   explicitly changed requirement, or an environment problem.
3. If the test expresses intended behavior, do not change its expected value, remove or dilute
   assertions, add a skip, over-stub the subject, or otherwise adjust the test merely to make it
   pass. Fix the application code when implementation is in scope.
4. Change the test only when there is concrete evidence that the test itself is wrong or the
   requested behavior changed. Explain that evidence.
5. If the user requested tests only and the correct regression test exposes an application bug,
   leave the meaningful failing test intact and report the failure; do not silently modify
   production code or weaken the test.

## Validation

Run commands from the repository root, narrowing first:

```sh
bin/rails test test/path/to/file_test.rb
bin/rails test test/path/to/file_test.rb:LINE
bin/rails test test/models
<project linter> test/path/to/file_test.rb
```

Use `bin/rails test` when the change has broad impact. Do not run `bin/rails test:system`; UI
verification is a separate browser workflow. Use the project's full validation command (for example `bin/ci`) for broad or release-ready validation.
Report exact commands, failures, and anything left unverified.

## Do Not

- Do not create system, browser, ViewComponent, view, rendering, DOM, or presentation tests.
- Do not make exceptions for an explicit UI-test request without first changing this repository
  policy; explain the conflict instead.
- Do not add an automated test solely because a view, component template, or stylesheet changed.
- Do not assert private methods, incidental SQL shape, callback order, or other implementation
  details when public behavior is observable.
- Do not add redundant tests solely to raise coverage.
- Do not modify unrelated tests or user-owned working-tree changes.
- Do not make a correct intended-behavior test less strict to obtain a green run.
- Do not add route-recognition tests; controller tests already prove routes work.
