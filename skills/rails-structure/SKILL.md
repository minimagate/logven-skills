---
name: rails-structure
description: Place, name, namespace or extract Rails code; assess ownership, boundaries and Zeitwerk loading.
---

# Rails Structure

Apply the [shared principles](../how-we-work/SKILL.md#principles) and matching project conventions.

## Place and name

Domain records and plain Ruby objects belong in `app/models/<domain>/`; no services layer. Generic infrastructure belongs in `lib/`, independent of application models and product vocabulary. Keep templates, SQL and other supporting assets beside their owner.

Mirror namespaces in controllers, policies, helpers and tests. Namespaced Active Record modules set `self.table_name_prefix`. One class per file; constants live on their owning class. Mailers and jobs use Rails directories.

Name objects for their domain role, without repeating the namespace. Name operations specifically. Make necessary conceptual renames before building on them; keep pure moves separate from edits.

## Define boundaries

Foundations expose small explicit contracts. Higher-level owners compose them and choose product policy. A reusable mechanism should integrate locally, without leaking its transport or workflow into unrelated consumers. Avoid template→helper configuration hashes→component translation chains, caller detection, thread-locals, monkeypatches and speculative registries.

Prefer an existing owner or direct method before a new file/layer; minimize concepts and clear lines, not just file length. Remove only superseded paths and leftovers in scope.

Extract an object for a coherent responsibility or meaningful boundary, even with one caller. Inline forwarding wrappers that add neither. Caller count alone never decides architecture; helpers should not delegate ordinary formatting through a dedicated class just to return to a helper.

Share a resource interface when identity and lifecycle genuinely match; keep independent options as attributes. Separate flows that differ in responsibility, such as editing versus read-only reporting. Use polymorphism for real types, not a mandatory STI/factory architecture.

Concerns represent cohesive capabilities shared by models. Reuse existing casting, validation, identifiers and policy mechanisms before adding alternatives; tolerate small duplication when sharing would couple unrelated domains.

## Respect existing contracts

Read required configuration with `ENV.fetch` or credentials. Keep user-facing strings consistent with the project's existing localization approach.

Preserve framework authentication/bootstrap defaults unless the task provides a concrete reason to change them. Before deleting apparently unused code, check framework, dynamic and public callers and documented intent; a text search alone is not proof. Remove superseded paths in scope. Explain non-obvious constraints, not ordinary code.

## Verification

For behavior, routes and presentation, use [models](../rails-models/SKILL.md), [controllers](../rails-controllers/SKILL.md) and [frontend](../rails-frontend/SKILL.md). Verify changed behavior, the project linter and `bin/rails zeitwerk:check`.
