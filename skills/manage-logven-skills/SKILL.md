---
name: manage-logven-skills
description: Maintain Logven's external skill repository and its local discovery link. Use when creating, changing, validating, committing, pushing, installing, or repairing Logven workflow skills, the companion `logven-skills` repository, or the ignored `.agents/skills` symlink.
---

# Manage Logven Skills

Keep Logven's reusable agent workflows versioned in the companion repository, while the application repository only provides local discovery through an ignored symlink.

## Topology

The checkouts are siblings:

```text
~/Github/
├── logven/                         # Application repository
│   ├── AGENTS.md                    # Tracked; names the required workflows
│   └── .agents/skills -> ../../logven-skills/skills
└── logven-skills/                  # Private workflow repository
    └── skills/<skill-name>/
```

Treat `logven-skills/skills/` as the source of truth. Keep `.agents/` ignored in Logven. Do not commit the symlink or a copied skill directory to the application repository.

## Workflow

1. Inspect `git status -sb` in both repositories before changing anything.
2. Edit or create skills only under `logven-skills/skills/`. Preserve each skill's `SKILL.md`, optional `agents/openai.yaml`, and directly referenced resources together.
3. Validate a changed or new skill with `quick_validate.py` from the installed `skill-creator` package. For existing Logven workflows, also verify every relative Markdown link resolves.
4. Confirm Logven's `.agents/skills` is a symlink to `../../logven-skills/skills` and that the discovered `SKILL.md` files match the companion checkout.
5. Leave the application repository unchanged unless the requested workflow itself requires an `AGENTS.md` update or application-code change.

## Version Control Boundaries

- Commit or push only when the user explicitly asks.
- When asked to commit a skill change, stage only the relevant path in `logven-skills`; never stage `.agents/` in Logven.
- Make one coherent Conventional Commit per requested unit. If the user requests one commit per skill, keep every skill directory in its own commit.
- Before pushing, inspect the companion repository's branch, remote, and ahead/behind state. Push only the explicitly requested branch/remote.
- Report the commit IDs and whether the companion repository remains ahead of its remote.

## Repairing Local Discovery

If the link is missing or points elsewhere, retain any existing local directory as a named backup, then recreate the relative symlink from `logven/.agents/skills`. Do not delete a local skill directory until the companion checkout has been verified as complete.

## Do Not

- Do not move these workflows into `logven/.agents/skills` as tracked application files.
- Do not use a globally installed generic skill as a substitute for this Logven-specific workflow set.
- Do not commit, push, or change remotes based on an implied request.
