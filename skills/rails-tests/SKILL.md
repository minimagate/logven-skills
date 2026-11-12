---
name: rails-tests
description: Choose verification for behavior changes, bug fixes, interface-only work and reviews; write minimal Rails domain, policy and HTTP-contract tests. Own the no UI/DOM test policy across stacks.
---

# Rails tests

Load before choosing checks, even when no test file will change. The presentation-testing boundary applies in any stack; Rails-specific commands and helpers apply only to Rails.

## Hard boundary: no UI or DOM tests

Never add or expand tests for presentation or browser behavior, regardless of filename or test framework. Forbidden: `assert_select`, `css_select`, Nokogiri/DOM parsing, HTML or rendered-text assertions, CSS classes, element attributes, templates/partials, component rendering, visual snapshots, screenshots as automated assertions, system/Capybara/Playwright tests. This also applies inside request, helper, mailer and model tests; renaming the test does not change the rule.

A request test may assert status, redirects, authorization, persisted state, side effects and a nonvisual API payload/media type. It must not inspect HTML or Turbo Stream markup. UI-only changes need browser inspection and an asset build, not an automated test. Never run `bin/rails test:system`. Existing UI tests are not permission to copy them; replace touched presentation coverage with a real logic contract only when in scope. A later explicit user instruction can change this policy; ordinary UI work cannot.

## Minimal meaningful coverage

### Choose the contract

Read the nearest tests and `test_helper` first. Use Minitest, existing authentication/setup helpers and the project's fixtures/builders. Mirror source namespaces and paths.

Choose the narrowest public boundary: model/domain invariants, policy permissions and tenant isolation, nonvisual HTTP behavior, jobs/mail effects or external API contracts. Do not test framework mechanics or duplicate one contract across layers.

Reproduce a bug with the smallest meaningful nonvisual regression case, then fix its cause and inspect shared callers. Do not add a test harness or duplicate cases where one direct assertion proves the contract.

Cover distinct changed behavior, material denial/failure paths and relevant retry/idempotency/concurrency risks. No automatic test-per-file, getter, page or extracted class; every case must protect a real failure.

### Keep evidence direct

Keep arrange/action/assert linear and small; straightforward setup repetition is fine. Assert exact observable outcomes; reload persisted state. Avoid helpers, factories and combinatorial cases that obscure behavior. Use public setup APIs, never private instance-variable manipulation.

Stub external providers and nondeterminism only; never the subject's own logic. Do not call live providers. Use Rails mail/job helpers for enqueues, deliveries and arguments, not rendered bodies.

Scenario/eval cases must verify the known business result, not merely that execution does not crash. Keep setup, inputs and expected outcome inspectable together.

Keep tests order-independent and safe under parallel execution. No fixed IDs, shared mutable state or wall-clock races.

## Failure integrity and verification

Reproduce narrowly and identify application, test, requirement or environment defects. Fix application code when the test correctly expresses the requested behavior. Never weaken assertions, skip tests or over-stub to manufacture a pass. Change expectations only with evidence that the test or requirement changed. For tests-only work exposing an application bug, report it without silently expanding scope.

Run changed tests and the project linter, then broader checks proportionate to impact. Release work follows [ship](../ship/SKILL.md). Report exact results and verification limits.
