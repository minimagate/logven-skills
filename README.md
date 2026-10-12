# logven-skills

Private, versioned agent skills for how Logven's Rails app is built, planned, implemented and reviewed.

## How it is wired

The sibling Logven checkout discovers the skills through its ignored local link:

```text
logven/.agents/skills -> ../../logven-skills/skills
```

Logven's `AGENTS.md` describes what the repo contains. These skills describe how to work in it.
`.agents/` and the symlink are not tracked in Logven.

## The workflow

1. Plan. Use `plan` for small changes, or `plan-feature` for big features: parallel explorers, then critics, then triage to a lean plan. The user agrees the plan before any code.
2. Delegate. Subagents on the cheapest capable model implement from self-contained briefs.
3. Verify and commit. The orchestrator reads the full diff, runs tests and linters, and commits one scoped change at a time.
4. Review. Lens reviewers run in parallel on the strongest available model: small diffs run conventions, cleanliness and correctness; larger diffs run all six. The orchestrator verifies their findings and synthesizes them.
5. Pull request. Written from the branch's commits and diff, with checks reported factually.

Invariants:

- The main thread plans and analyzes only.
- Implementation is always delegated to a subagent.
- Reviews are always delegated, never done by the orchestrator.
- No tool, harness, assistant or model names in commits, PRs or review comments.
- No new dependencies without the user's approval.

## Skills

| Group | Skill | Use it for |
|---|---|---|
| Workflow | `plan` | Agreeing scope and approach before any code, for small changes |
| Workflow | `plan-feature` | Multi-agent planning for big features (new concepts, schema, integrations, contracts) |
| Workflow | `feature-sequencing` | Ordering and slicing work into commits and PRs; commit and PR naming |
| Workflow | `delegate` | Briefing a subagent for every implementation, including small fixes |
| Workflow | `verify-and-commit` | Checking the subagent's diff, running checks, committing one scoped change |
| Workflow | `pull-request` | Writing a PR title and description from the branch's actual commits and diff |
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
| Review | `review-maintainer` | The lead reviewer's structural bar |
| Rails | `rails-structure` | Where code lives, how it is named and namespaced |
| Rails | `rails-models` | Active Record models, state, associations, validations, callbacks |
| Rails | `rails-controllers` | Thin controllers, routes, strong params, responses |
| Rails | `rails-authorization` | Pundit policies, scopes and roles |
| Rails | `rails-migrations` | Schema-only, reversible migrations and `db/schema.rb` |
| Rails | `rails-frontend` | ERB, Turbo, Stimulus, ViewComponent and Importmap UI |
| Rails | `rails-design` | Visual design and Tailwind styling, in light and dark mode |
| Rails | `rails-tests` | Minimal Minitest coverage of logic and HTTP contracts |

## Editing skills

- Each skill is `skills/<name>/SKILL.md` with `name` and `description` frontmatter. The description says when to trigger the skill and what it hands off to.
- Each skill also has an `agents/openai.yaml`.
- Keep skills tight, about 40 to 70 lines. Say each rule once, and link `principles` instead of restating it.
- Reference other skills by relative path, such as `../name/SKILL.md`.
- Every rule should be backed by evidence from the Logven repo.
- After renames or edits, check that every `../<name>/SKILL.md` link resolves.
- Model tiers are written abstractly (cheapest capable for implementation, strongest available for review); the only mapping to concrete model names is a single line in `delegate`.

## Research

`research/` holds the analysis of the lead reviewer's review comments, commit corrections and feature structuring. The Rails guideline skills and `review-maintainer` are derived from it. It is evidence, not a skill.
