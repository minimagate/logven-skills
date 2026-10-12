---
name: rails-tests
description: Plan, write, repair, or review tests for any Rails code change, including questions about coverage or regressions and deciding what belongs in Minitest. Enforce minimal logic and HTTP-contract tests; never add UI, DOM, rendered-markup, ViewComponent, system, or browser tests.
---

# Rails Tests

Write the smallest maintainable Minitest coverage that proves requested application behavior. Generated tests use the fewest lines that prove the contract; add no setup, helpers, assertions, cases or abstractions beyond that.

Test logic and non-visual application contracts only. Never test presentation or browser behavior, even when the request concerns UI code; verify UI in the browser (see `../rails-design/SKILL.md`).

Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs, it wins.

## Workflow

1. Establish the intended behavior from the request, application code and existing tests. Read `test/test_helper.rb`, the nearest related tests and relevant helpers first.
2. Run the narrow existing test file first when practical. Distinguish a pre-existing failure from one the change introduced.
3. Decide whether a non-visual behavioral contract exists. Purely visual, markup-only, CSS and component-composition changes need no automated test. Otherwise choose the narrowest layer:
   - Model, plain domain object or policy: inherit `ActiveSupport::TestCase`, under `test/models/` or `test/policies/`. Every policy has a test that proves the meaningful permission matrix and policy-scope membership, including denial and isolation boundaries where they differ by role or ownership.
   - Controller or HTTP contract: inherit `ActionDispatch::IntegrationTest`, under `test/controllers/`. Assert authentication, authorization, status or redirect, persistence, side effects, and response format where it is an API contract. Never assert HTML bodies, rendered text, selectors, CSS classes, DOM structure, templates, partials or components.
   - Mailer or job: use the matching Rails non-system test API and location. Assert delegation and resulting application state, not Active Job internals.
   - External provider or tool: isolate the network boundary and prove the request/response contract. Never call a live provider.
   - No `ApplicationSystemTestCase`, `ViewComponent::TestCase`, view, browser or other render-based tests. If presentation code holds important business rules, move them to a non-presentation object when that is in scope, and test that object's public logic.
4. Arrange only the records and inputs the scenario requires, perform one meaningful action, and assert observable outcomes in the shortest clear form. Cover the requested happy path and the material failure or authorization boundary without building a combinatorial suite.
5. Run the changed test file, then the smallest relevant directory or broader suite the change warrants. Run the project's linter (for example `bin/standardrb` or `bin/rubocop`) on changed Ruby test files.

## Conventions

- Use Minitest's `test "behavior" do` style and `require "test_helper"`. Mirror source namespaces and paths in `test/`.
- One test file per class, mirroring the source path (`test/models/billing/invoice_test.rb` for `app/models/billing/invoice.rb`). An extracted plain Ruby object gets its own test in the same change. A deleted feature's tests are deleted with it.
- Name test classes after their unit (`InvoicePolicyTest`, not a generic name). Reference app classes with a leading `::` inside nested test modules.
- Records: fixtures by default in a fresh Rails app; builders or factories only if the project skill names them. Keep scenario-specific values in the test. Authenticated request tests use the application's existing authentication helper.
- Every controller gets at least one request test per page and one per action branch (valid and invalid), even if it only does `get path; assert_response :ok`. That test is what catches a missing template.
- Stub external interactions (HTTP, mail delivery, payment or LLM providers) with Minitest stubs or WebMock unless the project skill names a stubbing helper. Preserve any contract that rejects missing or unused stubbed responses. Stub only true boundaries or nondeterminism (external services, time, randomness), never the behavior under test.
- Assert mail and jobs through `ActionMailer::TestHelper` and `ActiveJob::TestHelper` (enqueued, delivered, arguments), and use `assert_enqueued_with` or `perform_enqueued_jobs` for asynchronous boundaries. Do not assert rendered bodies or PDF contents beyond a contract the model owns.
- Prefer precise assertions (`assert_difference`, `assert_no_difference`, `assert_changes`, `assert_raises`, `assert_predicate`, exact persisted values, policy scope results). Reload records before asserting persisted state. Prefer explicit per-case assertions over data-driven graders.
- Test claim, resume and idempotency behavior when concurrent or duplicate work could create duplicate children or repeat side effects.
- Keep tests isolated and order-independent, since the suite runs in parallel. Do not depend on fixed database IDs, wall-clock races, global ordering, records from another test, or shared mutable registries without cleanup.

## Keep test code hygienic

- Use the project's existing setup helper and the direct public API. No factory DSL, shared context, test harness, custom assertion or helper abstraction unless repeated setup becomes materially shorter and clearer.
- Keep every test linear: arrange, perform one action, assert the contract. No branching, loops, metaprogrammed cases, deep helper chains, or setup shared by unrelated scenarios.
- Assert public behavior, not private methods, incidental SQL shape, callback order or other implementation details.
- Prefer one strong boundary assertion over overlapping tests at multiple layers. Each additional case must protect a distinct failure mode, permission boundary, invariant or regression. Do not add redundant tests to raise coverage.
- Never add production logging or instrumentation merely to make a test observable. Do not assert logs unless a log entry is an explicit operational contract, and remove temporary diagnostic output.

## Failure Integrity

Treat a test that accurately expresses intended application behavior as the contract. When it fails:

1. Re-read the requirement and reproduce the failure with the narrowest command.
2. Determine the cause: an application defect, an invalid test setup or assertion, an explicitly changed requirement, or an environment problem.
3. If the test expresses intended behavior, do not change its expected value, remove or dilute assertions, add a skip, over-stub the subject, or otherwise adjust it to pass. Fix the application code when implementation is in scope.
4. Change the test only with concrete evidence that it is wrong or that the requested behavior changed, and explain that evidence.
5. If the user requested tests only and a correct regression test exposes an application bug, leave the meaningful failing test intact and report the failure. Do not silently modify production code or weaken the test.

## Validation

Run commands from the repository root, narrowing first:

```sh
bin/rails test test/path/to/file_test.rb
bin/rails test test/path/to/file_test.rb:LINE
bin/rails test test/models
<project linter> test/path/to/file_test.rb
```

Use `bin/rails test` when the change has broad impact, and the project's full validation command (for example `bin/ci`) for broad or release-ready validation. Do not run `bin/rails test:system`. Report exact commands, failures and anything left unverified.

## Do Not

- Do not make exceptions for an explicit UI-test request without first changing this repository policy; explain the conflict instead.
- Do not modify unrelated tests or user-owned working-tree changes.
- Do not add route-recognition tests; controller tests already prove routes work.
