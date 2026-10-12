---
name: rails-migrations
description: Use when writing or reviewing a Rails schema migration, index, foreign key, default, table prefix or db/schema.rb change. Covers structure-only reversible migrations. Hands off to rails-models for behavior, validations and associations.
---

# Rails Migrations

Write structure-only, reversible migrations that keep `db/schema.rb` an accurate record of the database, following the [Principles](../how-we-work/SKILL.md) section.

Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs, it wins.

## Structure only

- Data changes are separate, reviewable steps (a data migration or task), called out in the plan. A project with no production data may declare a schema-only stance in its project skill.
- No `UPDATE` statements, row loops, temporary models, backfills, dual writes or phased nullability in a structural migration.
- Before adding a non-null or identity column to an existing table, state in the plan how existing rows get a value (a separate data step) or that they will be nil.
- Resetting a development database is destructive. Get the user's approval first.

## Shape

- Subclass `ActiveRecord::Migration[<current Rails version>]` with a reversible `change`. Use `up`/`down` only when reversal is impossible.
- Write drops as `drop_table :x do |t| ... end` listing the columns. Give `remove_column` its type so it reverses.
- Create tables with final columns, nullability, defaults, timestamps, `null: false` references and foreign keys.
- Name composite and partial indexes explicitly.
- Keep durable invariants in the database: foreign keys for ownership, unique indexes for uniqueness. A uniqueness validation alone is not concurrency-safe.
- Status columns are strings backed by a model constant. No database enums.
- Prefix namespaced tables with their module when the project namespaces its tables. Changing a prefix is a rename migration.
- Name migrations for the action (`AddSettingsToUsers`, `CreateInvoices`). One coherent schema change per migration.

## History and schema.rb

- Change `db/schema.rb` only by running a migration, never by hand. Every change has a migration; a removed column gets its own removal migration.
- Inspect the schema diff: it should show only the intended structure and version.
- Edit an unshared migration on the current branch in place. Add a new migration for anything in shared history.
- Renames and drops are fine before production data exists. When old and new columns must coexist, use expand/contract in the same PR.

## Verify

- Run `bin/rails db:migrate`.
- When reversibility is not obvious, run `bin/rails db:rollback` and then `bin/rails db:migrate` again.
- Run `bin/rails db:test:prepare`.
- Run the relevant model tests.
- Confirm the new constraints and indexes appear in `db/schema.rb`.
