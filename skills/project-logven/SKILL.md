---
name: project-logven
description: Use only when working in the Logven repo. Project-specific names, paths, helpers and decisions. Read with the general rails-* skills and principles; it overrides general defaults where they differ.
---

# Project Logven

Logven is a Rails app for project-owned sheets, workers, workflows and workflow runs. This file holds every fact that is true only for Logven.

## How to use

- General rules live in the `rails-*` skills and `principles`. This file holds only what is specific to Logven.
- Where this file and a general skill differ, this file wins.
- Visual specifics (tokens, classes, geometry, status colors) are in [references/design.md](references/design.md).

## Structure and naming

- Domain namespaces under `app/models/` mix records and plain Ruby: `Workers::`, `Sheets::`, `Assistant::`, `Shapes::`, `Chat::`, `Credentials::`, `Apis::`.
- AR-backed namespaces get a 3-line module file setting `self.table_name_prefix` (`app/models/workers.rb`): tables are `workers_`, `sheets_`, `assistant_`.
- Mirror the namespace in controllers (`Projects::Workers::...`), policies, helpers and tests.
- Do not create `app/services` or `*Service` classes.
- Generic infrastructure lives in `lib/runtime` (the isolated runtime that executes workflow code). App glue sits next to its owner (`app/models/workers/runner/`).
- Prompt `.md` files sit next to the Ruby that uses them (`app/models/workers/builder/prompts/`). Prompt edits get their own commits.
- Evals live in `evals/`, outside CI and `bin/rails test`.
- Constants live on the owner: `Workflow::STATUSES`.
- Role-noun names: `Revisioner`, `Builder::Plan`, `Runner::Host`. No namespace repetition: `Workers::Run`, not `Workers::WorkflowRun`.
- Existing interfaces to reuse; never add a parallel registry, caster or escape hatch: the tools DSL, `Meterable` (with `include_meters_from`), Shapes `to_params` and cast, `turbo_id`, policies, chat profile constants.
- Concerns: `Meterable` is the model for a cohesive shared capability with a class macro.
- Keep user-facing strings inline in English. I18n is unused.
- LLM provider config: `OPENROUTER_*`, `OMLX_*`, `SCALEWAY_*` keys in `config/initializers/ruby_llm.rb`; profile via `LOGVEN_LLM_PROVIDER` and `LOGVEN_LLM_EFFORT` in `app/models/chat/profiled.rb`.
- Verify structure with `bin/rails zeitwerk:check`, `bin/standardrb`, `bin/rails test <path>`.

## Models

- `Discard::Model` and `Meterable` are the first concerns in the declaration order.
- Route all metering through `Meterable`.
- `ApplicationRecord` holds `turbo_id` and `details_turbo_id`.
- State predicate example: `Workers::Workflow#active?`.
- Transitions: `Workflow#build_now!` and `Workflow#build_later!`, guarded by a predicate.
- The Shapes type system never raises: it returns errors. Representations are unambiguous and validators check real formats.
- `broadcasts_refreshes_to` is for runs and builds only, never interactive cards.
- In rescue paths write with `update_without_validation`.
- Status columns: `enum :status, STATUSES.keys.index_with(&:itself)` with `STATUSES` on the model.
- Soft delete: `Discard::Model` on `User`, `Project`, `Workers::Workflow` and `Assistant::Chat` (a default scope of kept records). Hard delete only to purge data.

## Controllers and routes

- `Projects::BaseController` sets the project. `Projects::Workers::Workflows::BaseController` sets the workflow.
- `ApplicationController` class macros `navigation`, `section`, `assistant_context` replace ad-hoc matching.
- Load nested records through the parent: `@project.workflows.find`, never `Workflow.find`.
- Each state change is a singular resource with `only: %i[create]`, its own controller and policy: `resource :build`, `:commit`, `:revision`, `:rerun`.
- Parent-owned controllers use `scope module: :projects`.
- Template placement example: `projects/workers/workflows/specs/_form`, not `projects/workers/workflows/_spec_form`.
- Autosave returns `head :no_content`.
- Turbo Frames are not used. No `turbo_frame_request?` forks.
- Keep each controller under 80 lines. Expose one object (`@summary`) instead of many ivars.

## Authorization

- `ApplicationController` runs `verify_authorized`, and `verify_policy_scoped` on `index`. Only sessions, passwords and oauth_callbacks opt out.
- `ApplicationPolicy` denies by default.
- Operation policies via `policy_class:`: `WorkflowBuildPolicy`, `WorkflowCommitPolicy`, `WorkflowSpecPolicy`. They delegate to `WorkflowPolicy#update?` or `ProjectPolicy` and add only the domain predicate, such as `buildable_later?`.
- A workflow is editable only while it is a draft.
- Starting a run spends credits: require `update?`, not `show?`.
- Member lookup: `@project.runs.find(params[:id])`.
- Views disable forms with `policy(workflow).update?`.
- Do not write `policy(run).show?` inside an already-scoped runs list.

## Migrations

- `AGENTS.md`: "Keep development migrations schema-only."
- `ActiveRecord::Migration[8.1]`.
- Table prefixes `workers_`, `sheets_`, `assistant_`. Changing a prefix is a rename migration.
- Status columns are strings backed by a model constant, no DB enums.
- Resetting a development database needs the user's approval.
- Renames and drops are acceptable before production.
- Before adding a non-null or identity column to an existing table, state in the plan that existing development rows will be nil.
- Verify: `bin/rails db:migrate`, `db:rollback` then `db:migrate`, `db:test:prepare`.

## Frontend

- Tools: ERB, ViewComponent, Turbo, Stimulus, Importmap, Tailwind.
- Importmap (`config/importmap.rb`) holds only `sortablejs`, `lexxy` and `@rails/activestorage` beyond the framework. Every new pin needs a stated reason.
- No `package.json` workflow.
- Partial names: `_show` (canonical per-record partial, reused by show pages, streams and collections), `_row` and `_card` (list variants), `_form`, `_new_dialog`.
- Page chrome via `content_for`: `:title`, `:page_title`, `:page_parent`, `:page_header`, `:page_header_actions`, `:body_class`.
- Turbo target ids come only from `turbo_id` / `details_turbo_id`; composite ids append `-details`, `-destroy` or `-editor`. Never hand-write an id or use `dom_id`.
- Partial updates are `turbo_stream.replace` templates named per action (`create`, `update`, `destroy`), rendering the same `_show`/`_form` partials as the full pages.
- Stimulus pairs like `autosave` + `sortable` stay generic.
- Icons: `svg_tag "icons/..."`.
- Tone helpers: `run_status_tone`, `build_status_tone`; `badge_class_for` and `text_class_for` map tone to a class. Unknown values fall back to `:neutral`. Extend the helpers, never branch in templates.
- Run lifecycle display: `RunStatusIconComponent`.
- Build CSS with `bin/rails tailwindcss:build`. Verify at the established desktop size and a narrow viewport.
- Light and dark mode are both supported through tokens (`light-dark(...)` palette, no `dark:` variants); check both. The design reference is [references/design.md](references/design.md).

## Tests

- Builders: `*_attributes(**overrides)` in `test/test_helpers/attributes/`. No fixtures.
- Stub LLM calls with `with_ruby_llm` from `test/test_helpers/ruby_llm_test_helper/helper.rb`, not `with_llm`. Un-stubbed LLM calls raise.
- Example mirrored path: `test/models/workers/builder/plan_test.rb`. Policy tests named like `TablePolicyTest`.
- Dev seed tests prove the idempotent showcase dataset.
- Evals live in `evals/`, assert on final output, stay outside CI.
- Commands: `bin/rails test test/models/workers/workflow_test.rb`, `bin/standardrb`, `bin/ci` (setup, lint, security audits, tests, test-env seed validation). SimpleCov has no minimum threshold.
- Environment: Ruby 3.3.6, Bundler, PostgreSQL. `bin/setup --skip-server`, `bin/dev` (port 3000 plus Tailwind watcher).

## Commits and PRs

- History style: short descriptive subjects such as `Improve sheet foreign key linking`. No prefix convention.
- Housekeeping (lint, dead code, schema fixes, brakeman) in its own commit.
- A batch "Testing everything" commit after a plumbing slice is acceptable.
- Body only for a one-line principle such as "Permission-related logic lives in permissions".
- PR descriptions: intent, the rules as bullets, out-of-scope and next steps, validation. Link issues; screenshots for visual changes.
- Keep credentials and local env files out of commits.
- Layer order for Logven features: migration + model, domain objects, runner/builder/jobs, prompts, HTTP plumbing slice, UI last.

## Known legacy exceptions (do not copy)

- `.badge` renders a dot; do not add status dots.
- Some headings use `text-label` instead of `text-title`.
- `components/layout.css` is 425 lines; do not grow it.
- Some components have one caller; inline new single-use ones.
- Legacy view coverage exists in tests; it is not precedent.
- The Sheets actions bypass authorization; do not copy it.
- `project_role_tone` has a fallback that other tone helpers do not use.
