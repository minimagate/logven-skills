# B. What Paolo changes when he pushes onto Michelangelo's PRs

Source: `B-paolo-commits-on-mikes-prs.md` (15 PRs, 155 non-merge Paolo commits). I read the diffs with `git show` in `logvenhq/logven`. Paolo is `psguazz`; Michelangelo is `minimagate`/`michelangelogubinelli`.

## 0. Scope and caveats (read first)

Not every Paolo commit on a Michelangelo PR corrects Michelangelo's work. I sorted them like this:

| Bucket | PRs / commits | Treated as |
|---|---|---|
| **Direct corrections**: Paolo commits made after Michelangelo's commits, rewriting his code | #65 (3), #69 (1), #129 (1), #140 (5), #143 (11), #144 (7), #148 (about 45 of 68, from `9c522e6b` to `e1b28691`), #155 (1), #157 (4), #160 (3), #177 (`597e1fec`, `9b1746fc`), #182 (2) | **Primary evidence** |
| Paolo's own feature work that sits under or merges into Michelangelo's branch | #52 (Paolo built the shapes form; Michelangelo's `forms ui v1` came after), #161 (all 11 Paolo commits come before Michelangelo's), #177 (the first 15 Paolo commits plus `f4c77846`..`e9c53baf`, which are his `workflow_tabs`/`profiles`/`editing_specs` branches) | Context only, not counted as corrections |
| Prompt and eval tuning in #148 (`b6d8437c`, `ee6ac583`, `12f4fdab`, `1d4a1da7`, `afea7b5a`, `621839c9`, …) | | Experiments, not corrections |
| Merges with main, `Fixing CI`, `Linting`, `Silly brakeman`, `Updating brakeman` | | Skipped as trivial |

PR #148 ("Vanilla-Icecream") is effectively a co-written rewrite. Michelangelo pushed 20 commits that introduced the `run()` sandbox, the Manifest, the Workbook, the tool class attributes and the Host. Paolo then pushed about 45 commits that restructured nearly all of it. That makes it the richest single source of evidence.

Where review comments exist (A-paolo-comments.md), they line up with the commits. On #65 and #140 he first commented in Italian and then pushed the fixes himself.

---

## 1. Taxonomy of corrections, ranked by frequency and weight

Strength: **S** means multiple independent instances (3 or more, usually across PRs). **M** means 2. **W** means a single instance.

### R1. Delete speculative machinery that nothing needs yet (YAGNI). [S, highest weight]
**Rule: when you add instrumentation, configurability, extra hooks, fallbacks or "just in case" branches, delete them unless a current caller needs them. Do not ship them preemptively.**

| PR / sha | File | What went |
|---|---|---|
| #148 `a5838de6` "Unused logs, redundant timings" | `app/models/workers/builder/base.rb` | `timed(label)`, `timings_report`, `duration`, `now` (monotonic clock) plus the `Build time:` logs: -31 lines. Test changed to `assert_nil @workflow.logs` |
| #148 `633e2cde` "Simpler host" | `app/models/workers/runner/host.rb` | `initialize(run, limits: {})` injectable limits, `OWN_LIMITS/LIMITS` merge, `MAX_RECORDED_BYTES`/`MAX_RUN_RECORDED_BYTES` truncation, `recordable`, `record`, `EXPECTED_ERRORS` + `Rails.error.report`, `remaining_time`. Went from 93 lines to 48 |
| #148 `5d144876` "Removing redundant code" (body: "We have specialized calls and callers, and don't need the generic budget and calls") | deletes `workers/call.rb`, `runner/budget.rb`, `calls/_call.html.erb`; adds migration `DropWorkersCalls` | a generic `Call` table and a `Budget` running in parallel with the specialised `LlmCall/TableCall/ToolCall` |
| #148 `e9bbad87` "Stagnation hints are meaningless" | `builder/base.rb` | `STAGNATION_HINT_AFTER`, `feedback(errors, repeats)` |
| #148 `cfb2f764` "Deterministic sampling" (body: "Either we make everything random, or nothing") | `app/models/shapes/sample.rb` | `seed:` parameter, `@ai_samples` counter, and 2 tests on seed rotation |
| #182 `25f15b1e` "Dropping submit tool" (body: "No reason and no evidence that a 'i'm done' tool is easier…") | `chat/structured.rb`, `chat/turn.rb`, `builder/tools.rb` | `finish_with:` option and the `Submit` tool class (-74 lines) |
| #157 `cec006e8` "Symmetry in env variables" | `config/initializers/ruby_llm.rb` | `ENV["OPENROUTER_API_KEY"] \|\| ENV.fetch("LOGVEN_LLM_API_KEY", …)` dual lookup |
| #140 `f8dc23f8` "Removing redundant updates" (review: "A cosa serve questo?") | `app/javascript/controllers/toggle_controller.js` | `syncTriggersIn` (aria label syncing), -21 lines |
| #148 `87ec2f2a` "Dead code" | `toggle_controller.js` | unused `stop(event)` |
| #148 `e1b28691` "Dead code" | `app/models/workers/builder.rb`, `workers/runtime/host.rb` | 460 lines of old files left behind after Michelangelo's refactor |
| #144 `945641f6` "Redundant information" | `step_builder/base.rb`, `coach.rb`, `graph.rb`, `prompts/graph.md` | `available_inputs(step)`, an extra LLM message duplicating `step.to_h.to_json`, plus 2 tests |
| #65 `923a3a34` "We don't use the edit page" (review: "Perché ci serve una pagina apposta?") | `node_runs_controller.rb`, `node_runs/edit.html.erb`, `routes.rb` | a whole `edit` page plus the html/turbo_stream branching in `update` |

Before and after (#148 `633e2cde`):
```ruby
# before
def initialize(run, limits: {})
  @budget = Budget.new(OWN_LIMITS.merge(limits.slice(*OWN_LIMITS.keys)), deadline:)
  @llm_caller = LlmCaller.new(run, count_limit: limits.fetch(:llm_calls, LlmCaller::COUNT_LIMIT))
  ...
# after
def initialize(run)
  @run = run
end
```

### R2. Remove redundant checks, guards and duplicated validation. [S]
**Rule: when a condition is already guaranteed upstream (policy scope, UI validation, an existing validator or policy), do not re-check it in the view, controller or model.**

- #65 `46b6a6a0` "Redundant checks". `app/views/agent_runs/_card.html.erb` and `_row.html.erb` lose `show_run = policy(run).show?`, the `manual_input_node_run` lookup and the `if destination … else` duplicate markup (-63/+30). The review comment says: "Questo è vero per definizione, sennò non vedremmo nemmeno la card."
- #65 `b90db06b` reverts Michelangelo's `AgentProjectTransferPolicy` and its 4 tests (-77). Review: changing `project_id` together with name and details "non ha senso… al massimo un controller dedicato". **Do not bolt a new policy class onto an action that should not allow the operation in the first place.**
- #177 `597e1fec` "Cleaning up update flow" (body: "Permission-related logic lives in permissions"). It deletes the model validation `validate_frozen_when_ready` and its test from `workers/workflow.rb`.
- #140 `78d0ec4c` (body: "Prompt just has to be present, the UI is already validating against that and showing other errors doesn't help"). It deletes `@prompt_error` composition in `assistant/chats_controller.rb`.
- #182 `6612c69a` drops `class ToolCallLimit` plus `rescue ToolCallLimit; raise` in `chat/structured.rb`.

### R3. Do not invent a parallel mechanism; use the interface or convention that already exists. [S]
**Rule: when the codebase already has an interface (Meterable, Shapes, Tools DSL, turbo_id, policy, profile constants), route through it. Do not add an escape hatch, a registry or a hand-rolled form/cast layer.**

- #148 `20d8d7b3` "Restoring tool dsl" (body: "The entire point is to have a standard interface and being able to add and remove tools without having to update a registry by hand"). It reverts Michelangelo's `876e5026` `TOOLS = %w[Workers::Tools::Google::GetEmail …]` + `class_attribute :tool_name, …` back to the self-registering DSL (`tool_name "google_get_email"`).
- #148 `a277aa1d` "Respecting meter interface" (body: "We have an interface for this, let's not invent hatches that do nothing"). It removes the public `Chat::Structured#usage` and `call.assign_attributes(structured.usage)` in `runner/host.rb`, and passes `call` as the meterable: `Chat::Structured.new(chat, call).complete`.
- #148 `176ec032` "Shape params" deletes `app/models/workers/run_input.rb` (73 lines of `permitted_for`, `cast_hash`, `field_kind`), `_input_field.html.erb` (47 lines) and `run_input_test.rb`. In their place it uses `params.expect(workers_workflow_run: [:workflow_id, input: Shapes::Base.new(workflow.input_shape).to_params])` and the shared `shapes/_fields` partial.
- #140 `e0d0c8c4` "No hard coded ids". `"app-chat-sidebar-body"` becomes `Assistant::Chat.turbo_id`. Review: "Non aggiungiamo id a caso — teniamo solo i vari metodi turbo_id… (vale dappertutto)."
- #160 `a76487c3` unifies two Redcarpet setups (`Assistant::Message.markdown` and the helper) into one `MarkdownRenderer`, and `.trix-content` + `lexxy-editor` styles into one `.markdown` class.
- #160 `e1b158e2` "Configuring sanitizer". A local `MARKDOWN_TAGS` constant becomes `config/initializers/sanitizer.rb` extending `Rails::HTML5::SafeListSanitizer.allowed_tags`.

### R4. Explicit over implicit or "magic". [S]
**Rule: when behaviour depends on hidden state (thread-locals, monkeypatched `prepend`, YAML lookups keyed by a stage tag, env-var switches, data tables driving a generic grader), replace it with explicit constants and calls at the use site.**

- #144 `da567a54` "Formalizing profiles". Deletes `Workers::LlmStage` (a thread-local stage tag), `config/llm_profiles.yml` and the `ruby_llm.rb` profile wiring. Each builder class gets `PROFILE = Assistant::Profiles::GEMMA_NO_THINKING` and `Assistant::ProfiledChat.with_profile(PROFILE)` (-218/+75).
  ```ruby
  # before
  chat = Workers::LlmStage.tag(:coach) { RubyLLM.chat }
  # after
  PROFILE = Assistant::Profiles::GEMMA_NO_THINKING
  chat = Assistant::ProfiledChat.with_profile(PROFILE)
  ```
- #144 `7b381491` "Updating helper" deletes `EvalProfiles::ChatOptions` (`RubyLLM.singleton_class.prepend`), `install!`, `stage_parameters` and `load_config` YAML merging.
- #143 `92db9ced` "Choosing profiles" replaces `ENV["EVAL_PROFILES"]` with a CLI option `-p` (`method_option :profile`) and `EvalProfiles.select(options[:profile])`. Tests stop mutating ENV.
- #157 `b5188688` "Defining profiles properly" moves `Base::PLAN_PROFILE`/`CODE_PROFILE` (with a justifying comment) to `PROFILE` constants in `Plan` and `Code` themselves.
- #143 `1eb2b1ba` "Explicit assertions" deletes the generic `assert_diff(before, after, expected)` grader driven by `{table:, field:, created:/updated:/deleted:/unchanged:}` hashes. Each eval now writes plain assertions (`find_record` plus `assert_nil before_record` / `assert after_record`, or `assert_equal before, after`). He accepts the repetition in exchange for readability.
- #148 `489b7190`/`40c08332`/`e20bd7c9` "Explicit workers refs / Explicit calls / Removing old manifest". Michelangelo's JSON `manifest` column and 201-line `Manifest` validator become `Workers::TableRef`/`ToolRef` and `LlmCall`/`TableCall`/`ToolCall` ActiveRecord models with associations and validations. Migration: `remove_column :workers_workflows, :manifest, :jsonb`.
- #148 `baa8605b` → `744c9dad` "Explicit workbook sections / Dropping workbook". Michelangelo's `Workers::Workbook` parsed `## ` headings out of markdown (`REQUIRED_SECTIONS`). It is replaced by real columns, later consolidated into one `spec` field (`5668552d`).

### R5. Fewer layers: inline one-off helpers, wrappers and base classes. [S]
**Rule: when a module, class, base class or helper has exactly one caller or only wraps a single call, inline it. Add a layer only when it carries real shared behaviour.**

- #143 `5893d69d` "Redundant seeeds" deletes `evals/builder/seeded_project.rb`, a module whose only method forwarded to `create_benchmark_project`.
- #143 `89428ef6` and `6a121fc3` delete `project_prompt_outcomes.rb` (an `EXPECTED` hash keyed by case name) and `project_prompt_grader.rb`, folding the expected data next to each prompt and the helpers into `BaseEval`.
- #148 `594727ee` "No base phase" deletes `app/models/workers/builder/phase.rb` (an inheritance base with `chat(name, shape)` and `complete`). `Plan` and `Code` now spell out `Chat::Profiled.with_profile(...).with_instructions(...).with_schema(...)` inline.
- #144 `af7e973b` "Cleaning up error handling" deletes the `apply_graph { … }` helper, which turned exceptions into return values (and carried a 5-line justifying comment). It uses a plain `rescue => e` in the loop instead (-31/+12).
- #148 `1814cfbb` "Cleaning up base loop" inlines `code_until_checked` into `build!`. A failure now `raise`s and is handled by the single `rescue`, instead of returning `errors` and branching on it.
- #140 `cf6101d5` "Inlining one-off classes" deletes `app/assets/tailwind/components/assistant.css` (128 lines of `@apply` classes) and inlines Tailwind utilities in 9 partials. Review: "Questo non è un componente, sono tutte classi usate esattamente una volta. Mettiamole direttamente nei template."
- #148 `ebed8b61` moves `register_models!` from the eval command into a `BaseEval` `setup` block.

### R6. Put logic in its own named object and file; keep controllers and helpers thin. [S]
**Rule: when a model has a nested helper class, or a helper holds non-trivial logic, extract it to its own file in `app/models` with its own test. Controllers expose one object, not many precomputed ivars.**

- #69 `28ec7098` "Extracting summary". `class AgentRun::Summary` (nested, plus a `self.summary(scope)` factory and an explanatory comment) moves to `app/models/agent_run_summary.rb`, and its test moves to `test/models/agent_run_summary_test.rb`. `DashboardsController#show` goes from 10 ivars (`@run_count`, `@running_run_count`, `@attention_items`, …) to `@summary = AgentRunSummary.new(...)`, and the view calls `@summary.in_progress_count`, etc.
- #160 `f967b512` "Extracting markdown nonsense" moves `render_markdown`/`separate_markdown_tables` out of `ApplicationHelper` into `app/models/markdown_renderer.rb`, and adds `test/models/markdown_renderer_test.rb` with 5 cases.
- #148 `f869d363`, `ea7ef144`, `8bd31140`, `003ae1b3` break the monolithic `workers/builder.rb` (206 lines) into `builder/{base,plan,code,check}.rb`, and the Host into `runner/{llm,table,tool}_caller.rb`.
- #148 `bed13c00` "Separating generic runtime and app specific stuff" moves the generic sandbox to `lib/runtime/{session,child,error}.rb` and keeps the app-specific part in `app/models/workers/runner/sandbox.rb`.
- #148 `50b1fb25` "Tests tests tests" gives one test file per class (`analyze_test`, `check_test`, `code_test`, `plan_test`, `llm_caller_test`, `table_caller_test`, `tool_caller_test`) and shrinks `host_test.rb` by about 330 lines.

### R7. Naming: drop redundant prefixes, be specific, keep params consistent. [S]
**Rule: inside a namespace, do not repeat the namespace in the name. Name actions by what they act on. Keep param keys the same across sibling forms.**

- #148 `358a3dc7` "Renaming runs": `Workers::WorkflowRun` → `Workers::Run`, with routes `workflow_runs` → `runs`, the policy, views, tests and `rename_table :workers_workflow_runs, :workers_runs` (36 files).
- #148 `7294ac1e`: `Workers::WorkflowRevisioner` → `Workers::Revisioner`.
- #148 `a287830c` "Renaming sheet actions": `delete/list/update.rb` → `delete_record/list_records/update_record.rb` (26 files).
- #140 `fab4b200`: message param `:content` → `:prompt`, matching the chat form, with a shared `_prompt.html.erb` partial.
- #140 `78d0ec4c`: `new_assistant_chat_path(context_domain: …)` → `new_assistant_chat_path(assistant_chat: {...})`, so `new` reuses `assistant_chat_params`. Review: "teniamo i params in sync e usiamo l'auth corretta (questo non è `create`)". `authorize @assistant_chat, :create?` → `authorize @assistant_chat`.

### R8. Reuse view partials instead of duplicating markup. [M]
**Rule: when two forms or views render the same control, extract one partial and render it from both.**
- #140 `fab4b200` "Sharing composer input" (body: "So we can keep using it after the chat starts") adds `assistant/messages/_prompt.html.erb`, used by both `chats/_new` and `messages/_form`. The old ad-hoc blue-button form (`bg-blue-600 …`) is removed.
- #65 `46b6a6a0` collapses the duplicated `<header>`/`<div>` blocks in `_card.html.erb`.

### R9. Constants for magic strings and patterns, and Rails 8 idioms. [M]
- #129 `d3c35cbc` "Extracting date/time patterns" adds `DATE_PATTERN = "%Y-%m-%d"` and `DATETIME_PATTERN` on `Shapes::InstanceValidator`, reused in `cast.rb` instead of the repeated literals `"%Y-%m-%dT%H:%M"`. It also adds a `# TODO` in `shape_inference.rb` rather than half-solving it.
- #144 `af7e973b`: `STAGNATION_ERROR` constant. #182 `6612c69a`: `STOPPED_MESSAGE` constant, asserted in tests.
- #177 `597e1fec`: `params.require(:workers_workflow).permit(...)` → `params.expect(workers_workflow: [...])`. #148 `176ec032` does the same.
- Counter-example, so this is not absolute: #148 `1814cfbb` re-inlines `RETRY_HINT` into the heredoc when it had a single use.

### R10. Make wrappers behave like the thing they wrap; no status-symbol protocols. [M]
**Rule: when you wrap a library object (a chat or turn), return what the library returns and model "stopped early" as a normal message. Do not return `:replied/:limit/:repeated` symbols that every caller must `case` on.**
- #182 `6612c69a` "Sane turn logic" (body: "`Turn` behaves like a normal chat — it simply ends early with a made up message…"). `Chat::Turn#run` now returns the final message, and on a loop or limit appends `STOPPED_MESSAGE`. It removes the `case turn.run when :replied … when :limit then raise` in `structured.rb` and the `if ending.in?(%i[repeated limit])` in `assistant/agent.rb`. It adds `test/models/chat/turn_test.rb` (4 cases).
- #144 `af7e973b` / #148 `1814cfbb`: exceptions flow through `rescue` instead of being converted to return values.

### R11. Migrations must be reversible. [W]
- #148 `9c522e6b` "Reversible migrations": Michelangelo's `def up; drop_table …; end; def down; raise ActiveRecord::IrreversibleMigration` → `def change` with `drop_table :x do |t| … end` blocks that restate the columns. His later drops follow the same pattern (`5d144876` `DropWorkersCalls`; `e20bd7c9` `remove_column … :jsonb, default: {}, null: false`).

### R12. Configuration: fail loudly and treat providers symmetrically. [M]
- #143 `5893d69d`: `ENV["LOGVEN_LLM_URL"]` → `ENV.fetch("LOGVEN_LLM_URL")`, and `ENV.fetch("LOGVEN_LLM_MODEL", "openrouter/auto")` → `ENV.fetch("LOGVEN_LLM_MODEL")`. No silent defaults. (Later commits re-add `dummy-*` defaults for CI, so this applies to real values, not test placeholders.)
- #157 `cec006e8`: no provider-specific env precedence.
- #143 `d6c76ac9` removes the up-front `abort "Set LOGVEN_LLM_API_KEY or LOGVEN_LLM_URL…"` guard in `eval_command.rb`.

### R13. Comments: delete narrative and justification comments. [S, with nuance]
**Rule: do not write comments that explain or defend a design choice ("Keeping the authorized relation as the input makes…", "OpenAI's strict mode rejects…", "LOGVEN_LLM_PROFILE switches every stage…"). Make the code readable instead.** Paolo deleted such comments in:
- #69 `28ec7098`: 3-line comment on `AgentRun.summary`
- #144 `af7e973b`: 5-line comment on `apply_graph`
- #144 `da567a54`: comment on `LlmStage`
- #157 `9e0a7c60` "Readable strict": the comment inside `to_schema`, rewritten as straight-line assignments
- #157 `cec006e8`: 3 comment blocks in `ruby_llm.rb`
- #157 `b5188688`: profile comment
- #160 `e1b158e2`: `MARKDOWN_TAGS` comment
- #182 `6612c69a`: 6-line class comment on `Turn`, plus "Returns how the turn ended…"
- #182 `25f15b1e`: `Submit` and `finish_with` comments

Nuance: Paolo does write a comment where code is a genuine hack. In #157 `dcbfdee4` he adds comments on the `ModelStub`/`ModelStoreStub` monkeypatches in the test helper, and in #148 `7954dcd3` he comments `format_errors`. So the bar is "no explanatory prose for ordinary code".

### R14. Tests: explicit, colocated with the class, with a smoke test per page. [S]
- They move with extracted code: #69 (`agent_run_summary_test.rb`), #160 (`markdown_renderer_test.rb`), #148 `50b1fb25` (one file per caller), #182 (`turn_test.rb`).
- Deleted together with deleted features: #65 (transfer policy tests), #144 (`available_inputs` tests), #148 `cfb2f764` (seed tests), `176ec032` (`run_input_test.rb`), `e20bd7c9` (`manifest_test.rb`, -154).
- Explicit per-case assertions beat data-driven graders (#143 `1eb2b1ba`, `002279ad` "Exploding eval cases": one 483-line `project_prompt_cases.rb` becomes 17 `*_eval.rb` files).
- Test-only code moves out of production code: #143 `f141f158` moves `create_benchmark_project` from `db/seeds/asteria_aerospace.rb` into `BaseEval#seed_project`.
- From the related review (A-paolo-comments, just above #65): "almeno uno per pagina… `get index_whatever_path; assert_response :ok`" and one test per branch of an action.

### R15. UI and CSS specifics. [M]
- **Tailwind utilities inline for one-off styles; no `@layer components` class used once** (#140 `cf6101d5`). Arbitrary values are fine (`[border-color:color-mix(...)]`, `[&::-webkit-details-marker]:hidden`, `group-open:rotate-180`, `empty:before:content-['Thinking…']`).
- **One shared class for one concept** (#160 `a76487c3`: `.trix-content` + `lexxy-editor` → `.markdown`).
- **No hard-coded DOM ids; use `Model.turbo_id` / `record.turbo_id`** (#140 `e0d0c8c4`).
- **Small spacing and layout fixes are done directly** (#155 `0f3ff673`: full-width primary submit `btn btn-primary w-full mt-2`, centered "Forgot password?", remove `pt-12 sm:pt-20`).
- **Do not add a separate page when the existing page's form works** (#65 `923a3a34`).
- **JS: delete Stimulus methods that are unused or only sync redundant state** (#140 `f8dc23f8`, #148 `87ec2f2a`).
- **Multi-line ERB helper args**: in #140 `78d0ec4c` he reformats `data:`/`aria:` hashes onto separate lines with trailing commas.

### R16. LLM-pipeline-specific judgement. [M]
- Do not send the model information it already has (#144 `945641f6`, `56cd0904` "Combining snippets that are always together": merges `prompts/graph/brief.md` into `graph.md`).
- Do not add hints the model cannot act on (#148 `e9bbad87`: "The coder only sees the current version, not the approach it took").
- Do not add a tool or protocol without evidence it helps (#182 `25f15b1e`).
- When something must be synchronous for the caller, do not background it (#148 `50d9d316` "Sync tools": `build_later!` → `build_now!`, because "it has to be sync for the assistant to interact with it").

---

## 2. Grouped view

### What he deletes or simplifies (over-engineering signals)
Timing and instrumentation (`a5838de6`); injectable limits and byte-truncation (`633e2cde`); generic Budget and Call next to specific ones (`5d144876`); seeded randomness (`cfb2f764`); "finish" tools and options (`25f15b1e`); custom exceptions that are only re-raised (`6612c69a`); wrapper modules and helpers with one caller (`5893d69d`, `594727ee`, `af7e973b`); data-driven generic graders (`1eb2b1ba`); thread-local, YAML and monkeypatch config (`da567a54`, `7b381491`); a hand-written param caster (`176ec032`); duplicated policy checks in views (`46b6a6a0`); an extra policy class (`b90db06b`); an extra page (`923a3a34`); dead files left after refactors (`e1b28691`, `87ec2f2a`); a one-off CSS component file (`cf6101d5`); justification comments (R13). Net size across the 155 commits: about +11.4k / -10.1k lines. In the direct-correction commits deletions usually exceed insertions: `633e2cde` -118/+45, `5d144876` -153/+25, `176ec032` -192/+20, `cf6101d5` -158/+29, `46b6a6a0` -63/+30, `da567a54` -218/+75.

### What he moves, renames and reorganizes (structure signals)
Nested class to its own file (`28ec7098`); helper logic to a PORO in `app/models` (`f967b512`); monolith to `base/plan/code/check` (`f869d363`) and to `*_caller.rb` (`8bd31140`, `ea7ef144`); generic vs app code split into `lib/runtime` and `app/models/workers/runner` (`bed13c00`); namespace-redundant names shortened (`358a3dc7`, `7294ac1e`); verbs made specific (`a287830c`); chat modules grouped under `Chat::` (`0abd3f9a`: `assistant/structured_chat.rb` → `chat/structured.rb`, `assistant/profiles.rb` → `chat/profiled.rb`); framework config moved to `config/initializers` (`e1b158e2`); test-only code moved out of seeds (`f141f158`); constants moved to the class that uses them (`b5188688`).

### What he adds (tests, constraints, guards)
- Tests for every extracted unit (`agent_run_summary_test`, `markdown_renderer_test`, `turn_test`, the per-caller tests in `50b1fb25`, `application_record_test` in `049d20cb`).
- DB-level structure instead of JSON (`489b7190`, `40c08332`: `TableRef` with `validates :action_name, inclusion: {in: Sheets::Actions::Base::ACTIONS.keys}`).
- Reversible migrations (`9c522e6b`).
- A safe write path in rescue blocks: `ApplicationRecord#update_without_validation` replacing `update!` inside `rescue` (`049d20cb`).
- Strict `ENV.fetch` (`5893d69d`).
- He adds guards rarely. His net direction is removing guards that duplicate other layers.

### CSS, views, components and JS
See R15. In short: inline Tailwind utilities for single-use styling; share real components and partials; use `turbo_id` for ids; one CSS class per concept; fewer conditional branches in partials; no unused Stimulus actions.

---

## 3. His commit habits when stacking on someone else's PR

- **Size:** small and single-purpose. The median is 4 files per commit. Large ones are mechanical renames (`358a3dc7`, 36 files) or test reorganizations. One concern per commit: "Dead code", "Redundant checks", "Renaming runs".
- **Message style:** a short, lowercase-ish noun or gerund phrase, no Conventional-Commit prefix, no PR or issue refs. Examples: "Extracting summary", "Inlining one-off classes", "Simpler host", "Removing redundant code", "Sane turn logic", "Dead code". Some are informal or self-deprecating: "Fixing test imports??", "Handling dumb quirks?!", "Silly brakeman", "Various fixes that I haven't read", "Tests tests tests".
- **Explains or silent:** mostly silent. Only **21 of 155** commits have a body. When he does write one, it is one or two sentences of principle, not a changelog:
  - "We have an interface for this, let's not invent hatches that do nothing" (`a277aa1d`)
  - "Permission-related logic lives in permissions" (`597e1fec`)
  - "No reason and no evidence that…" (`25f15b1e`)
  - "Either we make everything random, or nothing" (`cfb2f764`)
  - "Openrouter is not special…" (`cec006e8`)
- **Comment, then fix:** on #65 and #140 he first left Italian review comments (each one a one-line principle) and then pushed the fixes himself on the same branch. On #148, #157, #160 and #182 there are no review comments at all; he just pushed the corrections.
- **Reverts:** he uses `git revert` for a whole rejected commit (#65 `b90db06b`) rather than editing it away.
- **Merges main into the PR branch** himself and resolves conflicts there (`b86df74d`, `e64f593b`, `8a8791cc`, `a832ac3d`, `d554afed`). He does not rebase.
- **Tests travel with each correction.** Almost every refactor commit touches the matching `test/` file in the same commit.

---

## 4. Candidate guideline rules and review-checklist items

### Candidate guideline rules (for planning and implementation briefs)

| # | Rule | Strength | Evidence |
|---|---|---|---|
| G1 | Build only what a current caller needs. No timing logs, configurable limits, seeds, fallbacks, extra tools or options "for later". | **Strong** | `a5838de6`, `633e2cde`, `5d144876`, `cfb2f764`, `25f15b1e`, `e9bbad87`, `945641f6`, `923a3a34` |
| G2 | Before adding a mechanism, find the existing interface (Tools DSL, Meterable, Shapes `to_params`/`cast`, `turbo_id`, policies, profiles) and use it. Never replace an established convention without agreement. | **Strong** | `20d8d7b3`, `a277aa1d`, `176ec032`, `e0d0c8c4`, `a76487c3` |
| G3 | Authorization lives in policies and policy scopes, and only there. Do not re-check `policy(x).show?` in views of already-scoped records, and do not duplicate permission rules as model validations. | **Strong** | `46b6a6a0`, `597e1fec`, `b90db06b` |
| G4 | Prefer explicit constants and calls at the use site over thread-locals, `prepend` monkeypatches, YAML lookups or env-var switches. Prefer CLI options over env vars for tooling. | **Strong** | `da567a54`, `7b381491`, `92db9ced`, `b5188688` |
| G5 | Model structured data as tables and associations, not JSON blobs or markdown parsed by headings. | **Strong** (one PR, three separate commits) | `489b7190`, `40c08332`, `e20bd7c9`, `baa8605b`, `744c9dad` |
| G6 | One class per file. Extract nested classes and helper logic to `app/models/<name>.rb` with a matching test. Controllers assign one presenter-like object rather than many ivars. | **Strong** | `28ec7098`, `f967b512`, `f869d363`, `8bd31140` |
| G7 | Inline any helper, module, base class or CSS class used exactly once. | **Strong** | `5893d69d`, `594727ee`, `af7e973b`, `1814cfbb`, `cf6101d5` |
| G8 | Do not repeat the namespace in names (`Workers::Run`, not `Workers::WorkflowRun`). Use specific verb+noun action names. Keep param keys consistent across forms. | **Strong** | `358a3dc7`, `7294ac1e`, `a287830c`, `fab4b200`, `78d0ec4c` |
| G9 | Wrappers return what the wrapped thing returns. Signal failure with exceptions or normal messages, not status symbols or exceptions converted to return values. | Medium (2) | `6612c69a`, `af7e973b`, `1814cfbb` |
| G10 | Migrations are reversible (`def change`, a `drop_table` block with columns, `remove_column` with its type). | Weak (1 explicit fix, then consistent use) | `9c522e6b`, `5d144876`, `e20bd7c9` |
| G11 | Use `ENV.fetch` for required config. No provider-specific precedence chains. | Medium | `5893d69d`, `cec006e8` |
| G12 | No comments that narrate or justify ordinary code. Comment only genuine hacks or stubs. | **Strong** | R13 list |
| G13 | Use `params.expect(model: [...])`, not `require/permit`. | Medium | `597e1fec`, `176ec032` |
| G14 | Tailwind: inline utilities for single-use styles. Extract a component class only when it is reused. One semantic class per concept. | Medium | `cf6101d5`, `a76487c3` |
| G15 | Reuse the existing page or form before adding a new page or route. Share partials for identical controls. | Medium | `923a3a34`, `fab4b200` |
| G16 | When refactoring, delete the old files in the same PR. | Medium | `e1b28691`, `87ec2f2a` |
| G17 | Test code (benchmark seeding, eval graders) does not live in production files like `db/seeds`. | Weak | `f141f158` |
| G18 | LLM prompts: do not resend information already in context, and do not add hints the model cannot act on. | Medium | `945641f6`, `56cd0904`, `e9bbad87` |
| G19 | Do not background work the caller must see synchronously. | Weak | `50d9d316` |

### Candidate review-checklist items (to run on a diff before asking Paolo)

1. **Dead weight:** Is any new method, option, constant, column or JS action unused, or used only by its own test? Delete it. (Strong: `87ec2f2a`, `e1b28691`, `a5838de6`, `f8dc23f8`)
2. **Parallel mechanism:** Does this diff add a second way to do something the codebase already does (registry vs DSL, generic vs specific calls, own caster vs Shapes, own renderer)? (Strong: `20d8d7b3`, `5d144876`, `176ec032`, `a76487c3`)
3. **Redundant auth or validation:** Is anything re-checking what a policy scope, policy or UI `required` already guarantees? (Strong: `46b6a6a0`, `597e1fec`, `78d0ec4c`)
4. **Single-use abstraction:** Is a new module, base class, helper or CSS class used once? Inline it. (Strong: `5893d69d`, `594727ee`, `cf6101d5`)
5. **Implicit config:** Any `Thread.current`, `prepend`, YAML-lookup-by-tag or new env var? Replace it with an explicit constant or argument. (Strong: `da567a54`, `7b381491`, `92db9ced`)
6. **JSON blob or parsed markdown** holding structured data that should be rows? (Strong: `e20bd7c9`, `744c9dad`)
7. **Names:** Does the name repeat its namespace? Are param keys consistent with sibling forms? Are action names specific? (Strong: `358a3dc7`, `a287830c`, `fab4b200`)
8. **Comments:** Delete any comment that explains why the code is the way it is, unless it marks a hack. (Strong)
9. **Ids in views:** any hard-coded `id="..."` or `turbo_stream.update "some-id"`? Use `turbo_id`. (Weak, but the review comment says "vale dappertutto": `e0d0c8c4`)
10. **Migrations:** is every migration reversible? (Weak: `9c522e6b`)
11. **Params:** `params.expect`? Does `new` reuse the same params method as `create`, with the right `authorize` (no explicit `:create?` in `new`)? (Medium: `78d0ec4c`, `597e1fec`)
12. **Controller ivars:** more than 2 or 3 derived ivars for one view? Pass one object instead. (Weak: `28ec7098`)
13. **Tests:** does each new or extracted class have its own `test/models/...` file, and was each deleted feature's test deleted too? Does each page have a smoke `get …; assert_response :ok`? (Strong)
14. **Return protocol:** does a method return status symbols the caller must `case` on, or swallow exceptions into return values? (Medium: `6612c69a`, `af7e973b`)
15. **New page or route:** could the existing page's form do it? (Weak: `923a3a34`)
16. **Leftover files** after a move or rename? (Medium: `e1b28691`)
17. **Env:** `ENV.fetch` for required values, and no per-provider fallbacks? (Medium: `5893d69d`, `cec006e8`)

### Not supported by the evidence (so do not claim it)
- I saw no corrections about performance or N+1. `5d144876` only updates `includes` after a model change, and `7ba3d2ed` adjusts `includes`.
- I saw no corrections about security hardening by Paolo. He reverted a security-motivated policy addition (`b90db06b`) on product-design grounds, not because it was insecure.
- I saw no strong colour or design-token corrections. His CSS changes are structural (inline vs component), not palette.
