---
name: rails-migrations
description: Use when writing or reviewing a Rails schema migration, index, foreign key, default, table prefix or db/schema.rb change. Covers schema-only reversible migrations. Hands off to rails-models for behavior, validations and associations.
---

# Rails Migrations

Write schema-only, reversible migrations that keep `db/schema.rb` an accurate record of the database, following [principles](../principles/SKILL.md).

## Schema only

- Change structure only. `AGENTS.md` says: "Keep development migrations schema-only."
- No `UPDATE` statements, row loops, temporary models, data backfills, dual writes or phased nullability.
- Before adding a non-null or identity column to an existing table, state in the plan that existing development rows will be nil.
- Resetting a development database is destructive. Get the user's approval first.

## Shape

- Subclass `ActiveRecord::Migration[8.1]` and write a reversible `change`.
- Use `up`/`down` only when the operation cannot be expressed reversibly.
- Write drops as `drop_table :x do |t| ... end` listing the columns, and give `remove_column` its type so it reverses.
- Create tables with their final columns, nullability, defaults, timestamps, `null: false` references and foreign keys.
- Name composite and partial indexes explicitly.
- Keep durable invariants in the database: foreign keys for ownership, unique indexes for uniqueness. A uniqueness validation alone is not concurrency-safe.
- Store status columns as strings backed by a model constant. Do not use database enums.
- Prefix namespaced tables with their module (`workers_`, `sheets_`, `assistant_`). Changing a prefix is a rename migration.
- Name migrations for the action (`AddSettingsToUsers`, `CreateMeters`). Keep one coherent schema change per migration.

## History and schema.rb

- Change `db/schema.rb` only by running a migration, never by hand.
- Every `schema.rb` change has a migration. A removed column gets its own removal migration.
- Inspect the schema diff: it should show only the intended structure and version.
- Edit an unshared migration on the current branch in place. Add a new migration for anything already in shared history.
- Renames and drops are acceptable before production. When an old and a new column must coexist, use expand/contract within the same PR.

## Verify

- Run `bin/rails db:migrate`.
- When reversibility is not obvious, run `bin/rails db:rollback` and then `bin/rails db:migrate` again.
- Run `bin/rails db:test:prepare`.
- Run the relevant model tests.
- Confirm the new constraints and indexes appear in `db/schema.rb`.
