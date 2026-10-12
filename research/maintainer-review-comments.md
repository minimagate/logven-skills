# The maintainer as reviewer: principles from his review comments

Source: `A-maintainer-comments.md`. It holds about 80 inline comments, 3 review bodies and 2 issue comments, spread over 25 of Michelangelo's PRs (#10 to #159). I read all of it.
Extra context, labelled where used:
- the per-PR JSON in `scratchpad/prs/`, for review states and for Michelangelo's replies;
- The maintainer's own replies on his PRs #56, #81, #87 and #149. In those threads Michelangelo reviewed the maintainer, which is the only place the two argued back and forth;
- the current `config/routes.rb` and `app/controllers` in the logven repo.

Language: the maintainer writes in Italian up to #143 and in English on #159. Quotes are kept in the original. A short English gloss is given where the meaning is not obvious.

Strength labels:
- **[strong]**: 4 or more instances across at least 3 PRs.
- **[medium]**: 2 or 3 instances, or several inside one PR.
- **[weak / one-off]**: a single remark.

---

## 1. Recurring themes, ranked by frequency and weight

### T1. Every line must justify itself. Cut noise, defensive code and speculative branches. [strong, about 15 instances, highest frequency]
**Rule:** don't add code, branches, validations, JS or config that the current feature doesn't need. If it can't answer "a cosa serve?" ("what is this for?"), remove it.
- #37 `steps_controller.rb`: "Troppo rumore per niente qui -- tutti sti if/else in pratica non vengono mai usati" ("too much noise for nothing; these if/elses are never actually used"). He replaced `turbo_frame_request?` branching with a 4-line `render :update / render :edit`.
- #32 `node_run.rb`: "il metodo vecchio aveva già tutta la validazione necessaria. Mi sa stiamo aggiungendo solo rumore qua" ("the old method already had all the validation it needed; I think we're only adding noise here").
- #32 `google_controller.rb`: "Non ci servee questo" ("we don't need this"). The target was respond_to and flash scaffolding.
- #122 `instance_validator.rb`: "(Questo è molto più complicato del ripetere una riga due volte)" ("this is much more complicated than repeating one line twice"). He prefers a small duplication over a yield-based helper abstraction.
- #159 `chat/structured.rb`: on `stop_after_tool:` he wrote "I'm not convinced this requires explicit handling". On `check?` in `workers/run.rb`: "The name is irrelevant, every dry run should behave the same". On `builder/base.rb`: "Why should this matter?"
- Bare "what is this for?" questions: #42 `run_focus_controller.js` ("A cosa serve questo?"), #136 `scroll_container_controller.js`, #140 `toggle_controller.js` `syncTriggersIn`, #65 `node_runs_controller#edit` ("Perché ci serve una pagina apposta?", "why do we need a separate page?"), #23 `broadcast_refresh_later_to` ("Questo serve davvero?", "is this really needed?").

### T2. Authorization is non-negotiable and lives in the policy, as one consistent source of truth. [strong, about 11 instances, highest weight]
**Rule:** never skip Pundit checks. Put each action's rules in its policy method and reuse them in the views. Authorize with the right action and the right policy. Don't re-check what the scope already guarantees, and keep policies consistent with each other.
- #10 `tasks_controller.rb` on `skip_after_action :verify_authorized` (CHANGES_REQUESTED): "L'autorizzazione non si deve mai skippare per nessun motivo al mondo, nessuna eccezione" ("authorization must never be skipped, for any reason in the world, no exceptions"). The repo today skips it only in the unauthenticated controllers (sessions, passwords, oauth_callbacks).
- #23 `step_policy.rb`: "Il pattern sarà mettere qui le regole per ogni azione, e poi usare questi controlli anche nelle views -- tipo il form è disabilitato se i permessi dicono di no" ("the pattern is to put each action's rules here and reuse these checks in the views; e.g. the form is disabled if the permissions say no"). He also wants state-dependent rules: update only while the agent is draft and the step is draft or complete.
- #37 `step_orders_controller.rb`: `authorize @agent, :update?` conflicts with the agent policy, because the order must lock once the agent is ready. "o mettiamo una policy diversa qua. Sarei più per la seconda" ("or we use a different policy here; I'd go for the second").
- #140 `chats_controller.rb#new`: "usiamo l'auth corretta (questo non è `create`)" ("let's use the correct auth; this is not `create`").
- #84 `node_runs_controller.rb`: "`policy_scope` non serve qui -- `authorize` fa già tutto" ("`policy_scope` isn't needed here; `authorize` already does everything"). In `node_run_policy.rb`: "controllano le stesse cose più volte" ("they check the same things several times"), "`AgentPolicy` è il salto sbagliato" ("`AgentPolicy` is the wrong hop"). In `step_policy.rb`: "queste sono incongruenze che a un certo punto ci puniranno" ("these are inconsistencies that will punish us at some point").
- #65 `agent_runs/_card.html.erb` and `_row.html.erb` on `policy(run).show?`: "Questo è vero per definizione, sennò non vedremmo nemmeno la card" ("this is true by definition, otherwise we wouldn't even see the card"). Don't test conditions the page already guarantees.

### T3. Put logic where it belongs: domain methods on models, each responsibility in the object that owns it. [strong, about 10 instances]
**Rule:**
- Derived data and state queries become model methods (or associations), not controller locals or template logic.
- Validation lives in the object that owns the configuration.
- Service objects stay dumb.
- Helpers, templates and components must not spread one concern across layers.

Evidence:
- #32 `agents_controller.rb#load_show_data`: "Questi dovrebbero essere tutti metodi dell'agente" ("these should all be methods on the agent").
- #32 `step.rb` rescue block: "Questo magari lo spostiamo nel builder" ("maybe we move this into the builder").
- #42 `_step_run.html.erb`: "`StepRun` ha il suo stato, non c'è bisogno di guardare i nodi. (e magari `active?` potrebbe essere un metodo su `StepRun`...)" ("`StepRun` has its own state, no need to look at the nodes; maybe `active?` could be a method on `StepRun`").
- #84: replace hand-written joins with `has_many :step_runs, through:` and `has_many :node_runs, through:`, then `@project.node_runs.find(params[:id])`.
- #106 `nodes/data.rb`: "La configurazione si valida qui, non nelle actions -- è responsabilità del nodo sapere come configure se stesso. Le azioni sono solo service objects ... non sanno nemmeno che i nodi esistono" ("configuration is validated here, not in the actions; it's the node's job to know how to configure itself; actions are just service objects and don't even know nodes exist").
- #106 `runner/data.rb`: "Non c'è nulla da validare qua -- ci aspettiamo che i nodi siano validi a questo punto" ("nothing to validate here; we expect the nodes to be valid by now"). This is "validate at the boundary, then trust".
- #159 `table_caller.rb`: "This belongs in the type system -- we should have a `strict` version of the instance validator".
- #109 `application_helper.rb#run_table_row`: a template feeds a helper, which builds a hash, which a component reworks. "lasciamo che sia il component a smazzarsela, oppure facciamo gli helper per tutto ed evitiamo di sparpagliare la logica" ("let the component handle it, or make helpers for everything and stop scattering the logic").

### T4. The server drives the UI. Use Turbo and explicit server actions. JS is the last resort. [strong, about 6 instances]
**Rule:**
- View/edit switching, validation round-trips and state updates go through Turbo and controller actions, not client-side JS.
- Broadcasts are for background updates (runs, build phases), not for interactive cards.
- Don't add JS libraries for content the backend already renders.

Evidence:
- #32 `edit_step_controller.js`, marked "(Importante)": "se vogliamo avere bottoni per cambiare tra scheda e form nella stessa pagina, lo facciamo tramite turbo e azioni esplicite ... è il backend che valida tutto" ("if we want buttons to switch between card and form on the same page, we do it through Turbo and explicit actions; the backend validates everything"). Michelangelo then wrote #37 "Client side -> Server side step editing".
- #42 `run_focus_controller.js`: "dovrebbero potersi chiudere/aprire da sole senza JS o controlli strani" ("they should be able to open and close on their own, without JS or odd checks").
- #37 `step.rb` broadcast: "questi broadcast sono utili principalmente per le run che vengono aggiornate dietro le quinte, o durante le fasi di build e basta" ("these broadcasts are mainly useful for runs updated behind the scenes, or during build phases, and that's it"). #23 also questioned a `broadcast_refresh_later_to`.
- #136 `importmap.rb` (dompurify, marked): "quando tutto il testo arriva dal backend non dovrebbe esserci bisogno di alcun js" ("when all the text comes from the backend there should be no need for any JS"). He would rather explore Lexxy.

### T5. Stimulus controllers stay generic and composable, with no knowledge of specific elements. [strong, 4 instances in 4 PRs]
**Rule:** a Stimulus controller does one generic behaviour that forms compose. Never branch on a known id or page, and never hard-code feature-specific constants.
- #37 `sortable_controller.js`: "La separazione tra `autosave` e `sortable` era voluta: sono due azioni separate che possiamo comporre nei singoli form" ("splitting `autosave` and `sortable` was deliberate: they are two separate actions we can compose in each form").
- #136 `toggle_controller.js`: "ogni volta che ci troviamo a scrivere `if (id === "...")` in js ... significa che siamo sulla strada sbagliata" ("whenever we find ourselves writing `if (id === "...")` in JS, we are on the wrong road").
- #109 `sidebar_controller.js`: "Queste continuano a essere cose super specifiche nei controller che dovrebbero essere generici" ("these are still very specific things inside controllers that should be generic").
- #140 `toggle_controller.js` `syncTriggersIn`: "A cosa serve questo?" ("what is this for?").

### T6. Standard RESTful resources: no custom verbs, no slugs, nothing "clever". [strong, 4 instances in 3 PRs]
**Rule:** model actions as nested resources with standard actions, using plain id URLs. If an operation doesn't fit, give it its own controller rather than a member verb or a conditional inside `update`.
- #32 `routes.rb`, marked "(Importante)": "Queste dovrebbero essere risorse esplicite, non verbi a caso" ("these should be explicit resources, not random verbs"). He proposed `resources :node_runs, only: %i[update]` nested under agent_runs. He also reframed the domain: a run isn't "resumed"; its paused node is completed.
- #46 `routes.rb`: "Vedo routes non standard qui ☠️ ... limitiamoci alle url standard con gli id -- niente slug o altre cose furbe" ("I see non-standard routes here ☠️ ... let's stick to standard id URLs; no slugs or other clever things").
- #65 `agents_controller.rb#update` on a conditional project transfer: "Al massimo potremmo avere un controller dedicato per i trasferimenti" ("at most we could have a dedicated controller for transfers"). #37 makes the same point: other pages "funzionerebbero comunque meglio con un controller diverso" ("would work better with a different controller anyway").
- The current `config/routes.rb` follows this throughout: `resource :build`, `resource :commit`, `resource :revision` and `resource :rerun` with `only: %i[create]`, instead of member verbs.

### T7. Before removing or restructuring something, understand why it was there. [medium-strong, 5 instances]
**Rule:** existing structure is often deliberate. Check its purpose (or ask) before deleting it, and don't replace it with something that drops the original intent.
- #37 `agent.rb`, removed `accepts_nested_attributes_for :steps`: "Questo qua serviva appunto a evitare logica apposta per il `reorder` 🧐" ("this was there exactly to avoid special-case logic for `reorder` 🧐").
- #37: the separate autosave and sortable controllers "era voluta" ("was deliberate").
- #74 `application_helper.rb`, removed `svg_tag`: "Lo scopo di questo era gestire gli svg nello specifico, mettendoli inline ... Con `icon_tag` si perde il senso di tutto" ("the purpose was to handle SVGs specifically, inlining them ... with `icon_tag` the whole point is lost").
- #99 `_app_header.html.erb`, removed a wrapper div: "Questo serviva:" ("this was needed:"), with a screenshot of the regression.
- #23 `agents/show.html.erb`, partitioning steps: "Gli step hanno un ordine logico, e se li partizioniamo perdiamo il filo no?" ("steps have a logical order; if we partition them we lose the thread, no?").

### T8. CSS: Tailwind utilities inline in the template. Use a shared CSS class only for a real reusable primitive. No bespoke stylesheets or arbitrary values. [medium-strong, 4 instances in 3 PRs]
**Rule:** classes used once go inline in the partial. A truly reused visual primitive, such as a badge, becomes a small `@apply` class rather than a ViewComponent. Don't invent one-off shadows or colours. For markdown, start from Tailwind `prose`.
- #136 `assistant.css`: "Questi son tutti stili indipendenti che verranno usati una volta sola ... Tanto vale tenerli inline ... Forse perdiamo alcuni dettagli sulle ombre e colori. Meglio. Non dovremmo avere questi stili arbitrari" ("these are independent styles that will be used exactly once ... might as well keep them inline ... maybe we lose some shadow and colour details. Better. We shouldn't have these arbitrary styles").
- #140 `assistant.css`, a second time: "Questo non è un componente, sono tutte classi usate esattamente una volta" ("this isn't a component; these are all classes used exactly once").
- #32 `status_badge_component.rb`: "Tutto questo component potrebbe essere una classe CSS -- non succede niente qui dentro" ("this whole component could be a CSS class; nothing happens in here"). He proposed `.badge` / `.badge.blue`, which was adopted: #83 shows `badge badge-<%= tone %>`.

### T9. Components and abstractions must earn their keep. Prefer native elements and plain partials. [medium, 4 instances]
**Rule:** don't create a ViewComponent, a custom widget or a mode flag when a native element, a CSS class or a plain partial does the job.
- #58 `select_component.rb`: "Perché tutto questo invece di un `select` nativo?" ("why all this instead of a native `select`?").
- #32 StatusBadgeComponent: "non succede niente qui dentro" ("nothing happens in here").
- #109 run table component: "un componente super specifico che in generale non dovrebbe nemmeno esistere 🤪" ("a super-specific component that shouldn't even exist 🤪"). On an SVG-drawing helper he replied only "🤮".
- #99 `shapes/_fields.html.erb`, a `compact:` local: "Non mi fa impazzire il fatto di avere altri flag che trasformino tutto" ("I'm not keen on more flags that transform everything"). It was also forced to `false` further down, and it broke nested types.

### T10. Turbo DOM ids come only from `turbo_id` methods. No hand-written id strings. [medium, 2 explicit comments, flagged as "vale dappertutto", i.e. "applies everywhere"]
**Rule:** use `Model.turbo_id` or `record.turbo_id` (defined in `ApplicationRecord#turbo_id`) for every Turbo target. No magic id strings.
- #136 `reset.turbo_stream.erb`: "evitiamo gli id magici così, che son facili da sbagliare e perdere per strada" ("let's avoid magic ids like this; they're easy to get wrong and lose along the way").
- #140 `new.turbo_stream.erb`: "Non aggiungiamo id a caso -- teniamo solo i vari metodi turbo_id ... (Ci sono anche altri id in questa pr, questo commento vale dappertutto)" ("let's not add random ids; only the turbo_id methods ... (there are other ids in this PR too; this comment applies everywhere)").
- The same comment chain also asked to merge identical templates: "Reset e new sono identici -- facciamo in modo di poter tirar via `reset`" ("reset and new are identical; let's make it possible to drop `reset`").

### T11. The type system (Shapes) must be unambiguous, really validate, and never raise. [medium-strong, 5 instances in 3 PRs]
**Rule:**
- A shape representation must have exactly one reading.
- Validators must check the actual format (ISO 8601 and so on), not just `is_a?(String)`.
- Casting and validation return errors and never raise.
- Structural checks such as unknown keys belong in the validator, not in callers.

Evidence:
- #112 `shapes/base.rb#enum_descriptor?`: "gli enum non possono introdurre ambiguità" ("enums must not introduce ambiguity"). He gave a concrete counter-example and proposed an alternative syntax.
- #122 `instance_validator.rb`: "Eh ma va fatta davvero la validazione però 🤪" ("yes, but the validation has to actually be done 🤪").
- #122 `cast_test.rb`: "Nope, niente nel type system dovrebbe mai causare un'eccezione" ("nope, nothing in the type system should ever raise an exception").
- #159 `table_caller.rb`: a `strict:` option on `valid_instance?`, "If we find this is important in general, it might even be the default".
- #129 (issue): validation and inference duplicate checks, and he suggested "una miniclasse per ogni tipo" ("a mini-class per type") later. "Ho messo un TODO e amen ... Ma non oggi! Andiamo avanti." ("I added a TODO and that's that ... but not today! Let's move on.") A repo commit later followed through: `ccee064e Sharing inference/validation logic`.

### T12. Think through product and domain semantics before coding the fix. [strong, about 8 instances; review bodies carry the most weight]
**Rule:** a change must come from a clear model of how the feature should behave, covering archived states, sharing, who sees what and versioning. Don't patch symptoms such as a bug Codex found. Bring a plan.
- #84 review body (CHANGES_REQUESTED): "il punto non era il 'bug' (?) trovato da Codex, ma ragionare su come vogliamo davvero che funzionino gli agenti archiviati. Ci serve un piano concreto, non un fix al volo" ("the point wasn't the 'bug' (?) Codex found, but thinking through how we actually want archived agents to work. We need a concrete plan, not an on-the-fly fix"). He then listed the open questions himself.
- #84 `node_run_policy.rb`: "le run in corso ormai son partite. Archiviare un agente non le blocca" ("runs in progress have already started; archiving an agent doesn't stop them").
- #65 `agent_run_policy.rb`: "In un progetto condiviso mi aspetterei di avere anche run condivise più spesso che no" ("in a shared project I'd expect runs to be shared more often than not").
- #37 `_show.html.erb`: "`expired?` è un check che facciamo internamente ... non richiede azioni" ("`expired?` is a check we do internally; it needs no action"). Don't surface internal states that need no user action.
- #83: node usage doesn't belong in the run view. He also suggested making the meters collapsible and collapsed by default.
- #106 `get_records.rb`: "all'atto pratico come si usano negli agenti?" ("in practice, how are these used by the agents?").
- #46 `project_membership.rb`: roles are fine as presets, but expect granular per-action permissions later. "Per ora va bene così -- food for thought" ("fine for now; food for thought").
- #87 (his own PR): "read only" means you can't change the project, but you can use it (start runs).

### T13. Data modelling: real foreign keys, ids in the DB and names at the interface, no redundant columns. [medium, 4 instances]
**Rule:**
- Store references as real FKs and ids, and translate to human names at the boundary (for example in `body=` / `body`).
- Drop columns that duplicate an existing concept.
- Navigate with `has_many :through`.
- Reuse existing representations (`record_shape`) instead of adding parallel ones.

Evidence:
- #106 `nodes/data.rb`: "se aggiungessimo una foreign key vera ai nodi per attaccarsi alle tabelle farebbe comodo ... tradurre nomi e id in modo da esporre solo nomi sensati e salvare solo id precisi" ("a real foreign key from nodes to tables would be handy ... translate names and ids so we expose only sensible names and store only precise ids").
- #106 `sheet.rb#data_schema`: "Abbiamo già `record_shape` per tutto questo" ("we already have `record_shape` for all of this").
- #46 `project.rb` `belongs_to :created_by`: "forse questo belongs_to è ridondante -- per definizione chi crea un project si cucca il ruolo `owner`" ("this belongs_to is probably redundant; by definition whoever creates a project gets the `owner` role").
- #84: `has_many :through` chain on Project.
- #149 (his own PR): "Tables are meant to be soft deleted. Hard deletes are reserved for actual data purging".

### T14. Tests: cheap smoke coverage of every page and branch. No tests that duplicate other coverage. [medium, 3 instances]
**Rule:** each controller gets at least one test per page and one per branch of each action (valid and invalid), even if it's only `get path; assert_response :ok`. Don't write route-recognition tests. For LLM evals, prefer per-case tests with assertions on the final output.
- #58 `project_memberships_controller_test.rb`: "almeno uno per pagina ... e idealmente almeno uno per branching delle singole azioni ... È il tipo di test che avrebbe trovato il template mancante" ("at least one per page ... and ideally at least one per branch of each action ... it's the kind of test that would have caught the missing template").
- #23 `routes_test.rb`: "Questi test non servono assolutamente a niente -- stiamo già testando che le routes funzionano ... in tutti i test dei controller" ("these tests are completely useless; we already test the routes work in all the controller tests").
- #143 `project_prompt_eval.rb`: "sarebbe bello definire un test apposta per ogni prompt ... mettere delle asserzioni sull'output finale" ("it would be nice to define a dedicated test for each prompt ... and put assertions on the final output").

### T15. A single source of truth, and no brittle heuristics over it. [medium, 3 instances, all in #159]
**Rule:** pick one authoritative source (here: the generated code, for tool and table references). Don't cross-check it against a softer source with regexes or keyword lists.
- #159 `builder/analyze.rb`: "This is completely backwards. The entire point of this is that the code is the source of truth ... Do we have any actual reason to believe that the specs are more accurate".
- #159 `spec_data.rb` (a verb-synonym regex): "This is one synonym away from breaking the builder".
- #159 `builder/check.rb`: "We include the seed note in the errors? Doesn't this automatically fail the attempt?"
- Related, from his own PR #149: "We either do random or we don't ... reliance on arbitrary seed rules doesn't work".

### T16. Naming: no collisions with existing concepts, and short, precise names. [medium, 2 instances]
- #100 `base.rb` (renaming Sheet to Base): "Stiamo già usando `Base` altrove con un significato diverso -- mi sa dobbiamo cambiare direzione" ("we already use `Base` elsewhere with a different meaning; I think we need to change direction").
- #106 `data_instrument/base.rb`: "Stiamo usando `action` un po' ovunque" ("we use `action` pretty much everywhere"). He proposed `SheetActions::Create/Get/List/Update/Destroy` and config names `create, get, list, update, destroy`.
- #106 `create_record.rb`: "Niente parametri, e niente `self`" ("no parameters and no `self`"). He prefers instance methods on an object built with its collaborators (`initialize(user:, sheet:)`) over class methods taking a configuration hash.

### T17. Repo, environment and dependency hygiene. [medium, several unrelated one-offs grouped]
- #74 `db/schema.rb` (an unrelated column slipped in): "Bisogna guardare cosa mettiamo nei commit ☠️" ("we need to watch what we put in commits ☠️"). Supporting context from #56 (his PR): the column came from no migration.
- #136 `ruby_llm.rb`, loading `.env.local` in an initializer: "Non ha senso inventarsi un metodo per caricare l'env apposta per quest'app ... ancora meno senso implementare sta cosa in un initializer a caso 🤪 ... (A me piace direnv)" ("it makes no sense to invent an env-loading method just for this app ... even less in some random initializer 🤪 ... (I like direnv)").
- #136 `llm/chat.rb`: "c'è una pr aperta che cancella questo modulo" ("there's an open PR that deletes this module"). Check in-flight work before touching a module.
- #136 importmap pins: dependencies get questioned, and alternatives explored, before they're added.
- #32 webp icons and #74 svg/png mix: he wants consistent SVG icons that can be styled inline. Both are weak, aesthetic remarks.

### T18. Numeric and formatting correctness. [weak, a single PR, but detailed]
- #83 `meter_helper.rb`: integer division truncates ("`1020` e `1900` mostrano entrambi `1s`", "both show `1s`"). He wants more precision and wrote a compact alternative ("non l'ho testato 🤪", "I haven't tested it 🤪"). The cost currency is probably USD (OpenRouter), not €.

---

## 2. His bar: what he flags and what he lets pass

**What triggers a comment, roughly in order:**
1. Authorization gaps or inconsistencies. These are the only CHANGES_REQUESTED besides #84.
2. Code that doesn't need to exist: noise, unused branches, unexplained JS.
3. Architecture going the wrong way: client-side JS instead of Turbo, custom routes, logic in the wrong layer, feature-specific generic controllers.
4. Deleting something whose purpose wasn't understood.
5. Domain and product semantics that weren't thought through.
6. Type-system rigor.

**Severity signalling:**
- He labels blockers explicitly, with "(Importante)" (#32).
- He separates blockers from minor notes in the review body: "Ho lasciato un po' di commenti a caso più o meno trascurabili, ma un paio (quelli segnati 'importante') vanno risolti qua" ("I left a few more-or-less negligible comments, but a couple, the ones marked 'importante', must be fixed here").
- Many notes are explicitly deferred: "magari a un certo punto", "food for thought", "Per ora va bene così", "Ma non oggi!" ("maybe at some point", "food for thought", "fine for now", "but not today!").

**Review outcomes:**
- He approves with open comments quite often (#23 approved with 4 comments; #58, #83 and #99 approved after a COMMENTED round).
- Many PRs are approved with no comments at all: #5, #14, #38, #41, #53, #64, #78, #168, #181.
- CHANGES_REQUESTED appears only twice: #10 (an authorization skip) and #84 (confused intent, "Mi sembra ci sia un po' di confusione qui, sia nel codice in sé che nelle intenzioni", "there seems to be some confusion here, in the code itself and in the intentions").

**What he lets pass (no comments seen on these):**
- Formatting and Ruby style. The repo runs `standard` / `standardrb`, so the linter presumably covers it (inference).
- PR descriptions that say "Testing: Not run".
- AI-generated UI-heavy PRs, as long as the architecture is right.
- Thin test coverage on early PRs (#46 says "Test coverage is minimal cause it's boring" and drew no test comment; he raised tests later, in #58).
- Small Tailwind visual choices.

He doesn't nitpick variable names, line length or comment wording. Every comment is about structure, necessity or behaviour.

**Tone:**
- **Questions are the dominant mode**, often rhetorical and Socratic: "Siamo sicuri?", "A cosa serve questo?", "Perché tutto questo invece di...?", "Why should this matter?" ("are we sure?", "what is this for?", "why all this instead of...?").
- **Short directives when he's sure:** "Questo va tolto", "No --", "Nope", "Non ci serve questo", "This is completely backwards" ("this has to go", "no", "nope", "we don't need this").
- **Suggestion code is frequent:** routes, controller bodies, model associations and validators, often marked untested ("non l'ho testato 🤪", "o qualcosa del genere", "I haven't tested it", "or something like that").
- **Emoji for tone:** ☠️ for bad practice, 🤪 for over-engineering, 🤮 once for hand-drawn SVG paths in a helper, 🤔 for open doubts. Direct but friendly.
- He reasons from principles and often generalises one comment into a rule: "ogni volta che ci troviamo a scrivere `if (id === "...")`... siamo sulla strada sbagliata" ("whenever we find ourselves writing `if (id === "...")`, we're on the wrong road"), "questo commento vale dappertutto" ("this comment applies everywhere").

---

## 3. Code-shape preferences by area

| Area | Preference | Evidence | Strength |
|---|---|---|---|
| Routes | Standard `resources`, nested resources for sub-entities, `only:` lists, singular resources instead of member verbs, plain ids | #32, #46, #65, current routes.rb | strong |
| Controllers | Thin. Load, authorize, `if update → render :update else render :edit, status: :unprocessable_entity`. No `turbo_frame_request?` forks. A separate controller for a different operation. Params via one `*_params` method, kept in sync between new and create | #37, #65, #140 | strong |
| Authorization | Pundit everywhere, never skipped. Rules per action in the policy, state-aware. Reuse `policy(...)` in views to disable forms. Delegate to the closest related policy. No duplicate checks. No `policy_scope` when `authorize` plus association scoping covers it | #10, #23, #37, #84, #140 | strong |
| Models | Own derived data and state predicates (`active?`, tools of an agent). `has_many :through` for navigation. Validate own configuration (`validate :validate_body`). Translate names and ids at the accessor boundary. Errors handled where the operation lives (builder) | #32, #42, #84, #106 | strong |
| Service objects | Plain objects built with their collaborators (`new(user:, sheet:)`), instance methods, no knowledge of callers, no re-validation of already-valid input | #106 | medium (one PR, several comments) |
| Views and partials | Minimal logic. No re-checking of conditions guaranteed by context. Don't partition or reorder domain-ordered collections. No mode flags that transform a partial | #23, #42, #65, #99 | medium |
| Components | Skeptical. Native HTML first, CSS class second, ViewComponent only when there's behaviour | #32, #58, #109 | medium |
| CSS | Tailwind inline. `@apply` classes only for real primitives (badge). No arbitrary one-off styles. `prose` for markdown | #32, #136, #140 | medium-strong |
| JS / Stimulus | Minimal. Generic, composable controllers. No element-specific branches or constants. Server and Turbo handle state | #32, #37, #42, #109, #136, #140 | strong |
| Turbo | Ids via `turbo_id`. Broadcasts only for background-updated things. Explicit turbo_stream templates. No duplicate stream templates | #23, #37, #136, #140 | medium-strong |
| Tests | Smoke test per page and per action branch. No route tests. Assertions on outputs for evals | #23, #58, #143 | medium |
| Migrations / schema | Only intended changes in `schema.rb`. Soft delete for domain entities | #74, (#56, #149 own PRs) | weak-medium |
| Error handling | The type system never raises. Validate once at the boundary, then trust. Rescue narrowly (`rescue Date::Error`). No extra error plumbing (`completion_error`, `NotPaused`) when the existing guard suffices | #32, #106, #122 | medium |
| Duplication vs abstraction | Accepts small duplication over clever helpers (#122). Wants duplicate templates merged when truly identical (#136). On his own PR he defends near-copy partials that "will drift by design" (#149) | #122, #136, #149 | medium (nuanced) |
| Dependencies / config | Question new JS deps. No app-specific env loaders, since the environment is the developer's concern (direnv). No provider-specific references in generic modules | #136 | weak-medium (one PR) |
| Code comments | No direct stance. In #159 he challenged the logic that long explanatory comments justified, not the comments themselves | #159 | weak, no rule |
| Naming | Avoid names that collide with existing concepts (`Base`) or overloaded words (`action`). Short config verbs | #100, #106 | medium |

---

## 4. Pushback and changes of mind

**Michelangelo pushing back on the maintainer's comments on Michelangelo's own PRs:** none appears in the data. Michelangelo's only replies there are 👍🏻 or explanations of intent: #17 ("questa ui l'ho fatta con codex perchè... volevo capire meglio insieme", "I made this UI with Codex because I wanted us to work it out together"), #5, #44. Michelangelo complies, often with a follow-up PR (#32 → #37 moved editing to the server, #122 → #129).

**The maintainer defending his choices when Michelangelo reviewed the maintainer's PRs** (outside the input file; useful for his reasoning):
- #87: Michelangelo suggested members shouldn't start runs. The maintainer replied that "read only" means you can't change the project but you can use it. Michelangelo: "okok nice". On a lineage backfill migration: "We have no agents anywhere, and we keep blasting the dev db" (pragmatism: no backfills before production data exists).
- #149, six replies:
  - "Fetching all the records by default is insane. We should assume these tables to be massive."
  - "Tables are meant to be soft deleted".
  - Near-duplicate partials "will drift by design".
  - "We either do random or we don't".
  - build_now vs build_later: "build_later is just broken right now" (pragmatic over theoretical).
  - "Already fixed".
- #56: he rejected a focus-restoration finding: "Tabbing works just fine in practice." He trusts observed behaviour over hypothetical findings.

**Possible change of mind (moderate confidence):**
- #46: the maintainer suggested a top-level `agents` resource with a project dropdown in the agent form, "Questo ci darebbe anche modo di spostarli facilmente" ("this would also let us move them easily").
- #65: when Michelangelo implemented project_id changes inside `AgentsController#update`, the maintainer said "Questo va tolto -- nel contesto più 'grosso' dei progetti in realtà non ha senso cambiare il project_id insieme ai dettagli" ("this has to go; in the bigger context of projects it makes no sense to change project_id together with the details").
- The final routes nest everything under `projects` (`scope module: :projects`).
- So his #46 "top-level agents" idea was dropped. The constant part is "no slugs, standard resources".

**Self-acknowledged deferral:** #129, "Ho messo un TODO e amen ... Ma non oggi!" ("I added a TODO and that's that ... but not today!"). He accepts known debt when it's named and parked.

---

## 5. Candidate review-checklist items

Items marked (S) are backed by multiple instances. Items marked (W) are weak or one-off and should be phrased as "consider".

1. (S) **No skipped authorization.** No `skip_after_action :verify_authorized` / `verify_policy_scoped` in authenticated controllers. #10
2. (S) **Right policy, right action.** Each `authorize` names the actual action (`new?` is not `create?`). Operations with different rules get their own policy rather than reusing `update?`. Policies don't contradict each other. #37, #84, #140
3. (S) **Policy rules are state-aware and reused in views.** The form is disabled when the policy says no. No view re-checks what context guarantees (`policy(run).show?` inside a list of runs). #23, #65
4. (S) **No redundant scoping.** Use association scoping (`@project.node_runs.find`) plus `authorize`, not ad-hoc joins plus `policy_scope`. #84
5. (S) **Justify every addition.** For each new branch, rescue, flag, JS controller, broadcast, page or config: is it used now? If not, cut it. #23, #32, #37, #42, #65, #136, #140, #159
6. (S) **Standard REST.** No member verbs, no custom route strings, no slugs. Model actions as nested or singular resources with standard actions. #32, #46, current routes.rb
7. (S) **Thin controllers.** A single success/failure render path. No `turbo_frame_request?` forks. Data loading moves to model methods. #32, #37
8. (S) **Logic lives in the owning model.** State predicates on the model whose state it is (`StepRun#active?`). Config validation in the configurable object. Services don't re-validate. #42, #106, #159
9. (S) **Server-driven UI.** View/edit toggles and validation go through Turbo and controller actions. Broadcasts only for background-updated records (runs, builds). #32, #37, #42
10. (S) **Generic Stimulus.** No `if (id === "...")`, no page-specific constants or keys in shared controllers. Behaviours stay composable (autosave plus sortable). #37, #109, #136, #140
11. (M) **Turbo ids only via `turbo_id`.** No literal DOM ids in turbo_stream templates or partials. #136, #140
12. (M) **CSS.** Single-use styles go inline as Tailwind utilities. No `components/*.css` for one feature. No arbitrary shadows or colours. Reusable primitive means an `@apply` class, not a ViewComponent. #32, #136, #140
13. (M) **Native first.** Native `<select>` and HTML elements before custom components. No mode flags (`compact:`) that transform a partial. #58, #99, #109
14. (M) **Don't delete what you don't understand.** If the diff removes a helper, wrapper, `accepts_nested_attributes_for` or a controller split, state why it existed and why it's safe to remove. #37, #74, #99
15. (M) **Type system.** Representations are unambiguous. Validators check the real format. Nothing in Shapes raises. Structural strictness lives in the validator. #112, #122, #159
16. (M) **Data model.** Real FKs and ids in storage, names at the interface. No column duplicating an existing concept (`created_by` vs owner role). Reuse existing representations (`record_shape`). #46, #106
17. (M) **Controller tests.** At least one request per page and one per action branch (valid and invalid). No route-recognition tests. #23, #58
18. (M) **Product semantics first.** For lifecycle changes (archive, version, share), write down the intended behaviour before coding. Don't ship a "quick fix" for a tool-found bug. #65, #84, #87
19. (M) **One source of truth.** No regex or keyword heuristics checking an authoritative source against a softer one. #159
20. (M) **Naming.** New class or module names don't collide with existing ones (`Base`) or overloaded words (`action`). #100, #106
21. (W) **Clean diff.** `schema.rb` contains only changes from this PR's migrations. Nothing unrelated is committed. #74
22. (W) **Env and deps.** No custom `.env` loaders in initializers. New JS deps are justified (could the server render it?). Don't edit modules that an open PR is deleting. #136
23. (W) **Prefer instance methods on objects built with their collaborators** over `self.` methods taking a config hash. #106
24. (W) **Formatting helpers keep precision** (no silent integer truncation). Units match the data source (USD from OpenRouter). #83
25. (W) **Don't surface internal states that need no user action** (an OAuth `expired?` badge). Keep secondary metrics collapsed by default. #37, #83
26. (W) **Evals assert outcomes,** with one test per prompt and assertions on the final output, not just "it didn't crash". #143
27. (Meta) **Mark severity.** Blocking comments are labelled ("Importante"). Deferred ideas are labelled as such ("food for thought", "non oggi", i.e. "not today"). A reviewer persona should do the same. #32, #46, #129
