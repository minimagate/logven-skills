---
name: migrations
description: "Create or revise Logven PostgreSQL schema migrations, indexes, foreign keys, defaults, or constraints. Use for database structure changes. This application is development-only: keep migrations schema-only and never add data backfills or staged rollout choreography."
---

# Migrations

Logven is currently an on-premises, development-only application with no production dataset to preserve. Optimize migrations for a clean, correct schema—not for rolling upgrades across live versions.

## Keep every migration simple

- Use `ActiveRecord::Migration[8.1]` and prefer a reversible `change` method with Rails' migration DSL.
- Create tables with the final intended columns, nullability, defaults, timestamps, references, foreign keys, and indexes.
- Add or remove columns, references, indexes, and constraints directly. Prefer explicit names for composite or partial indexes when the generated name would be unclear.
- Put durable invariants in PostgreSQL: foreign keys for ownership, unique indexes for uniqueness, and partial indexes for conditional uniqueness such as one project owner.
- Match existing storage choices: PostgreSQL, `jsonb` for structured persisted objects that benefit from PostgreSQL semantics, and readable string statuses.

## Never backfill development data

Do not write `UPDATE`, `DELETE`, row loops, temporary models, data migrations, dual writes, compatibility columns, phased nullability changes, or expand/contract rollout steps to preserve local records. Do not copy historical backfill-heavy migrations as precedent.

If a schema change conflicts with disposable development data, make the target schema correct and reset/reseed the affected local database. A database reset is destructive, so obtain the user's approval immediately before running it.

Do not add a complicated `up`/`down` migration merely to transform values that can be recreated. Use `up`/`down` only when the schema operation itself cannot be represented reversibly with `change`.

## Manage migration history deliberately

Create a new migration for changes already shared in repository history. An unshared migration on the current feature branch may be corrected in place when doing so keeps the history simpler. Never rewrite a migration known to have been applied by someone else without explicit direction.

Do not edit `db/schema.rb` by hand. Run the migration so Rails updates it, then inspect the schema diff for only the intended version and structure changes.

## Verify

Run `bin/rails db:migrate`, the relevant model tests, and a rollback/reapply check when reversibility is not obvious. For a brand-new or reset database path, use `bin/rails db:test:prepare` or the repository setup command and confirm constraints appear in `db/schema.rb`.
