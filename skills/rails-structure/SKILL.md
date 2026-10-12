---
name: rails-structure
description: Use when deciding where Rails code belongs in Logven, how to name it, which namespace it takes, when to extract it, or how Zeitwerk loads it. Hands off to rails-models for records and validations, rails-controllers for routes and actions, and rails-frontend for views and JS.
---

# Rails Structure

Place and name Logven's Rails code so each piece has one clear owner. Follow [principles](../principles/SKILL.md).

## Layout

- Put domain namespaces under `app/models/`, mixing records and plain Ruby objects: `Workers::`, `Sheets::`, `Assistant::`, `Shapes::`, `Chat::`, `Credentials::`, `Apis::`.
- Do not create `app/services` or `*Service` classes.
- For AR-backed namespaces, add a 3-line module file that sets `self.table_name_prefix` (`app/models/workers.rb` gives `workers_`, `sheets_`, `assistant_`).
- Mirror the namespace in controllers (`Projects::Workers::...`), policies, helpers and tests.
- Put generic infrastructure in `lib/` (`lib/runtime`). Put app-specific glue next to its owner (`app/models/workers/runner/`).
- Keep prompt `.md` files next to the Ruby that uses them.
- Keep evals in `evals/`, outside CI.
- Define constants on the owning class (`Workflow::STATUSES`), never in a global constants file.

## Naming

- Name domain objects by role noun: `Revisioner`, `Builder::Plan`, `Runner::Host`.
- Do not repeat the namespace in the name: `Workers::Run`, not `Workers::WorkflowRun`.
- Use specific verb+noun action names: `list_records`, not `list`.
- Do not reuse a word that already means something else, such as `Base` or `action`.
- When a new concept needs room, rename and clean up first, as its own change.

## One owner, one file

- Keep one class per file.
- When a model grows, or holds a nested class or helper logic, extract a plain Ruby object into its own file in `app/models`, with its own test. The controller then exposes one object instead of many ivars.
- Build objects with their collaborators (`new(user:, sheet:)`) and use instance methods, not class methods that take a config hash.
- Use a concern only for one cohesive capability shared by several models, usually with a class macro (`Meterable`, `include_meters_from`).
- Inline any helper, module, base class or CSS class with exactly one caller. Small duplication beats a clever helper.

## Reuse before inventing

- Use the existing interface first: the tools DSL, `Meterable`, Shapes `to_params` and cast, `turbo_id`, policies, chat profile constants. Do not add a parallel registry, caster or escape hatch.
- Prefer explicit constants and arguments over thread-locals, `prepend` monkeypatches, YAML lookups keyed by a tag, or env-var switches.
- Use `ENV.fetch` for required config, with no provider-specific precedence.
- Prefer CLI options over env vars for tooling.

## Keeping the tree clean

- Delete the old path, leftover files and dead code in the same change that replaces it. No aliases or compat shims.
- Do not write comments that narrate or defend ordinary code. Comment only genuine hacks.
- Keep pure file moves in their own change, separate from edits to lines.
- Keep user-facing strings inline in English. I18n is unused, so do not introduce it piecemeal.

## Verify

- Run `bin/rails zeitwerk:check`.
- Run `bin/standardrb`.
- Run `bin/rails test <path>` for each changed file's test.
