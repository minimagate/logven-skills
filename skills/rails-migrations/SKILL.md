---
name: rails-migrations
description: Create or review Rails schema changes, data rollout/backfills, indexes, foreign keys, defaults and rollback compatibility.
---

# Rails Migrations

Apply the [shared principles](../how-we-work/SKILL.md#principles). Structural migrations define durable data invariants; explicit application flows choose product defaults.

## Separate structure and data

Keep schema changes separate from data changes. No row loops, temporary application models, SQL updates or backfills inside structural migrations. Plan a separate reviewed data step when existing rows need values.

Before adding non-null or identity columns, account for existing records. A project with no production data may declare that fact; do not assume it. Never reset a database without authorization.

## Define durable constraints

Prefer a clear ownership/constraint change over schema that requires permanent application reconciliation. Keep the migration minimal without dropping rollout, data-safety or reversibility requirements.

Define intended nullability, timestamps, defaults, references and foreign keys. Unique indexes protect uniqueness under concurrency. Name composite/partial indexes explicitly. Keep statuses as strings backed by model constants; no database enums.

Match namespaced table prefixes to their owning modules; prefix changes require rename migrations. Name each migration for one coherent structural action.

## Preserve rollback and rollout

Use the project's current migration version and reversible `change`; use explicit `up`/`down` when needed. Include dropped-table structure and removed-column types so rollback can restore structure; restoring dropped data needs its own plan.

Change `db/schema.rb` only by running migrations. Inspect the resulting diff for unrelated changes. Edit branch-local unshared migrations in place; add migrations for shared history.

For deployed data, plan compatible rollout and expand/contract where coexistence is necessary; do not remove an old column before its consumers and required data are handled.

## Verification

Run `bin/rails db:migrate`, `bin/rails db:test:prepare` and relevant [model tests](../rails-tests/SKILL.md). Check rollback/remigration in a safe local database when reversibility is uncertain. Confirm intended constraints and indexes in the generated schema. Domain behavior belongs in [models](../rails-models/SKILL.md).
