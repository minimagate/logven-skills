---
name: generate-tests
description: Plan, write, repair, or review tests for any Logven Rails code change. Use whenever a task changes Rails application code, asks about tests, coverage, or regressions, or requires deciding what belongs in Minitest. Enforce minimal logic and HTTP-contract tests; never add UI, DOM, rendered-markup, ViewComponent, system, or browser tests.
---

# Generate Tests

Write the smallest maintainable Minitest coverage that proves requested application behavior.
Test logic and non-visual application contracts only. Never test presentation or browser behavior,
even when the request concerns UI code. Verify UI changes in the browser instead of encoding their
appearance or DOM structure in the test suite.
Protect the test's behavioral contract when diagnosing failures.

## Workflow

1. Establish the intended behavior from the request, application code, and existing tests. Read
   `test/test_helper.rb`, the nearest related tests, and relevant helpers before writing code.
   Consult the official testing links in `docs/links.md` when framework behavior matters.
2. Run the narrow existing test file first when practical. Distinguish a pre-existing failure
   from one introduced by the change.
3. Decide whether the change has a non-visual behavioral contract worth testing. Purely visual,
   markup-only, CSS, and component-composition changes require no automated test. When a logic or
   HTTP contract exists, choose the narrowest layer that proves it:
   - Model, plain domain object, service-like namespace, or policy: inherit
     `ActiveSupport::TestCase` and place the test under the matching `test/models/` or
     `test/policies/` path.
   - Controller or HTTP contract: inherit `ActionDispatch::IntegrationTest` under
     `test/controllers/`. Assert authentication, authorization, status/redirect, persistence,
     side effects, and other request-level functionality.
   - Route, mailer, or job: use the matching Rails non-system test API and repository location.
   - Controller tests must stop at the HTTP/application boundary: authentication, authorization,
     status or redirect, persistence, side effects, and response format where it is an API
     contract. Do not assert HTML response bodies, rendered text, selectors, CSS classes, DOM
     structure, templates, partials, or components.
   - Do not create `ApplicationSystemTestCase`, `ViewComponent::TestCase`, view, browser, or other
     render-based tests. If presentation code contains important business rules, move those rules
     to a non-presentation object when that is in scope and test the public logic there.
4. Arrange only the records and inputs required for the scenario, perform one meaningful action,
   and assert observable outcomes. Cover the requested happy path and material failure or
   authorization boundary without building a combinatorial suite.
5. Run the changed test file, then the smallest relevant directory or broader suite warranted by
   the change. Run Standard on changed Ruby test files.

## Repository Conventions

- Use Minitest's `test "behavior" do` style and `require "test_helper"`.
- Mirror source namespaces and paths in `test/`.
- Create records with helpers from `test/test_helpers/attributes/` where they fit; keep scenario-
  specific values in the test when that makes the behavior clearer. Do not introduce fixtures.
- Use `sign_in_as` for authenticated request tests.
- Use `with_llm([...])` for deterministic LLM interactions. It intentionally fails on missing or
  unused responses; do not weaken that contract.
- Prefer precise assertions such as `assert_difference`, `assert_no_difference`,
  `assert_changes`, `assert_raises`, `assert_predicate`, exact persisted values, and policy scope
  results. Assert public effects rather than private implementation details.
- Stub only true boundaries or nondeterminism, such as external services, time, or randomness.
  Do not stub the behavior under test.
- Keep tests isolated and order-independent because the suite runs in parallel.

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
bin/standardrb test/path/to/file_test.rb
```

Use `bin/rails test` when the change has broad impact. Do not run `bin/rails test:system`; UI
verification is a separate browser workflow. Report exact commands, failures, and anything left
unverified.

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
