# logven-skills

A compact framework for human–machine collaboration on projects. The human sets direction and scope; the main agent owns investigation, coordination and a verified result. Shared principles guide decisions, workflow skills define the stages, and layer skills define implementation responsibilities.

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

No automated UI/DOM tests, including markup assertions hidden in other test layers. Inspect UI in the browser; test domain, policy and nonvisual HTTP contracts. New dependencies require approval. Commits and publication require authorization.

## Discovery and installation

Make `skills/` visible to the host's skill catalog. From a sibling project root:

```sh
mkdir -p .agents
ln -s ../../logven-skills/skills .agents/skills
```

Preserve existing directories and links; merge with the current configuration. Hosts using another skills root can link or install individual skill folders there.

Add this to the target repository's existing `AGENTS.md` or equivalent always-loaded instructions:

```text
Inspect the workspace first. Before repository work, read
.agents/skills/how-we-work/SKILL.md and follow its discovery routes.
If unavailable, locate how-we-work in the configured skill catalog/roots.
```

The always-loaded instruction establishes the entry point; a symlink alone cannot guarantee loading. Trigger descriptions and automatic-invocation metadata support selection. The entry point selects relevant skills and passes resolved paths into delegate briefs without requiring the user to name them.

## Maintaining the framework

Keep each skill focused on its responsibility, with a short purpose, named decision areas or work stages, and a clear completion check. Use tables for contracts and numbered steps for sequences; keep conditional evidence in linked references. Do not repeat shared rules or put project-specific UI systems into general guidance.

Preserve required `name`/`description` frontmatter, discriminating triggers, working relative links and aligned `agents/openai.yaml` metadata. Keep concrete model mappings in `how-we-work`.

Validate every skill with skill-creator's `scripts/quick_validate.py`, check relative links and run `git diff --check`. After workflow changes, verify behavior in temporary workspaces and report what was exercised and its limits. Keep evaluation fixtures and results outside this repository.
