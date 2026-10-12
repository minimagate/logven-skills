---
name: rails-models
description: Use when adding or changing Active Record models, domain objects, state transitions, associations, validations or callbacks in this app. Hands off schema to rails-migrations, permissions to rails-authorization and file placement to rails-structure.
---

# Rails Models

Shape the app's models so each rule has one owner, the database backs it, and callers can trust it. Follow `../principles/SKILL.md`.

Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs from this skill, it wins.

## Order inside a model

- Declare in this order: concerns (shared capabilities), constants, `default_scope`, associations, `enum`, `normalizes` and validations, callbacks, nested attributes and broadcasts, class methods, public instance methods, then `private`.
- Choose `dependent:` from real ownership. Do not default to `:destroy`.
- Declare string statuses with `enum :status, STATUSES.keys.index_with(&:itself)`, keeping `STATUSES` on the model.
- Add scopes rarely. Prefer a class method.

## Domain behavior lives on the owner

- Put state predicates and derived data on the model, such as `Order#fulfillable?`, not in controller locals or template logic.
- Navigate with `has_many :through` instead of hand-written lookups.
- Model a transition as a `predicate?` guard plus `verb_now!` and `verb_later!` methods, such as `order.ship_now!` and `order.ship_later!`.
- Keep the job that runs `verb_later!` to a one-line delegator.
- Do not background work the caller must see synchronously.
- Validate a model's own configuration at the boundary. Domain objects and callers do not re-validate.
- Keep permission rules in policies, never in model validations.

## Data modelling

- Use real foreign keys. Store ids and expose names at the interface, translating in the accessor.
- Drop columns that duplicate an existing concept, such as `created_by` when the creator is the owner role.
- Store structured data as rows and associations, not JSON blobs or markdown parsed by heading.
- Soft delete only where the project skill says so (it implies a library or column convention nobody should add silently); otherwise delete deliberately and check `dependent:` chains for lost history.
- Back uniqueness validations with a unique index and required ownership with a foreign key (see `rails-migrations`).

## Plain Ruby domain objects

- Take collaborators in `initialize`, expose instance methods, and do not know your callers.
- A wrapper returns what the wrapped thing returns.
- Model an early stop as a normal outcome, not as status symbols every caller must `case` on.
- Do not convert exceptions into return values.
- Make representations unambiguous, and have validators check real formats.

## Mail, files and background work

- Send mail with `deliver_later` after the state change commits (`after_commit` or a `verb_later!` method), never inside the request when the user must see the result synchronously.
- The domain object that renders a document (for example an invoice PDF) is a plain object under `app/models` named for its role, not a service.
- Attach generated files with Active Storage.
- Mark state (for example `sent_at`) in the same transaction as the enqueue decision, and make the job idempotent.

## Callbacks and broadcasts

- Use callbacks only for local bookkeeping that must run on every save.
- Put external effects in `after_commit`, and make them idempotent.
- Use `broadcasts_refreshes_to` only for records updated in the background (for example imports or sync runs), not interactive cards.
- Rescue narrowly. In rescue paths, write without validations so the failure cannot fail again.

## Reuse

- Route a shared capability (such as search) through its existing concern.
- Put id helpers on `ApplicationRecord`.
- Do not add a parallel mechanism beside these.

## Verify

- `bin/rails test test/models/<path>`
- The project's linter (for example `bin/standardrb` or `bin/rubocop`)
- `bin/rails zeitwerk:check`
