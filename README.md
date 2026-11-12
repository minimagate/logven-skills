# logven-skills

Compact skills for technical orchestration, Rails implementation, design and review. The main agent plans and delegates technical work, owns design directly, and verifies the result. Complex implementation and delegated planning judgment use a mid-tier reasoning model or stronger; lightweight models handle mechanical work. Adversarial review is one whole-change pass by a flagship reasoning model, examining actual risks beyond repository rules. Concrete tier labels live in `how-we-work`.

## Discovery and installation

Make `skills/` visible to the host's skill catalog. Existing local setup from a sibling project root:

```sh
mkdir -p .agents
ln -s ../../logven-skills/skills .agents/skills
```

Do not overwrite an existing directory/link; merge with its current configuration. Hosts that use another skills root can link or install the individual skill folders there instead.

In the target repository's existing `AGENTS.md` or equivalent always-loaded instructions, add:

```text
Inspect the workspace first. Before repository work, read
.agents/skills/how-we-work/SKILL.md and follow its discovery routes.
If unavailable, locate how-we-work in the configured skill catalog/roots.
```

A symlink alone cannot guarantee that every host loads an entrypoint; the always-loaded instruction makes routing explicit. Each skill also has a trigger description and automatic-invocation metadata. The entrypoint lists descriptions, selects relevant skills and passes their resolved paths into delegate briefs. It never requires the user to name a skill.

## Included skills

| Skill | Purpose |
|---|---|
| `how-we-work` | Discovery, work modes, delegation tiers, principles and verification |
| `plan` | Short technical plan, scoped delegation, no routine approval pause |
| `review` | One flagship adversarial reviewer, beyond guideline compliance |
| `ship` | Coherent authorized commits, checks, pushes and PRs |
| `rails-structure` | Placement, names and responsibility boundaries |
| `rails-models` | Domain invariants, explicit lifecycle and effects |
| `rails-controllers` | HTTP contracts, params and resource routes |
| `rails-authorization` | Pundit permissions and tenant isolation |
| `rails-migrations` | Reversible schema, constraints and data-change separation |
| `rails-frontend` | ERB, Turbo, Stimulus and explicit UI composition |
| `rails-design` | Stack-independent compact design consistent with the product |
| `rails-tests` | Minimal nonvisual coverage; no UI/DOM tests anywhere |

The design name remains `rails-design` for compatibility; its visual principles apply to any stack. Non-Rails projects skip Rails implementation defaults. Optional project skills use [this template](skills/how-we-work/references/project-skill-template.md); load only the matching repository's facts.

## Operating rules

- Think before editing, keep changes surgical, define observable success and verify it. Use the fewest clear lines that preserve behavior and best practices. Source adaptations: [Karpathy-inspired guidelines](https://github.com/multica-ai/andrej-karpathy-skills/blob/main/CLAUDE.md) and [Ponytail](https://github.com/DietrichGebert/ponytail).
- Technical work: inspect, plan, delegate, verify. Design: main agent designs and edits directly without plan approval. Ask only when a material decision or actual authorization is missing.
- Model domain facts explicitly, derive technical representations, and use native framework flows. Foundations own mechanics and intrinsic invariants; explicit callers choose defaults and apply product policy. [Sheets rewrite evidence](skills/how-we-work/references/foundations.md) and [direct review patterns](skills/how-we-work/references/review-patterns.md) explain the distinctions and their limits.
- No UI/DOM tests, including HTML/text/selector assertions concealed in request/helper tests. Verify UI in the browser; test domain, policy and nonvisual HTTP contracts.
- No new dependencies without approval. No automatic commits or publishing. Existing user authorization persists; external actions follow `ship`.

## Maintaining the package

Keep required `name`/`description` frontmatter, concise trigger descriptions, relative links and `agents/openai.yaml` aligned. Put conditional evidence/procedures in linked references, not every skill. Record concrete model mappings only in `how-we-work`; other skills refer to capability tiers. No installed project-specific UI system belongs in shared guidance.

Validate every skill with the skill-creator `scripts/quick_validate.py`, check relative links and `git diff --check`, and exercise realistic routing/delegation scenarios after workflow changes.
