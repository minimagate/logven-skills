# logven-skills

Reusable agent skills for planning, building and reviewing Rails apps with a minimalist philosophy, plus per-project skills that carry each app's own conventions (currently `project-logven`).

## How it is wired

A project discovers the skills through a local link to `skills/`, which is ignored in git:

```text
logven/.agents/skills -> ../../logven-skills/skills
```

The link lives in each project checkout, so nothing project-specific is committed here.

- The project's `AGENTS.md` says what the repo contains.
- The general skills say how to work.
- The project skill (`project-<name>`) carries that app's names, paths and decisions, and wins where it differs.

## The workflow

Start with `how-we-work`; it routes each situation to the skill below.

1. Plan. Use `plan` for small changes, or `plan-feature` for big features: parallel explorers, then critics, then triage to a lean plan. The user agrees the plan before any code.
2. Delegate. Subagents on the cheapest capable model implement from self-contained briefs.
3. Verify and commit. The orchestrator reads the full diff, runs tests and linters, and commits one scoped change at a time.
4. Review. Lens reviewers run in parallel on the strongest available model: small diffs run conventions, cleanliness and correctness; larger diffs run all six (the five general lenses plus `review-structure`). The orchestrator verifies their findings and synthesizes them.
5. Pull request. Written from the branch's commits and diff, with checks reported factually.

The six lenses are `review-overengineering`, `review-over-standardisation`, `review-conventions`, `review-cleanliness`, `review-correctness` and `review-structure`.

Invariants:

- The main thread plans and analyzes only.
- Implementation is always delegated to a subagent.
- Reviews are always delegated, never done by the orchestrator.
- No tool, harness, assistant or model names in commits, PRs or review comments.
- No new dependencies without the user's approval.

## Skills

| Group | Skill | Use it for |
|---|---|---|
| Entrypoint | `how-we-work` | Start here: the roles, the plan/delegate/verify/review loop and which skill to load next |
| Workflow | `plan` | Agreeing scope and approach before any code, for small changes |
| Workflow | `plan-feature` | Multi-agent planning for big features: new concepts, schema, integrations, contracts |
| Workflow | `feature-sequencing` | Ordering and slicing work into commits and PRs; commit and PR naming |
| Workflow | `delegate` | Briefing a subagent for every implementation, including small fixes |
| Workflow | `verify-and-commit` | Checking the subagent's diff, running checks, committing one scoped change |
| Workflow | `pull-request` | Writing a PR title and description from the branch's commits and diff |
| Principles | `principles` | Shared minimalism, dependency and future-proofing rules; cited, not restated |
| Plan critics | `plan-simplicity` | Scope and machinery beyond the stated requirement |
| Plan critics | `plan-future-proofing` | Decisions that are expensive to reverse |
| Plan critics | `plan-edge-cases` | Failure modes and unusual states the plan ignores |
| Plan critics | `plan-fit` | Placement, duplication, repo rules and slice ordering |
| Review | `review` | Coordinating the six lens reviewers, then verifying and synthesizing |
| Review | `review-overengineering` | Machinery the requirement does not justify |
| Review | `review-over-standardisation` | Premature sharing and uniformity that couples code |
| Review | `review-conventions` | Compliance with written repo rules and neighbouring patterns |
| Review | `review-cleanliness` | Dead code, leftovers and scope creep the diff introduces |
| Review | `review-correctness` | Wrong results, authorization gaps, races and data loss |
| Review | `review-structure` | The project's structural bar: necessity, one mechanism per job, ownership, authorization, REST |
| Rails guidelines | `rails-structure` | Where code lives, how it is named and namespaced |
| Rails guidelines | `rails-models` | Active Record models, state, associations, validations, callbacks |
| Rails guidelines | `rails-controllers` | Thin controllers, routes, strong params, responses |
| Rails guidelines | `rails-authorization` | Pundit policies, scopes and roles |
| Rails guidelines | `rails-migrations` | Structure-only, reversible migrations and `db/schema.rb` |
| Rails guidelines | `rails-frontend` | ERB, Turbo, Stimulus, ViewComponent and Importmap UI |
| Rails guidelines | `rails-design` | Visual design and Tailwind styling, in light and dark mode |
| Rails guidelines | `rails-tests` | Minimal Minitest coverage of logic and HTTP contracts |
| Project | `project-logven` | Logven's names, paths, helpers and design system |

## Starting a new project

1. Link this repo's `skills/` into the project as `.agents/skills` (see above).
2. Write the project's `AGENTS.md`: what the repo contains and its commands.
3. Copy `templates/project-skill.md` to `skills/project-<name>/SKILL.md`, plus `agents/openai.yaml` as shown in the template's comment. Fill it as you learn the app, and keep project facts there only.
4. The `rails-*` skills are opinionated defaults for Rails 8 with Hotwire, Tailwind, Pundit, minimal dependencies and no npm build. A project skill can override any of them.
5. For a non-Rails stack, keep the workflow, planning, review and `principles` skills and skip the `rails-*` ones.

`delegate` briefs list the `rails-*` skills for the layers touched, the project skill and `principles`.

## Editing skills

- Each skill is `skills/<name>/SKILL.md` with `name` and `description` frontmatter. The description says when to trigger the skill and what it hands off to.
- Each skill also has an `agents/openai.yaml`.
- Keep skills tight, about 40 to 70 lines. Say each rule once, and link `principles` instead of restating it.
- Reference other skills by relative path, such as `../name/SKILL.md`.
- After renames or edits, check that every `../<name>/SKILL.md` link resolves.
- Model tiers are written abstractly (cheapest capable for implementation, strongest available for review); the only mapping to concrete model names is a single line in `delegate`.
- Project-specific names belong in the project skill, never in the general skills.
- Examples in general skills use neutral names (orders, invoices).
- When a skill is added, renamed or removed, update the table in the same change, so every skill in `skills/` appears exactly once.
