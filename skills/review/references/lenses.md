# Review Lenses

## How every reviewer works

- Read the guideline files you were given before reviewing (repo AGENTS.md, CLAUDE.md or equivalent, `rails-*`, `project-*`, `how-we-work`), and neighbouring files when your lens needs them.
- Review only the given diff scope, plus the code it touches.
- Stay in your lens. Do not report what other lenses cover.
- Read-only: do not edit files, run git, run migrations or change state.
- Falsify first: try to disprove each finding by tracing callers, searching for dynamic or external references, and checking for more specific overrides. Drop it if it fails.
- Return findings in the format at the end of this file. No praise, no restating the diff.

## Overengineering

Find machinery the current requirement does not justify, and name the simpler direct form. Apply the Principles section of `how-we-work`.

Look for:
- Options, parameters, hooks, config keys or extension points that no caller uses today.
- Service, wrapper, adapter, decorator, form or query objects that only delegate to one call.
- One-public-method classes where a plain method on an existing object does the job.
- Registries, DSLs, plugin systems or metaprogramming where straight code reads fine.
- Abstractions for hypothetical providers, scale or future reuse; state machines for two states.
- Defensive checks for cases the framework, types or callers already prevent.
- Compatibility shims, aliases or deprecation paths for callers that do not exist here.
- Interfaces with one implementation and no planned second.
- New dependencies (`Gemfile`, `Gemfile.lock`, `config/importmap.rb`, `package.json`) that a small own implementation or existing code could replace.

Not a finding:
- Complexity the requirement demands: concurrency, security, external integration.
- Boundaries and layers the repo already established and uses consistently.
- An abstraction with a real second caller in the repo today.
- Framework-mandated structure, such as required base classes or generated code.
- Preference for a different but equally simple style. Report only when the simpler form is clearly less machinery.

Report: name the machinery, state why the current requirement does not need it, and suggest the simpler direct form. Search for callers and requirements first; drop the finding if a real one exists.

## Over-standardisation

Find sharing and uniformity that couple things which should be free to diverge, and the rare copy that has real drift. This lens is meant to sometimes disagree with overengineering. Report both sides of a tension honestly instead of hedging.

Look for:
- Shared bases, concerns, partials, helpers, components or utilities extracted from two or fewer real callers (rule of three).
- Shared code that gains flags, conditionals or optional parameters to serve its callers.
- Look-alike code from different domains, changing for different reasons or likely to diverge.
- A cross-cutting change forced through one abstraction when each caller needs a different outcome.
- Renames or restructures done only to make things look uniform.
- A "common" or "shared" module that many unrelated places depend on.
- Under-sharing: a copy that now exists three or more times and has started to drift in behaviour.

Not a finding:
- Duplication that costs less than the coupling a shared helper would add.
- Sharing that the framework or repo guidelines require.
- Copies identical by design and expected to change together, when the diff makes that explicit.
- Identical copies with no drift and no third caller.
- Taste about whether a helper should exist, without a concrete divergence or coupling cost.

Report: for over-sharing, name the shared unit, list its callers, and state the concrete divergence or forced flag. For under-sharing, list every copy with its path and the specific drift. Falsify by checking that the callers really diverge or the copies really drift.

## Conventions

Check that the diff follows the rules the repo has written down and the patterns its neighbouring code already uses.

Look for:
- Violations of an explicit rule in AGENTS.md, CLAUDE.md or repo docs, including the `rails-*` and `project-*` skills.
- Naming, file placement or module layout that differs from sibling files without a reason.
- Error handling, logging or return shapes that differ from neighbouring code doing the same job.
- Framework conventions broken without need. Rails: RESTful controllers and routes, strong parameters, thin controllers, model invariants backed by database constraints, Zeitwerk-compatible names.
- A second way to do something the repo already does one way, such as a second HTTP client, job pattern or form pattern.
- Tests that contradict the repo's testing rules: wrong framework, location or forbidden mocking style.
- Commit or PR conventions the repo documents, when the diff includes them.
- New dependencies or a JavaScript build step against the Principles section of `how-we-work` or a repo rule.

Not a finding:
- Personal taste with no written rule and no neighbouring pattern.
- Patterns only in legacy code the repo is moving away from.
- Style the linter or formatter enforces, unless the diff bypasses it.
- A rule the diff does not touch that was already broken.
- Choices the guidelines explicitly leave open.

Report: quote the rule text, or cite the neighbouring file path that sets the convention. Name the convention, show the diff location that breaks it, and state the conforming form. Falsify by checking that the rule still applies to this file and that no more specific document overrides it.

## Cleanliness

Find hygiene problems that the diff adds or leaves behind, and nothing it did not touch.

Look for:
- Dead code added or left behind: unused methods, parameters, variables, imports, constants and routes.
- Leftovers from a superseded implementation: old paths, aliases, always-on feature flags, commented-out code.
- Debug output added: `binding.pry`, `console.log`, `puts`, temporary logging.
- TODO, FIXME, XXX or stray notes without an owner or ticket.
- Unclear or misleading names, and comments that restate the code or no longer match it.
- A missing comment only where a non-obvious why exists and the code would mislead without it.
- Duplicated logic inside the change itself, such as the same block twice in one file.
- Methods or nesting the change made overly long or deep.
- Files added that nothing in the repo references.
- Unrelated edits mixed in: reformatting, or renaming code the feature did not need to touch.

Not a finding:
- Pre-existing mess in lines the diff did not touch.
- Formatting the configured linter or formatter handles.
- A comment explaining a real non-obvious constraint, even if long.
- Code unused in this diff but kept as an intentional public API the repo exports.
- Naming consistent with neighbouring code, even if you would name it differently.

Report: the file, line range and specific artifact. For unused code, show no reference exists by searching the repo, and say what you searched. Falsify by searching for dynamic or external references.

## Correctness

Find code in the diff that produces wrong results, unsafe behaviour or lost data. Prove each one with a concrete scenario.

Look for:
- Logic errors: wrong conditions, inverted checks, off-by-one, operator precedence, wrong status codes or redirects.
- Nil, empty and blank inputs reaching code without a guard on the changed path.
- Missing authentication or authorization on new or changed actions; record lookups not scoped to the current user or tenant.
- Mass assignment of unpermitted attributes, SQL or shell injection, unsafe `html_safe` or raw rendering of user input.
- Secrets or credentials in code, fixtures, logs or configuration.
- Race conditions and missing transactions around multi-step or read-then-write logic.
- Uniqueness enforced only by a validation, with no database unique index.
- Callbacks or jobs with external side effects that run before the transaction commits.
- N+1 queries and unindexed lookups on changed paths.
- Migrations that drop or rewrite data without backfill, or are not reversible when the repo expects reversibility.
- Error paths that swallow failures, or report success after a failed step.
- Tests that would still pass if the changed code were broken, assert only framework behaviour, or skip the new branch.

Not a finding:
- Hypothetical failures with no plausible input or state that reaches them.
- Style, naming, structure or formatting.
- Performance on code that runs once, on tiny bounded data, or outside the changed paths.
- Checks that a framework, type or documented caller contract already guarantees.
- Races already serialised by a lock, a queue or a single worker.

Report: a concrete failing scenario (exact inputs or state, and the wrong output or effect), the faulty file and line range, and for test findings the test that would still pass. Falsify by tracing the scenario through the real path, including callers and validations.

## Structure

Ask the structural questions that reviewers repeatedly block on, and report only where the diff fails one. This is not a style review; formatting belongs to the linter.

Scope:
- Run all 17 questions when the project states mechanisms (`rails-*`, `project-*`). Measure "a second way" against those mechanisms.
- Without stated mechanisms, limit to questions 1, 8–12 and 15.
- Leave abstraction size, hygiene, conventions and bugs to their lenses.

Look for:
1. Is every new branch, rescue, option, flag, JS controller, broadcast, page, config key or log used now? If not, what is it for?
2. Does the diff add a second way to do something the codebase already does (a registry beside a DSL, a caster beside the shared validation layer, hand-written ids beside `dom_id` or the id helper)?
3. Is each action authorized with the right action and policy: no `verify_authorized` skipped, `new` checked as `create?`, no policy re-checked or contradicted elsewhere, no state-changing or charging action guarded only by `show?`?
4. Is a nested record found through its owner's scope, not an unscoped `find`?
5. Do derived data, state predicates and config validation live on the owning model, not in controllers, templates or services that re-validate?
6. Are view/edit switches done via Turbo and explicit server actions, not client JS, Turbo-frame forks or Stimulus branching on a known id or page?
7. Are live updates limited to records that change in the background, not interactive forms?
8. Are routes standard resources (no custom verbs, member routes or slugs), with any conditional operation in `update` split into its own controller?
9. Is a new page needed, or would the existing form do the job?
10. Is structured data stored as rows and real foreign keys, not JSON blobs, parsed markdown or redundant columns?
11. Is each deleted helper, wrapper, nested-attributes call, controller split or shared helper justified as safe to remove?
12. Does a lifecycle change (archive, share, version) or a tool-found quick fix state its intended behaviour?
13. Is behaviour explicit, not thread-locals, `prepend`, tag-keyed YAML, env switches or status symbols callers must `case` on?
14. Is a helper, base class, module, CSS class or ViewComponent used once where a native element or inline class would do, or a mode flag added to a partial?
15. Do tests cover each new page and action branch, without route-recognition tests or leftover tests for a deleted feature?
16. Does the diff bring unrelated `schema.rb` changes, a new dependency, or justification comments on ordinary code?
17. Is a new interface a rough placeholder (missing states, tokens or dark mode) rather than complete under `rails-design`?

Not a finding:
- Formatting, naming taste with no collision, comment wording, small Tailwind visual choices.
- Thin tests on an early slice of a larger feature, when the diff states what follows.
- Known debt the diff names and parks with a stated deferral.
- Small duplication that avoids coupling, or complexity the requirement demands.

Severity: `major` for what the project's reviewers would mark as blocking. Never `blocker`, which is reserved for wrong behaviour, security holes or data loss. `minor` for what should be fixed in this change. `nit` for what can be deferred.

Report: confirm the existing mechanism exists and fits, and that no real caller or requirement justifies the machinery.

## Finding format

Every reviewer returns a list of findings in this format and nothing else.

Fields, in this order:
- `lens`: the short lens name, for example `correctness`.
- `severity`: `blocker`, `major`, `minor` or `nit`.
- `location`: `path:line`.
- `claim`: one sentence stating the problem.
- `evidence`: the specific code or fact that shows it, quoted or referenced.
- `falsification`: what you checked that could have disproven the claim, and why it still holds.
- `suggestion`: the smallest fix, in one or two sentences.

Rules:
- Report only findings you can point to in the diff or in the code it touches.
- Do not raise style opinions that the repo guidelines do not support.
- No praise. Do not restate the diff.
- If there are no findings, reply `No findings` and list what you checked.
- Cap at 15 findings, most severe first.

Severity guide:
- `blocker`: wrong behaviour, security hole or data loss.
- `major`: clear guideline violation, or a structural problem that will cost soon.
- `minor`: worth fixing in this change.
- `nit`: optional.

Example:

```
- lens: correctness
  severity: major
  location: app/services/report_sync.rb:42
  claim: The retry loop re-sends records that already succeeded, so the same item is pushed twice.
  evidence: `retries.each { |rec| push(rec) }` runs over `all_records`, and `push` does not check `rec.synced_at`.
  falsification: `pending_records` filters on `synced_at IS NULL`, but the retry list at line 30 is built from `all_records`, so the filter does not apply.
  suggestion: Build `retries` from `pending_records`.
```
