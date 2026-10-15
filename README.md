# logven-skills

Reusable agent skills for planning, building and reviewing Rails apps with a minimalist philosophy, plus per-project skills that carry each app's own conventions.

## How it is wired

A project discovers the skills through a local link to `skills/`, which is ignored in git:

```text
logven/.agents/skills -> ../../logven-skills/skills
```

The link lives in each project checkout; each app's own facts live in its `project-<name>` skill in this repo. Only the project skill named after the repo applies.

- The project's `AGENTS.md` says what the repo contains.
- The general skills say how to work.
- The project skill (`project-<name>`) carries that app's names, paths and decisions, and wins where it differs.

## The workflow

Start with `how-we-work`; it routes each situation to the skill below.

1. Plan. Use `plan` to agree scope and approach. Big features use its multi-agent mode: parallel explorers, then four critics from `plan/references/critics.md`, then triage to a lean plan. The user agrees the plan before any code.
2. Delegate. Delegation briefs are a section of `how-we-work`. Subagents on the cheapest capable model implement from self-contained briefs.
3. Verify and commit. Also a section of `how-we-work`. The orchestrator reads the full diff, runs tests and linters, and commits one scoped change at a time. Commits stay local.
4. Review. `review` runs lens reviewers in parallel on the cheapest capable model: small diffs run conventions, cleanliness and correctness; larger diffs run all six. The orchestrator verifies their findings and synthesizes them.
5. Pull request. `ship` writes a simple title and a one-paragraph body from the branch's commits and diff. Opening it is the first push; later pushes need the user's approval. Unrelated tweaks go in a stacked PR.

The six lenses are `overengineering`, `over-standardisation`, `conventions`, `cleanliness`, `correctness` and `structure`, defined in `review/references/lenses.md`.

Invariants:

- The main thread plans and analyzes only.
- Implementation is always delegated to a subagent.
- Reviews are always delegated, never done by the orchestrator.
- Work stays local until the PR; every later push needs the user's approval.
- No tool, harness, assistant or model names in commits, PRs or review comments.
- No new dependencies without the user's approval.

## Skills

| Group | Skill | Use it for |
|---|---|---|
| Entrypoint | `how-we-work` | Start here: roles, the plan/delegate/verify/review loop, routing, principles, delegation briefs, verify and commit |
| Workflow | `plan` | Agreeing scope and approach before any code; multi-agent mode with critics for big features |
| Workflow | `review` | Coordinating lens reviewers, then verifying and synthesizing |
| Workflow | `ship` | Ordering and slicing work into commits and PRs; commit messages; pushing; PR text |
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
3. Copy `skills/how-we-work/references/project-skill-template.md` to `skills/project-<name>/SKILL.md` in this repo (it is the same checkout the project links to), plus `agents/openai.yaml` as shown in the template's comment, and commit it here. Fill it as you learn the app, and keep project facts there only.
4. The `rails-*` skills are opinionated defaults for Rails 8 with Hotwire, Tailwind, Pundit, minimal dependencies and no npm build. A project skill can override any of them.
5. For a non-Rails stack, keep `how-we-work`, `plan`, `review` and `ship` and skip the `rails-*` ones.

Delegate briefs (in `how-we-work`) list the `rails-*` skills for the layers touched, the project skill and the Principles section.

## Editing skills

- Each skill is `skills/<name>/SKILL.md` with `name` and `description` frontmatter. The description says when to trigger the skill and what it hands off to.
- Each skill also has an `agents/openai.yaml`.
- Keep skills tight; put long checklists (lenses, critics, design tokens) in `references/`. Say each rule once, and link the Principles section of `how-we-work` instead of restating it.
- Reference other skills by relative path, such as `../name/SKILL.md`.
- After renames or edits, check that every `../<name>/SKILL.md` link resolves.
- Model choice is written abstractly: every subagent runs on the cheapest capable model; the only mapping to concrete model names is a single line in the Delegate section of `how-we-work`.
- Project-specific names belong in the project skill, never in the general skills.
- Examples in general skills use neutral names (orders, invoices).
- When a skill is added, renamed or removed, update the table in the same change, so every skill in `skills/` appears exactly once.
