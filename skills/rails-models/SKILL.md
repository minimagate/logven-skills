---
name: rails-models
description: Use when adding or changing Logven Active Record models, domain objects, state transitions, associations, validations or callbacks. Hands off schema to rails-migrations, permissions to rails-authorization and file placement to rails-structure.
---

# Rails Models

Shape Logven models so each rule has one owner, the database backs it, and callers can trust it. Follow `../principles/SKILL.md`.

## Order inside a model

- Declare in this order: concerns (`Discard::Model`, `Meterable`), constants, `default_scope`, associations, `enum`, `normalizes` and validations, callbacks, nested attributes and broadcasts, class methods, public instance methods, then `private`.
- Choose `dependent:` from real ownership. Do not default to `:destroy`.
- Declare string statuses with `enum :status, STATUSES.keys.index_with(&:itself)`, keeping `STATUSES` on the model.
- Add scopes rarely. Prefer a class method.

## Domain behavior lives on the owner

- Put state predicates and derived data on the model, such as `Workers::Workflow#active?`, not in controller locals or template logic.
- Navigate with `has_many :through` instead of hand-written lookups.
- Model a transition as a `predicate?` guard plus `verb_now!` and `verb_later!` methods, such as `Workflow#build_now!` and `Workflow#build_later!`.
- Keep the job that runs `verb_later!` to a one-line delegator.
- Do not background work the caller must see synchronously.
- Validate a model's own configuration at the boundary. Services and callers do not re-validate.
- Keep permission rules in policies, never in model validations.

## Data modelling

- Use real foreign keys. Store ids and expose names at the interface, translating in the accessor.
- Drop columns that duplicate an existing concept, such as `created_by` when the creator is the owner role.
- Store structured data as rows and associations, not JSON blobs or markdown parsed by heading.
- Soft-delete domain entities with Discard. Hard delete only to purge data.
- Check `dependent: :destroy` chains for loss of history before adding them.
- Back uniqueness validations with a unique index and required ownership with a foreign key (see `rails-migrations`).

## Plain Ruby domain objects

- Take collaborators in `initialize`, expose instance methods, and do not know your callers.
- A wrapper returns what the wrapped thing returns.
- Model an early stop as a normal outcome, not as status symbols every caller must `case` on.
- Do not convert exceptions into return values.
- The Shapes type system never raises. It returns errors. Representations must be unambiguous, and validators check real formats.

## Callbacks and broadcasts

- Use callbacks only for local bookkeeping that must run on every save.
- Put external effects in `after_commit`, and make them idempotent.
- Use `broadcasts_refreshes_to` only for records updated in the background, such as runs and builds, not interactive cards.
- Rescue narrowly. In rescue paths, write with `update_without_validation` so the failure cannot fail again.

## Reuse

- Route metering through `Meterable`.
- Put id helpers such as `turbo_id` on `ApplicationRecord`.
- Do not add a parallel mechanism beside these.

## Verify

- `bin/rails test test/models/<path>`
- `bin/standardrb`
- `bin/rails zeitwerk:check`
