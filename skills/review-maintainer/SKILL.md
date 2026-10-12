---
name: review-maintainer
description: Use when reviewing a diff against the bar of Logven's lead reviewer: necessity, no parallel mechanisms, authorization, ownership of logic, server-driven UI, REST. Covers only that maintainer bar.
---

# Review Maintainer

Ask the questions the lead reviewer repeatedly asks of Logven code, and report only the places where the diff fails one of them.

## Scope

- This lens covers only the maintainer's bar: the structural questions the lead reviewer repeatedly blocks or questions.
- Leave abstraction size to review-overengineering and review-over-standardisation, hygiene to review-cleanliness, written-guideline compliance to review-conventions and bugs to review-correctness. Do not report their findings.
- Not a style reviewer: formatting is covered by the linter, so do not comment on it.
- Review only the diff scope you were given, plus the code that the diff touches.

## What to look for

1. Is every new branch, rescue, option, flag, JS controller, broadcast, page, config key or log used now? If not, what is it for?
2. Does the diff add a second way to do what the codebase already does, such as a registry beside the tools DSL, a generic call beside a specific one, a caster beside Shapes, metering beside `Meterable` or hand-written ids beside `turbo_id`?
3. Does each action get authorized with the right action and policy? Is `verify_authorized` skipped in an authenticated controller, is `new` checked as `create?`, is a policy re-checked in a view, controller or validation, do two policies contradict each other, or is a state-changing or credit-spending action guarded only by `show?`?
4. Is a nested record found through its owner's scope rather than an unscoped `find`?
5. Do derived data, state predicates and config validation live on the owning model, rather than in controllers, templates or services that re-validate?
6. Is view/edit switching or validation done through Turbo and explicit server actions, rather than client-side JS, Turbo-frame forks or a Stimulus controller that branches on a known id or page?
7. Are broadcasts limited to background-updated records, rather than interactive cards?
8. Are routes standard resources, with no custom verbs, member routes or slugs, and is a conditional operation inside `update` split into its own controller?
9. Is a new page needed, or would the existing form do the job?
10. Is structured data stored as rows and real foreign keys, rather than JSON blobs, parsed markdown or redundant columns?
11. Is each deleted helper, wrapper, nested-attributes call, controller split or `svg_tag` justified in the diff as safe to remove?
12. Does a lifecycle change (archive, share, version) or a tool-found quick fix state its intended behaviour?
13. Is behaviour explicit, rather than thread-locals, `prepend`, YAML keyed by tag, env switches or status symbols that callers must `case` on?
14. Is a helper, base class, module, CSS class or ViewComponent used only once where a native element or inline class would do? Is a mode flag added to a partial?
15. Do the tests cover each new page and action branch, without route-recognition tests or leftover tests for a deleted feature?
16. Does the diff bring unrelated `schema.rb` changes, a new dependency or env loader, edits to a module another open PR deletes, or justification comments on ordinary code?
17. Is a new interface a rough placeholder (missing states, tokens or dark mode) rather than a complete one that follows `../rails-design/SKILL.md`?

## What is NOT a finding

- Formatting, naming taste with no collision, and comment wording.
- Thin tests on an early slice of a larger planned feature, when the diff states what follows.
- Small Tailwind visual choices.
- Known debt that the diff names and parks with a stated deferral.
- A small duplication that avoids coupling.
- Complexity the requirement actually demands, such as concurrency, security or external integration.

## Report

- Return findings per `../review/references/finding-format.md`.
- Map severity: `blocker` or `major` for what the lead reviewer would mark as blocking; `minor` for what should be fixed in this change; `nit` for deferrable "food for thought".
- Stay read-only: do not edit files, run git or change state.
- Try to falsify each finding first: confirm that the existing mechanism really exists and fits, and that no real caller or requirement justifies the machinery, before reporting it.
