# C: How Paolo (psguazz) structures and builds big features in logvenhq/logven

Sources: `C-paolo-own-prs.md` (PR descriptions, commit lists, Michelangelo's comments) plus read-only git on `/Users/michelangelogubinelli/Github/logven` (`git log --stat` on each PR's merge range `M^1..M^2`, `git show`, and the current code on main). Shas are the ones on main. Some PRs were rebased before merging, so a few shas in the input file differ. For example, #88's "Builder -> StepBuilder" is `f988cd84` on main and `0e73ad80` in the input.

Volume: Paolo has about 930 commits (`psguazz` plus `Paolo Sguazzabia`) and Michelangelo about 515. All PRs are merged with merge commits (no squash), so per-commit slicing is preserved and visible.

---

## 1. Feature reconstructions

### F1. Type system / Shapes (#6, +2283/-423, 25 commits, July 2)
- **Order:** `c48c24c4` "Type system plumbing" creates five empty PORO classes under `app/models/shapes/` (`Base`, `ShapeValidator`, `InstanceValidator`, `Subshape`, `SchemaParser`). Each has `attr_accessor` and `initialize`, and its `validate` returns `[]`. `Base` already wires the public API (`valid?`, `validate(instance)`, `compare`). Each later commit fills **one** collaborator **together with its test file**: `5cd4d4d2` "Validating shape" (+50 code / +202 test), `2a2377e1` "Validating instances", `0289afa7` "Checking subtypes", `71e3fbb5` "Parsing JSON schemas". Only after that does he touch the rest of the app: `e44d660f` "Renaming schemas -> shapes" (a rename migration plus all callers), `9de1cdd1` "STI for nodes" (a `type` column and `workflow_nodes/*` subclasses), and then prompts (`8517a485` "Type system rules", which only touches `.md` prompt files). `ddf7677f` "Type inference?!" adds one more collaborator with its test.
- **Patterns introduced:** the `Shapes::` namespace of single-purpose POROs (validator, parser, inference, later cast, params, sample, json_schema), STI for node types, and prompt files kept beside the code.
- **Not built:** no UI. Seeds come last ("Some silly seeds").

### F2. Agent life cycle: build, commit, revise, run (#29, +1009/-176, 18 commits; extended by #87)
- **Order:** "Noise" and `44fff0ef` "Renaming outputs to runs" first (cleanup and rename before the feature). Then `f374eff2` "Defining agent statuses" (model). Then `af03a343` "Agent revision flow" adds **three new resource controllers** (`AgentBuildsController`, `AgentCommitsController`, `AgentRevisionsController`), each with its own policy (`AgentBuildPolicy`...), routes and controller tests, all in one commit and before the logic exists. `b03afc86` "Revision logic" (model plus model test) follows, then "Building individual steps" (another resource and policy), `b141b144` "String statuses" (migration), `062901e0` "Async flow", `7e126811` "Builder jobs" (two thin jobs), `304757e6` "Testing everything", and finally runs (`07ddf433` "Starting a new run", then `e2bc473e` "Async runs").
- **Patterns:** verbs become singular nested resources (`resource :build, :commit, :revision, only: :create` survive on main in `config/routes.rb`). There is a policy class per action resource (`Workers::WorkflowBuildPolicy#create?` delegates to `WorkflowPolicy#update?` and adds a domain predicate `buildable_later?`). The `verb_now!` / `verb_later!` pair lives on the model, and the job is a one-liner calling `_now!` (`Workflow#build_now!/build_later!`, `Run#start_now!/start_later!`, `WorkerBuildJob#perform`). Predicates such as `buildable_now?`, `buildable_later?` and `building_or_later?` guard transitions.
- **#87 "Agent lineage/versioning"** (11 commits) continues it in this order: migration plus model (`bb554942`), tests, then policies one by one ("Better agent policy", "Refining role meaning", "Refining other policies"), then "So many tests" and "Missing policy tests", and finally view tweaks. The description has an explicit **"Out of scope for this pr"** list and an "Open questions" list.

### F3. Cost metering (#76, +578/-45, 9 commits)
- **Order:** `d53202af` "Usage model" (migration, `Meter` model and a 171-line test), `09a3bc08` "Meterable concern" (concern plus its own test), `602a4ae4` "Applying meterable" (one `include` line on six models). Then one commit per measured dimension: "Tracking time", "Tracking tokens", "Tracking cost". Each touches the call sites plus tests. Then "Carrying costs over to new versions" (an edge case) and "Storing milliseconds".
- **Patterns:** a polymorphic `has_one :meter` concern with a class-level DSL (`include_meters_from`) and a `with_time_meter` block wrapper. The PR description explains the API with a code sample. Enforcement is by construction: "the LLM module now requires a `meter` object to be used at all".
- **Not built:** UI. The PR description says "If/when we decide to show some of this information in the UI, we should use `total_meter`".

### F4. Loops and ifs (#80, +1856/-264, 19 commits)
- **Order:** `250c35b9` "Adding loop/guard columns" (migration, model validation and a 304-line model test, all in one commit). Then runner (`7caad3a5`, `70d7c384` "Defining runner rules", which adds `Runner::NodeRunner`), then "Explicit shapes", "More validation", `a53ff69a` "Testing everything". Then builder (`de868b21` "Accepting new properties in builder"), then prompts (`fe3e669a` "Describing new rules", `ee3f0aa5` "Updating judge prompt", `d2498a23` "Saner example"). UI is a single 2-file commit, `e63c2c9e` "Rendering skipped status".
- **Framing:** "I want to keep things simple and avoid making the graphs more complex than they absolutely need to be... instead of dedicated `if` and `loop` nodes, I'm adding some extra rules to the existing nodes". The description has separate sections, "At build time" and "At runtime", per sub-feature.
- **Layer order:** schema+model → runtime → LLM builder → prompts → UI.

### F5. Sheets ("Shelf foundation" #98, then #108 actions, then #110 foreign keys)
- **#98 order:** `4b0601db` "Basic shelf tables" (three migrations and three tiny models, no logic). `c9e025cd` "Managing sheets" (controller, policy, index/new/show views, route, controller test, policy test and test attributes helper, all in one commit). `e5677529` "Managing records" (same slice for the child resource). "Sheet shapes" (migration and model), then `5e7f7448` "Testing everything" (model tests only). Then UI increments: "Rendering records", "Adding records and fields", "Editing records", "Editing fields". The PR is presented as "A very rough first draft of a table... Obviously very much a WIP... But the data is there, is editable, and validated."
- **#108** was started by Michelangelo with terse lowercase commits (`a61467d2` "data instrument", `568891b3` "data block", `940f430c` "ui", `428da812` "local env"). Paolo continued **in the same PR**: `a2e95264` "Renaming classes" (`DataInstrument` → `SheetActions`), "Simpler references", "Renaming get", `1d4b1824` "Connecting nodes and sheets" (migration), "Simpler tool runner", "Simpler data tools", tests, and `5cc8cfc1` "No local env", which deletes Michelangelo's initializer.
- **#110 order:** preparatory normalization first (`e5622955` "Case insensitive names", `59285533` "Normalizing names properly" with a migration, `431cdffd` "Normalizing sheet names, too"). Then `69df9a42` "Foreign key model" (migration, model and test), "Stronger validation", "Exposing foreign keys in shapes" (domain), `2c50c632` "Record associations" (second model and migration), "Building data object with foreign keys". After that the HTTP layer: `27c10ac2` "Adding/removing references" (controller, policy, turbo_stream views, route and a 99-line controller test). UI comes last ("Showing references", "Controls"), followed by hardening ("Validation/sanitization", `dcf5c09f` "N+1 queries", "Fixing/adding tests"). The description says "UI is very basic". The follow-up #114 "Fk UI cleanup" is a separate small PR.

### F6. Namespacing (#123, +14908/-14629, 415 files, 31 commits)
- **Purpose:** "Grouping the `workers` and `sheets` objects into their explicit modules -- will make it easier to add big concepts without going crazy with the names".
- **Slicing is mechanical and rename-safe.** `a03feb87` "Moving sheets" and `2fe54b6e` "Moving actions" are **pure `git mv` commits with 0 line changes** (`rename ... (100%)`), followed by separate "Declaring modules" / "Applying module" commits that add the `module` wrappers. Then "Renaming tables" (a migration adding `table_name_prefix` in `app/models/sheets.rb` and `workers.rb`), then policies (move, then apply), controllers ("Grouping controllers as well", "Explicit modules"), test helpers, routes ("Grouping worker routes"), and several "Updating references", "More renames", "MORE renames" and "Final pass" commits.
- **Why split move from edit:** in #56 he complained that "moving the controller and adding a `module` wrapper makes it seem like we deleted and recreated everything". #123 is the fix for that.
- **Not built:** behavior changes. Dead code ("Removing artifacts", which drops a table) is removed in the same sweep.

### F7. Assistant (#128 RubyLLM plumbing → #130 sidebar → #131 context and tools → #133 RubyLLM everywhere → #134 workers assistant)
- **#128 order:** gem (`a80541c8`), ActiveStorage, then **generator commits whose subject is the literal command** (`ffa65db7` "bin/rails generate ruby_llm:install chat:Assistant::Chat message:Assistant::Message", `c319bd53` "bin/rails generate ruby_llm:chat_ui ..."). Then `197ac3c0` "Cleaning up", which deletes the generated `models_controller` and views and trims the routes. Then "Connecting the pieces" (policy plus migration), "Cleaning up views", "Adding tests", "Turbo streams", "Broadcasting changes", "Auto scroll". This keeps the generated code reviewable separately from his edits. The same convention appears in older history: "rails g authentication", "rails g pundit:install".
- **The description has an ordered roadmap checklist:** "Prossimi step, in ordine: [ ] Spostare il chatbot in una sidebar... [ ] contesto... [ ] tool... [ ] storico" ("next steps, in order": move the chatbot to a sidebar, then context, then tools, then history). The following PRs #130, #131 and #133 execute that list in order, one PR per checkbox.
- **#131:** migration first ("Adding context data to chats"), then a controller class macro `assistant_context :sheets, resource_id: :table_id` (now in `ApplicationController.assistant_context`), then "Agent setup" (`Assistant::Agent` base, `Assistant::Sheets::Agent`, two tool classes), then tests ("Smoke tests", "Tests tests tests", "Enforcing stubbed requests"). Design rule from the description: "The tools themselves should do almost nothing -- they're a thin interface between existing functionality and methods and the chat."
- **#133:** migrate the old LLM layer to RubyLLM and then delete it (`d2e8ce12` "Removing LLM module").

### F8. "Chocolate": restructuring Michelangelo's code-based workers (#149, +3890/-3044, 67 commits, stacked on #148)
- **Context:** Michelangelo's #148 `vanilla-icecream` was a fast big-bang rewrite. It had 21 commits in about 1 day (`893a69a3` "Remove graph workflow builder and runner", `29199bda` "Add sandboxed run() runtime for workflows", `ad7473f7` "Add workbook-to-code workflow builder", `1eccd74e` "Show workbook, permissions, code and calls in the workflow UI", "eval suite", "final cleanup", `2cd2e2da` "Tidy the run() workflow change for review"). Paolo stacked #149 on it and reshaped it.
- **His stated goals (description):** "Clear separation between runtime (a thin wrapper around MiniRacer...) and runner (... app-related)"; "Explicit models for everything"; "Adherence to the standards of the app (shapes, meters, chat helpers rather than custom logic everywhere)"; "Overall cleanup".
- **Order:** `9c522e6b` "Reversible migrations" first. He rewrote Michelangelo's `def up; drop_table...` into `def change` with full `drop_table ... do |t| ... end` bodies. Then "Restoring tool dsl", "Respecting meter interface", "Shape params" (reuse of existing domain systems). Then explicit models: `489b7190` "Explicit workers refs" (`workers_table_refs` and `workers_tool_refs` tables) and `40c08332` "Explicit calls" (three tables, `tool_calls`, `table_calls`, `llm_calls`, each `include Meterable`). Then splitting: "Breaking up builder", `bed13c00` "Separating generic runtime and app specific stuff" (moves the sandbox to `lib/runtime/{session,child,error}.rb` with app glue in `app/models/workers/runner/`), "Breaking up runner host". Then removals ("Removing old manifest", "Dropping workbook", "Removing redundant code"), renames ("Renaming runs", "Renaming revisioner"), "Tests tests tests", and finally prompt and eval tuning.
- **Michelangelo's review found 10 correctness issues on this PR:** lost input casting, `list_records` silently capped at 50, a blocking `build_now!` in a tool, an aborted savepoint in dry runs, string-interpolated error arrays, deterministic sampling hiding branches, a `worflow_refs` typo plus `dependent: :destroy` erasing call history, a Zeitwerk-hostile registry, and three near-duplicate partials.

### F9. Workflow tabs, then spec editing (stack #166 → #167 → #170 → #171, merged together via #171)
- **#166 (Paolo's part):** `b0aaab2d` "Workflow tabs controller" adds `Workflows::BaseController` (with `section`, `assistant_context` and `set_workflow` scoped via `@project.workflows.find`) and one singular-resource controller per tab (`resource :spec`, `resource :code`, `resource :details`, `resources :runs`, `resources :revisions`). Then "Consolidating names", then one commit per page ("Spec page", "Code and runs pages", "Revisions page"), then "Using tab pages". The description: "This is very basic and is meant to be a scaffolding that needs to be extended rather than a final version. To do: [ ] ..." Michelangelo then added about 45 UI commits on the same branch.
- **#170:** `2e0b4fa1` "Basic plumbing" (specs controller, edit view, route, controller test). Then "HTML everywhere", "Splitting inputs and specs", `f13c5c57` "Spec permissions" (a separate `WorkflowSpecPolicy`, with commit body "Permission-related logic lives in permissions"), then `4a0af18d` "Spec draft flow" (migration), "Autosaving form", "Extracting details form".
- **#171** uses expand/contract inside one PR: `855249de` "Writing spec sections" adds the new columns, then `48c47d24` "Removing full spec fields" drops the old ones, then "Updating seeds and helpers".

### F10. Persisted calls (#183, +281/-43, 3 commits) and Evals (#85, #115, #145): small but conceptual
- #183 is 3 commits, but the description is a full design note: "So, new plan: ... But: ... So live runs are unaffected by this; dry runs will not show partial progress... But at least they do show up." It states the trade-off it accepts.
- #85 introduces `app/evals` (later `evals/`) with a `rails eval` command built on minitest, committed reports, and `rails eval:summary`. Evals are kept out of CI on purpose. #145 refactors them toward "one explicit eval file per scenario... Abstracting and simplifying via composition, not via configuration".

---

## 2. Generalized playbook

### Sequencing a big feature (bottom-up, with UI last)
1. **Clean up and rename first, so the new concept has room.** This happens in its own commits: #88 `f988cd84` "Builder -> StepBuilder" and `d91c2e87` "Renaming everything for good measure" before `7cd713e1` "Agent builder plumbing"; #29 "Noise" and "Renaming outputs to runs"; #110 name normalization before FKs; #6 "Renaming schemas -> shapes". The #88 description says: "a lot of noise here is about renaming this and some other things to make room for the new builder".
2. **Schema and model next.** The migration commit is usually tiny and paired with the model, often with a large model test (#76 `d53202af`, #80 `250c35b9`, #98 `4b0601db`, #110 `69df9a42`, #87 `bb554942`).
3. **Domain logic** in POROs or concerns, with tests (Shapes, Meterable, NodeRunner, Revisioner).
4. **Integrate with existing systems**: runner, then builder, then prompts (#80, #6, #24). Prompt `.md` edits go in their own commits.
5. **HTTP layer as a "plumbing" slice:** controller, policy, route, empty or near-empty views, controller test and policy test in one commit (`19566262` "Workflow controller plumbing" with empty `index/show.html.erb`; `e67c250e` "Node list plumbing"; `2e0b4fa1` "Basic plumbing"; `c9e025cd` "Managing sheets"; `af03a343` "Agent revision flow").
6. **UI last and minimal**, framed as rough ("very ugly diagram", "very rough first draft", "UI is very basic", "not meant to be usable in real life").
7. **Hardening tail:** N+1 queries, null checks, stricter validation, "Testing everything", "Linting", "Updating brakeman".

### "Plumbing first" (strong, 7 commits literally named so)
`c48c24c4` Type system plumbing, `0f1e7944` Runner plumbing, `19566262` Workflow controller plumbing, `7cd713e1` Agent builder plumbing, `e67c250e` Node list plumbing, `2e0b4fa1` Basic plumbing. The first commit of a new subsystem establishes the class/route/policy skeleton and its public interface with stubbed bodies. The following commits fill one piece each.

### Slicing commits
- One concern per commit, named for the concern ("Tracking time" / "Tracking tokens" / "Tracking cost").
- Pure moves are separate from edits (#123).
- Generated code gets its own commit, with the command as the subject (#128).
- Prompt changes are isolated ("Updating prompts", "Describing new rules", "Updating judge prompt", "Steps prompt").
- Tests either ride with the unit they cover (Shapes, Meter, Meterable) or come as a batch right after the feature skeleton ("Testing everything" ×3, "Tests tests tests" ×3, "So many tests", "Missing policy tests").
- Housekeeping is committed separately and named flatly: "Linting" ×15, "Fixing tests" ×9, "Dead code" ×6, "Updating brakeman" ×3, "Fixing schema" ×5.
- Commits are small. About 75% of subjects are 2-3 words, and most touch one layer.

### Slicing PRs
- **One capability per PR, often a chain:** #128 → #130 → #131 → #133 → #134 (assistant); #98 → #108 → #110 → #114 → #118 (sheets); #29 → #87 → #88 → #90 (agents); #166 → #167 → #170 → #171 (worker UI and specs).
- **Stacked PRs are common, and he finds them painful:** "Stacking this on top of #87 because it's easier this way" (#88); #149 on #148; #171 includes #166/#167/#170; `5ef576e3` "Stacks are terrible"; `d68b5e28` "Fixing stack conflict nonsense"; #178 "Rescuing #177 from nonsense conflicts"; #185 "Cherry picking the easy stuff from #182".
- **Follow-up cleanup PRs** after a feature: #35 "Backend tweaks", #39 "Final cleanup", #40 "Perf", #91 "Readability cleanup", #114 "Fk UI cleanup", #127 "Form fixes".
- **Pure refactor PRs are kept separate from features:** #123 Namespacing, #91 Readability cleanup, #77 native SolidQueue, #72 Simpler flows, #60/#73/#97 native HTML.

### Naming
- Domain namespaces mirrored across layers: `Workers::`, `Sheets::`, `Assistant::`, `Shapes::`, `Chat::`. Each has a module file with `table_name_prefix` (`workers_`, `sheets_`), plus `app/controllers/projects/workers/...`, `app/policies/workers/...` and `test/...` in parallel.
- Verbs become nouns and resources: `BuildsController`, `CommitsController`, `RevisionsController`, `RerunsController`, `table_references`. In #35: "No `resume` route" and "I nodi sono la loro risorsa a se" ("nodes are a resource of their own"). In a review on Michelangelo's PR (file A, line 113): "Queste dovrebbero essere risorse esplicite, non verbi a caso" ("these should be explicit resources, not random verbs").
- Templates are named by the resource they render, not by the page they appear on (#39): "BAD: `render "agents/step_form"` GOOD: `render "steps/form"`... Bisogna pensare in termini di risorse" ("you have to think in terms of resources").
- Role nouns for domain objects: `Revisioner`, `Builder::{Plan,Code,Analyze,Check}`, `Runner::{Host,Prelude,ToolCaller,TableCaller,LlmCaller}`, `NodeRunner`, `StepBuilder`, `AgentBuilder`.
- Predicates and bang verbs on models: `buildable_later?`, `building_or_later?`, `build_later!`, `start_now!`, `revise!`.
- He renames aggressively as the concept clarifies (schemas→shapes, outputs→runs, Builder→StepBuilder, agents→workers→workflows, data_instrument→sheet_actions, workbook→spec sections).

### Where code lives
- Business transitions live on the model or in PORO domain objects. When a model bloats, he extracts: #91 "Extracting revision logic" and "Extracting promotion logic" (now `Workers::Revisioner`). The description says the Agent and Step classes "were getting a bit bloated".
- Cross-cutting behavior goes in a concern with a class macro (`Meterable.include_meters_from`). Controller-level config uses class macros too (`section :workflows`, `assistant_context :workers, resource_id: :workflow_id`), "instead of reading the tea leaves with complicated match rules" (#56).
- Authorization lives in Pundit policies, one per action resource where needed (`WorkflowBuildPolicy`, `WorkflowCommitPolicy`, `WorkflowSpecPolicy`). Commit body of `f13c5c57`: "Permission-related logic lives in permissions".
- Jobs are one-line wrappers around a model `_now!` method, with SolidQueue `limits_concurrency` (#77 replaced custom claiming with "native SolidQueue concurrency controls").
- Generic infrastructure goes in `lib/` and app-specific glue in `app/models` (`lib/runtime` vs `workers/runner`, #149).
- He prefers native HTML/CSS over JS and components: #60 "Theming without JS", #73 native select "so we can get rid of some components/controllers", #97 native popover ("No reason for this except that I like using native html/css functionality"). ViewComponents in `app/components` are mostly Michelangelo's (6 of 8 files); Paolo uses resource partials.

### Refactor vs feature
- Refactors are their own PRs, or their own leading commits inside a feature PR. He deletes the old path in the same PR once the new path works: #9 "Removing benchmark code"; #133 "Removing LLM module"; #149 "Removing old manifest" and "Dropping workbook"; #77 removed custom claiming; #131 "Removing unused views"; #128 deleted generated `models_controller`.
- He simplifies when complexity annoys him, and says so in the description: #72 ("Tutte le cerimonie e i girotondo attorno al builder e runner mi stavano facendo impazzire", roughly "all the ceremony around the builder and runner was driving me crazy"); #91 ("The guards and checks... were driving me insane").

### Tests
- Mostly model and domain tests with large test files per unit; controller and policy tests for every new resource; LLM stubbed (`with_llm`, "Enforcing stubbed requests" `1ee57c72`); builders via `test/test_helpers/attributes/` (`workers_workflow_attributes`, `create_ready_workers_workflow!`).
- No presentation or browser tests. AGENTS.md says: "Avoid adding presentation or browser tests; verify UI changes in the browser."
- LLM quality is measured by evals outside CI (#85, #115, #145). Results tables go in the PR description (#7 "Task 1 ... PASS", #85 the model/pass/time/cost table).

### Migrations
- Schema-only; no data backfills (AGENTS.md: "Keep development migrations schema-only"). This has bitten them. On #87, Michelangelo noted that existing agents get a nil `lineage_id`, and `db/migrate/20260830091300_add_lineage_fields_to_agents.rb` indeed only adds the column.
- He insists `schema.rb` only changes through migrations. #34: "@minimagate please non fare modifiche a questo file senza migrazioni" ("please don't change this file without migrations"). #67 removes a stray field "there's no migration adding it in the first place, so we can't remove it via one". There are 5 "Fixing schema" commits.
- He prefers reversible `change` migrations (#149 `9c522e6b`).
- He churns the schema freely pre-production (spec sections were added, combined into `spec` with `20260930160000_combine_workflow_spec_sections.rb`, then re-split in #171). Expand/contract happens within one PR (#171).

### Docs
- Design rationale goes in PR descriptions, not in docs files. Commit bodies are rare (about 94 of 930 commits), but when present they explain *why* ("Openrouter is not special and should not get preferential treatment with the env variables", "A table is a table").
- He updates `AGENTS.md`/`README.md` when moving architecture (#149 `bed13c00`, `003ae1b3`) and keeps `evals/README.md` alongside the eval system.

---

## 3. Commit message and PR description style

### Commit subjects (Paolo)
- 2-3 words in about 75% of commits. Gerund-first in about 60% (484 of 814): "Validating shapes", "Renaming runs", "Breaking up builder". Comparative or adjective-first in about 11% ("Simpler slug", "Safer whitelists", "More explicit guards", "Stricter policy checks", "Explicit calls").
- No conventional-commit prefixes (0 of 814).
- Informal and candid: "Type inference?!", "RELOADING THE WORKFLOW", "What", "Stupid gems", "Massive CVE", "Various fixes that I haven't read", "Gotta go fast", "Dumb change to reset GH", "MORE renames".

### Commit subjects (Michelangelo), for contrast
- Median 6 words, imperative sentence: "Run a finished run again with the same input", "Prefer explicit run detail views over clever loops", "Move the run data renderer back to runs".
- 36 conventional-commit subjects (`feat(runs): structure run activity data`).
- Some early terse lowercase subjects ("data instrument", "ui", "local env", "gemma", "login", "fix").

### PR descriptions (Paolo)
- **Opening one-liner of intent:** "Mini type system for some strong validation for the builder." (#6); "Adding a "meta builder" to break down a big task into steps." (#88); "Grouping the `workers` and `sheets` objects into their explicit modules..." (#123).
- **Bullet list of behavioral rules,** often nested: #87 ("Drafts can be destroyed for real; ready agents can only be archived... an agent is "active" if it's the last version _and_ is not archived"); #44 lists one broadcast rule per model.
- **"The point of X is Y" layering explanation** (#24): "The point of the interface in `settings` is to manage the credential models / The point of the credential models is to manage the tokens / The point of the API helpers is... / The point of a tool is... / The point of a tool node is...".
- **Code snippets showing the new API:** `step.with_time_meter do ... end` (#76); `assistant_context :sheets, resource_id: :table_id` (#131); BAD/GOOD template paths (#39).
- **Explicit scope limits:** "Out of scope for this pr, but could reasonably be added at some point" (#87); "To do: [ ]" (#166); "Prossimi step, in ordine" ("next steps, in order", #128); "This is just a convenience page... not meant to be usable in real life" (#9).
- **Results and evidence:** the #7 test output, the #85 eval table, #30 "I went through all the prompts with a bigger model to validate a few things", #90 "The changes I'm making are in response of actual failures I've experienced."
- **Trade-offs stated plainly:** #183 "dry runs will not show partial progress... But at least they do show up"; #47 "The shape system gained a bunch of weight in the process, but I think it's worth it".
- **Language:** English through about #34. From #35 onward he mixes in Italian: #35, #39, #72, #81, #85, #115, #118, #128, #130, #133, #134 and #139 are Italian, while #87, #88, #156, #158 and #183 are English. Headers (`## IF/ELSE`, `## Sort form`) are used when a PR has more than one sub-topic.
- **Humor and frustration are visible:** "Just one task, but 1 >> 0", "Sadly... 🤮", "facciamo finta che ci siano delle possibilità di avere delle collisioni prima della morte termica dell'universo" (roughly "let's pretend there's a chance of collisions before the heat death of the universe").

---

## 4. Habits and mannerisms

| Habit | Strength | Evidence |
|---|---|---|
| Plumbing or skeleton commit first (interfaces, routes, policy, empty views, tests) | **Strong** | `c48c24c4`, `0f1e7944`, `19566262`, `7cd713e1`, `e67c250e`, `2e0b4fa1`, `af03a343` |
| Rename or clean up before adding the concept | **Strong** | #88 `f988cd84`/`d91c2e87`; #29 `44fff0ef`; #6 `e44d660f`; #110 normalization; #108 `a2e95264`; #149 "Renaming runs/revisioner" |
| Bottom-up layer order: schema → model/domain → runtime/builder → prompts → controller → UI | **Strong** | #80, #98, #110, #76, #29, #24 |
| Delete the old path in the same PR | **Strong** | #9, #133 `d2e8ce12`, #149 (manifest, workbook, calls), #77, #131, #128 |
| Verbs as resources, with one policy per action resource | **Strong** | #29, #35, #170 `f13c5c57`, routes on main, review in file A |
| Extract a PORO when a model bloats | **Strong** | #91, #149 "Breaking up builder/runner host", `Workers::Revisioner` |
| Native HTML/CSS over JS and components | **Strong** | #60, #73, #97, #114 ("Enabling nested menus rather than defining a "submenu" concept") |
| Rough UI and solid data, called out explicitly in the description | **Strong** | #9, #98, #110, #128 ("ovviamente è orrenda da vedere", "obviously it's hideous to look at"), #130 ("È ancora brutta", "it's still ugly"), #166 |
| Separate commits for linting, dead code, brakeman and schema fixes | **Strong** | counts in §2 |
| Batch "Testing everything" commit after the skeleton | **Strong** | #29 `304757e6`, #80 `a53ff69a`, #98 `5e7f7448`, #87 `47d90e9e`, #131 "Tests tests tests" |
| Prompt edits isolated in their own commits | **Strong** | #6 `8517a485`, #80 `fe3e669a`/`ee3f0aa5`/`d2498a23`, #88 `28011142` |
| PR chains, roadmap checklist executed in order | **Strong** | #128 → #130 → #131 → #133 |
| Stacked PRs, despite disliking the conflicts | **Strong** | #88, #149, #171, #178, `5ef576e3`, `d68b5e28` |
| Prefer reusing app primitives (shapes, meters, chat helpers) over custom logic | **Strong** | #149 description, `a277aa1d` "Respecting meter interface", `176ec032` "Shape params", #77 |
| Simplify instead of adding concepts (rules on existing nodes vs new node types) | Medium | #80, #72, #114 |
| Pure-move commits separated from edits | Medium (one big instance, motivated by #56) | #123 `a03feb87`, `2fe54b6e`, `6a3cfbd7` |
| Generator command as commit subject | Medium | `ffa65db7`, `c319bd53`, older "rails g authentication", "rails g pundit:install" |
| Expand/contract columns within one PR | Weak | #171 `855249de` → `48c47d24` |
| Reversible `change` migrations with full drop bodies | Weak (single) | #149 `9c522e6b` |
| Empty placeholder file committed, filled later | Weak | #88 `7e16c642` creates an empty `prompts/steps.md`, filled in `28011142` |

---

## 5. Candidate planning rules and review-checklist items

### Planning rules (to emulate Paolo when planning a big feature)
1. **Start with a "prep" slice:** list the renames and cleanups needed so the new concept has a clear name. Do them first, as their own commits (or PR) with no behavior change. *(#88, #29, #110, #6)*
2. **Plan layers bottom-up:** migration+model → domain object or concern (+tests) → integration (runner/builder/jobs) → prompts → controller+policy+route ("plumbing") → UI. Mark UI as minimal or rough unless UI is the point. *(#80, #98, #110, #76)*
3. **Name a "plumbing" commit that fixes the public interface** (class skeletons, routes, policy, controller test) before filling the logic. *(7 plumbing commits)*
4. **Model actions as resources.** Each new verb gets a singular nested resource with its own controller and policy (`resource :build, only: :create`). Do not add custom member routes. *(#29, #35, routes.rb)*
5. **Put state transitions on the model** as `predicate?` + `verb_now!` / `verb_later!`, with a one-line job. *(workflow.rb:119-146, run.rb:41-49, jobs/)*
6. **Decide what gets deleted.** The plan should name the old code path removed in the same PR. *(#133, #149, #77, #9)*
7. **Write an explicit "Out of scope / To do / Next steps (in order)" list** and use it to cut the follow-up PRs. *(#87, #128, #166)*
8. **Split mechanical moves from edits** (pure `git mv` commit, then a module or edit commit) in any namespace or directory change. *(#123, motivated by #56)*
9. **Keep each PR to one capability.** For a large capability, plan a chain of PRs, and prefer independent PRs to stacks where possible: stacking caused repeated conflict pain. *(#178, `d68b5e28`)*
10. **For LLM features:** validation rules with clear messages first, then prompts, then evals outside CI. Report eval numbers in the PR. *(#6, #7, #85)*
11. **Reuse existing app primitives** (Shapes for I/O validation and casting, Meterable for costs, the Chat helpers) rather than bespoke logic. *(#149, #76)*

### Review-checklist items (each tied to evidence)
1. **Nested lookups are scoped through the parent** (`@project.workflows.find`, not `Workflow.find`). *Evidence: Michelangelo's P1 on #56; fixed pattern in `Workflows::BaseController#set_workflow`.*
2. **Every `schema.rb` change has a migration**, and column removals have a removal migration. *Evidence: #34, #56 P2, #67, 5 "Fixing schema" commits.*
3. **New non-null or identity columns on existing tables have a backfill plan**, since migrations are schema-only. *Evidence: #87 nil `lineage_id` comment.*
4. **Policies match the intended role split.** Starting runs and other credit-spending actions check `update?`, not `show?`. *Evidence: #87 comment on run policy.*
5. **Form and param round-trip:** list params use `[]`, optional `?` keys are preserved, and input is cast via Shapes before validation. *Evidence: #47 comments (two bugs), #149 casting comment, #127 "we don't have tests that submit the forms as they are".*
6. **No silent truncation or pagination caps** in tool and data layers. *Evidence: #149 `list_records` limit 50.*
7. **Transactions and rescue paths:** no writes inside an aborted savepoint; rescues use safe log updates. *Evidence: #149 savepoint comment; Paolo's own fix `049d20cb` "Safe log updates in rescues".*
8. **Long work is not run synchronously from a request or tool call** (use `*_later!`). *Evidence: #149 `build_now!` comment; #9 note on blocking threads.*
9. **Avoid side-effect registries that fight Zeitwerk;** prefer an explicit list or `eager_load_dir`. *Evidence: #149 registry comment; #29 `c30f3eec` "Cleaner tool loading".*
10. **Check `dependent: :destroy` chains** for loss of history or audit data. *Evidence: #149 TableRef → calls comment.*
11. **Look for near-duplicate partials** and collapse them with a local. *Evidence: #149 comment on the three call partials.*
12. **Templates live under the resource they render** (`steps/_form`, not `agents/_step_form`). *Evidence: #39.*
13. **Turbo ids use the helpers,** not hand-written magic ids; check permanent elements after broadcasts. *Evidence: #40 "Missing turbo ids (dammit)", #158, file A line 1360.*
14. **N+1 queries and preloading on new list pages.** *Evidence: #40 "Preloading associations", #110 `dcf5c09f`.*
15. **Old path removed and dead code deleted;** brakeman updated. *Evidence: §4 counts.*
16. **Randomness in test or sampling paths still exercises all branches.** *Evidence: #149 deterministic-sampling comment.*

---

### Caveats
- Some commits inside Paolo's PRs are Michelangelo's (#108 first five; #166 about 45 UI commits; #47 `8cbebf7e` and others from the merged `shapes-form-ui`). They are attributed by author above.
- "Michelangelo's style" here is inferred from his commits in shared PRs (#108, #148, #166) and his review comments in the input. His own PR descriptions were not in this input (they are in file A).
- In #166, Michelangelo's commits "Prefer explicit run detail views over clever loops", "Restore per-type call partials" and "Move the run data renderer back to runs" look like responses to Paolo's feedback. That is inferred from the subjects and was not verified against review text.
