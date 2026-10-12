---
name: rails-structure
description: Use when deciding where Rails code belongs in this app, how to name it, which namespace it takes, when to extract it, or how Zeitwerk loads it. Hands off to rails-models for records and validations, rails-controllers for routes and actions, and rails-frontend for views and JS.
---

# Rails Structure

Place and name Rails code so each piece has one owner, following the [Principles](../how-we-work/SKILL.md) section.

Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs, it wins.

## Layout

- No services layer. Domain objects go under `app/models/` in namespaces that mix records and plain Ruby (`Billing::Invoice`, `Billing::Calculator`).
- With namespaced tables, add a module per AR-backed namespace that sets `self.table_name_prefix`.
- Mirror the namespace in controllers, policies, helpers and tests.
- Generic infrastructure goes in `lib/`. App glue and non-Ruby assets (templates, SQL) sit next to their owner (`app/models/orders/fulfillment/`).
- Mailers go in `app/mailers`. Jobs go in `app/jobs` as one-line delegators (rails-models). Document renderers are plain objects under `app/models/<namespace>/` (`Billing::InvoicePdf`), not services.
- Constants live on the owning class (`Order::STATUSES`), never in a global file.

## Naming

- Name domain objects by role noun (`Fulfiller`, `Fulfillment::Plan`). Do not repeat the namespace (`Orders::Shipment`, not `Orders::OrderShipment`).
- Use specific verb+noun action names (`list_records`, not `list`). Avoid words that already mean something, such as `Base` or `action`.
- When a concept needs room, rename and clean up first, as its own change.

## One owner, one file

- One class per file.
- Extract a growing model's nested class or helper logic into a plain Ruby object in `app/models`, with its own test. The controller then exposes one object, not many ivars.
- Build objects with their collaborators (`new(user:, order:)`), expose instance methods, and do not know your callers. No class methods that take a config hash.
- Use a concern only for one cohesive capability shared by several models, usually with a class macro (such as `Archivable`).
- Inline any helper, module, base class or CSS class with exactly one caller.

## Reuse before inventing

- Use the existing interface first: DSLs, shared concerns, cast helpers, the id helper, policies and constants. Add no parallel registry, caster or escape hatch.
- Prefer explicit constants and arguments over thread-locals, `prepend` monkeypatches, tag-keyed YAML lookups or env-var switches.
- Read config with `ENV.fetch` or credentials; no silent defaults.

## Keeping the tree clean

- Delete the old path, leftovers and dead code in the same change that replaces it. No aliases or shims.
- Comment only genuine hacks; no comments that narrate ordinary code.
- Keep pure file moves in their own change.
- Keep user-facing strings consistent with the project's choice (inline or I18n). Do not introduce I18n piecemeal.

## Verify

- Run `bin/rails zeitwerk:check`.
- Run the project's linter (for example `bin/standardrb` or `bin/rubocop`).
- Run `bin/rails test <path>` for each changed file's test.
