# logven-skills

A compact framework for human–machine collaboration on projects. The human sets direction and scope; the main agent owns investigation, coordination and a verified result. Shared principles guide decisions, workflow skills define the stages, and layer skills define implementation responsibilities.

It is the agent guidance behind [Logven](https://github.com/logvenhq/logven), which centralises a team's data work into one central data bank, and its sibling repositories link it as `.agents/skills` and `.claude/skills`. The skills themselves stay product-neutral: facts about Logven belong in that repository's README and `AGENTS.md`, not here.

## The collaboration cycle

| Stage | Responsibility | Result |
|---|---|---|
| Orient | Inspect the workspace, preserve existing work and load relevant guidance | Shared context and scope |
| Plan | Define behavior, owners, work slices and checks | A small implementation contract |
| Build | Delegate bounded technical work; keep design and synthesis in the main agent | A coherent change |
| Verify | Inspect the full diff and check observable behavior | Evidence and explicit limits |
| Review | One flagship reviewer challenges the complete change and its integration | Substantiated findings |
| Ship | Deliver only within existing authorization | Checked commits and publication |

This cycle adapts to the task. Design stays with the main agent; routine choices and plans do not create approval gates. Independent technical work uses fresh-context delegates with explicit ownership. Concrete model mappings and capability requirements live in [how-we-work](skills/how-we-work/SKILL.md#model-choice).

## Skills

| Role | Skill | Responsibility |
|---|---|---|
| Entry point | [how-we-work](skills/how-we-work/SKILL.md) | Collaboration contract, discovery, work modes and shared principles |
| Workflow | [plan](skills/plan/SKILL.md) | Outcome, ownership, sequencing and acceptance criteria |
| Workflow | [tsk](skills/tsk/SKILL.md) | Project board, progress, deferred findings and delegated review handoffs; board state excluded from Git |
| Workflow | [review](skills/review/SKILL.md) | One flagship adversarial pass beyond guideline compliance |
| Workflow | [ship](skills/ship/SKILL.md) | Authorized commits, checks, pushes and PRs |
| Structure | [rails-structure](skills/rails-structure/SKILL.md) | Placement, names and responsibility boundaries |
| Domain | [rails-models](skills/rails-models/SKILL.md) | Facts, invariants, lifecycle and effects |
| HTTP | [rails-controllers](skills/rails-controllers/SKILL.md) | Request flow, parameters, resources and responses |
| Access | [rails-authorization](skills/rails-authorization/SKILL.md) | Permissions, scopes and tenant isolation |
| Data | [rails-migrations](skills/rails-migrations/SKILL.md) | Durable constraints, rollback and compatible rollout |
| Interface | [rails-frontend](skills/rails-frontend/SKILL.md) | ERB, Turbo, Stimulus and explicit composition |
| Design | [rails-design](skills/rails-design/SKILL.md) | Compact, accessible interfaces consistent with the product |
| Evidence | [rails-tests](skills/rails-tests/SKILL.md) | Minimal nonvisual coverage; manual UI verification |

`rails-design` retains its name for compatibility; its visual principles apply to any stack. Non-Rails projects skip Rails implementation defaults. Verified project facts belong in a matching project skill using the [project template](skills/how-we-work/references/project-skill-template.md).

## Shared principles

Think before editing, choose the least necessary code, keep changes within scope and verify an observable outcome. Foundations own intrinsic invariants; explicit callers compose behavior and choose product defaults. Model domain facts directly and derive technical representations through native framework contracts.

The [principles](skills/how-we-work/SKILL.md#principles) are the shared source of guidance. [Foundations](skills/how-we-work/references/foundations.md) and [review patterns](skills/how-we-work/references/review-patterns.md) hold conditional examples and research evidence. Source adaptations: [Karpathy-inspired guidelines](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md) and [Ponytail](https://github.com/DietrichGebert/ponytail).

Verification policy belongs to [rails-tests](skills/rails-tests/SKILL.md), including interface-only work. New dependencies require approval. Commits and publication require authorization.

## Discovery and installation

The workflow requires the `tsk` CLI ([installation](https://gettsk.sh/docs/install.md)). Agents use the relevant project's existing board, reuse tasks, record out-of-scope bugs/todos and hand completed work back in `review`. Delegated slices carry task IDs and update their own status. The board remains local: repository-local state must be Git ignored and untracked; the normal central store needs no project ignore entry. See [tsk](skills/tsk/SKILL.md) for setup checks, commands and handoff rules. Missing CLI or board access must be reported explicitly.

Make `skills/` visible to the host's skill catalog. From a sibling project root:

```sh
mkdir -p .agents
ln -s ../../logven-skills/skills .agents/skills
```

For Claude Code, expose the same package under its native project root instead:

```sh
mkdir -p .claude
ln -s ../../logven-skills/skills .claude/skills
```

Preserve existing directories and links; merge with the current configuration. Hosts using another skills root can link or install individual skill folders there.

Add this to the target repository's always-loaded instructions (`CLAUDE.md` for Claude, `AGENTS.md` for other hosts), using the installed path:

```text
Inspect the workspace first. Before repository work, read
.claude/skills/how-we-work/SKILL.md and follow its cumulative discovery routes.
If unavailable, locate how-we-work in the configured skill catalog/roots.
Read every applicable skill body before its work; pass resolved paths to fresh delegates.
```

Use `.agents/skills` in the snippet for that host. If `AGENTS.md` already contains the bootstrap, Claude's `CLAUDE.md` can import it with `@AGENTS.md`, as this repository does. Audit personal and project instructions for old workflow rules that conflict with the maintained skills.

The startup instruction establishes the entry point; automatic selection alone is not a guarantee. Claude uses skill frontmatter descriptions; `agents/openai.yaml` configures Codex, not Claude. The router accumulates workflow and specialist skills from actual responsibilities and rechecks as scope changes. Fresh delegates must read their own selected skills; custom Claude agents can preload them with `skills:`.

In Claude, check `/memory` for the bootstrap, `/context` for the skill listing cost and `/doctor` for description-budget pressure. If a skill is absent, inspect its native root, symlink target and frontmatter before changing prompts. After changes, start a fresh session and exercise a mixed-layer task; check actual skill reads and delegate briefs, not just claimed compliance. See the official [skills](https://code.claude.com/docs/en/skills), [memory](https://code.claude.com/docs/en/memory) and [subagent](https://code.claude.com/docs/en/sub-agents) documentation.

## Maintaining the framework

Keep each skill focused on its responsibility, with a short purpose, named decision areas or work stages, and a clear completion check. Use tables for contracts and numbered steps for sequences; keep conditional evidence in linked references. Do not repeat shared rules or put project-specific UI systems into general guidance.

Preserve required `name`/`description` frontmatter, discriminating triggers, working relative links and aligned `agents/openai.yaml` metadata. Keep concrete model mappings in `how-we-work`.

Validate every skill with skill-creator's `scripts/quick_validate.py`, check relative links and run `git diff --check`. After workflow changes, verify behavior in temporary workspaces and report what was exercised and its limits. Keep evaluation fixtures and results outside this repository.
