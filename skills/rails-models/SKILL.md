---
name: rails-models
description: Use when adding or changing Active Record models, domain objects, state transitions, associations, validations or callbacks in this app. Hands off schema to rails-migrations, permissions to rails-authorization and file placement to rails-structure.
---

# Rails Models

Shape models so each rule has one owner, the database backs it, and callers can trust it, following the [Principles](../how-we-work/SKILL.md) section.

Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs, it wins.

## Order inside a model

- Declare in this order: concerns, constants, `default_scope`, associations, `enum`, `normalizes` and validations, callbacks, nested attributes and broadcasts, class methods, public instance methods, then `private`.
- Declare statuses with `enum :status, STATUSES.keys.index_with(&:itself)`, keeping `STATUSES` on the model.
- Choose `dependent:` from real ownership. Do not default to `:destroy`.
- Back uniqueness validations with a unique index and required ownership with a foreign key (see rails-migrations).
- Add scopes rarely; prefer a class method.

## Domain behavior lives on the owner

- Put state predicates and derived data on the model (`Order#fulfillable?`), not in controller locals or templates.
- Navigate with `has_many :through`, not hand-written lookups.
- Model a transition as a `predicate?` guard plus `verb_now!` and `verb_later!` (`order.ship_now!`). The job that runs `verb_later!` is a one-line delegator.
- Do not background work the caller must see synchronously.
- Validate a model's own configuration at the boundary; domain objects and callers do not re-validate.
- Permission rules live in policies (rails-authorization), never in validations.

## Data modelling

- Use real foreign keys. Store ids and expose names at the interface, translating in the accessor.
- Drop columns that duplicate a concept, such as `created_by` when the creator is the owner role.
- Store structured data as rows and associations, not JSON blobs or markdown parsed by heading.
- Soft delete only where the project skill says so (it implies a convention nobody should add silently). Otherwise delete deliberately and check `dependent:` chains for lost history.

## Plain Ruby domain objects

- A wrapper returns what the wrapped thing returns.
- Model an early stop as a normal outcome, not as status symbols callers must `case` on.
- Do not convert exceptions into return values.
- Make representations unambiguous, and have validators check real formats.

## Files and background work

- Attach generated files with Active Storage.
- Set state (for example `sent_at`) in the same transaction as the enqueue decision, and make the job idempotent.

## Callbacks and broadcasts

- Use callbacks only for local bookkeeping that must run on every save.
- Put external effects (mail, jobs) in `after_commit` or a `verb_later!` method, after the state change commits. Send mail with `deliver_later`. Keep them idempotent.
- Use `broadcasts_refreshes_to` only for records updated in the background (imports, sync runs), not interactive cards.
- Rescue narrowly. In rescue paths, write without validations so the failure cannot fail again.

## Reuse

- Route shared capabilities (such as search) through their existing concern. Id helpers live on `ApplicationRecord`. No parallel mechanisms (rails-structure).

## Verify

- `bin/rails test test/models/<path>`
- The project's linter (for example `bin/standardrb` or `bin/rubocop`)
- `bin/rails zeitwerk:check`
