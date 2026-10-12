---
name: rails-structure
description: Use when deciding where Rails code belongs in this app, how to name it, which namespace it takes, when to extract it, or how Zeitwerk loads it. Hands off to rails-models for records and validations, rails-controllers for routes and actions, and rails-frontend for views and JS.
---

# Rails Structure

Place and name the app's Rails code so each piece has one clear owner. Follow [principles](../principles/SKILL.md).

Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs from this skill, it wins.

## Layout

- Avoid a services layer. Put domain objects under `app/models/`, in namespaces that mix records and plain Ruby objects (`Billing::Invoice`, `Billing::Calculator`).
- For AR-backed namespaces, add a small module file that sets `self.table_name_prefix`, and keep the prefix consistent with the namespace.
- Mirror the namespace in controllers (`Orders::...`), policies, helpers and tests.
- Put generic infrastructure in `lib/`. Put app-specific glue next to its owner (`app/models/orders/fulfillment/`).
- Keep non-Ruby assets that one class uses (prompts, templates) next to that class.
- Define constants on the owning class (`Order::STATUSES`), never in a global constants file.

## Naming

- Name domain objects by role noun: `Fulfiller`, `Fulfillment::Plan`, `Importer::Host`.
- Do not repeat the namespace in the name: `Orders::Shipment`, not `Orders::OrderShipment`.
- Use specific verb+noun action names: `list_records`, not `list`.
- Do not reuse a word that already means something else, such as `Base` or `action`.
- When a new concept needs room, rename and clean up first, as its own change.

## One owner, one file

- Keep one class per file.
- When a model grows, or holds a nested class or helper logic, extract a plain Ruby object into its own file in `app/models`, with its own test. The controller then exposes one object instead of many ivars.
- Build objects with their collaborators (`new(user:, order:)`) and use instance methods, not class methods that take a config hash.
- Use a concern only for one cohesive capability shared by several models, usually with a class macro (a shared concern such as `Trackable`).
- Inline any helper, module, base class or CSS class with exactly one caller. Small duplication beats a clever helper.

## Reuse before inventing

- Use the existing interface first: the project's DSLs, shared concerns, type/cast helpers, id helper, policies and constants. Do not add a parallel registry, caster or escape hatch.
- Prefer explicit constants and arguments over thread-locals, `prepend` monkeypatches, YAML lookups keyed by a tag, or env-var switches.
- Use `ENV.fetch` for required config, with no provider-specific precedence.
- Prefer CLI options over env vars for tooling.

## Keeping the tree clean

- Delete the old path, leftover files and dead code in the same change that replaces it. No aliases or compat shims.
- Do not write comments that narrate or defend ordinary code. Comment only genuine hacks.
- Keep pure file moves in their own change, separate from edits to lines.
- Keep user-facing strings consistent with the project's choice (inline or I18n). Do not introduce I18n piecemeal.

## Verify

- Run `bin/rails zeitwerk:check`.
- Run the project's linter (for example `bin/standardrb` or `bin/rubocop`).
- Run `bin/rails test <path>` for each changed file's test.
