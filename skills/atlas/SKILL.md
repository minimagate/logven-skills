---
name: atlas
description: Use whenever working in the logven repo: to learn how something works or why it is built that way, before changing code, and when a change makes a new structural choice. Atlas is the local map and decision history of logven at origin/main, read through the `atlas` CLI.
---

# Atlas

Atlas maps logven at `origin/main`: subsystems, flows, types and files, each linked to the decisions, conventions and review patterns (Paul, `psguazz`) behind them, down to the commit that shaped each line. Atlas tells you where to look and why. The code tells you what is true.

## Navigate

1. `atlas ask "<question>"` returns ranked addresses and the matching code and doc sections.
2. `atlas show <address>` prints the page, then **Code** (`path:line · symbol`) and **Next** (linked addresses). Follow Next instead of guessing commands.
3. Answer from both sources. Atlas gives the history and where to look; the code and the repo docs (`README.md`, `AGENTS.md`) say what holds today. Open the Code lines behind every claim, follow each step to where it is enforced, and read the doc sections `ask` returns. A why answer pairs the recorded decision with the rule that enforces it now.

Addresses: `workers` (subsystem) · `flow/worker-run` · `type/Workers::Workflow` · `D-268-3` · `app/models/workers/run.rb` · `app/models/workers/run.rb:40-60` · `#268` · `history/workers` · `playbook` · `pattern/<slug>` · `convention/<slug>` · `feature/<slug>` · `doc/<name>` · `person/<handle>`.

| You need | Route |
|---|---|
| How X works | ask → flow or subsystem → open the Code lines and follow each step to its checks |
| Why X is built so | ask → `D-…` → quote stated reasons with their source link, then confirm what enforces them today |
| Why these lines exist | `atlas why <path>:<from>-<to>` → the commits that last shaped them, messages verbatim, their PRs and those PRs' decisions for the file |
| How a file or subsystem got this way | `atlas history <path|subsystem>`: PRs and decisions in order |
| To change a file | the edit hook injects its rules; `atlas show <path>` for the rest |
| What Paul would flag | `atlas show playbook` → `pattern/<slug>`; for a real diff, the `atlas-review` skill |
| System overview | `atlas map` (full) or `atlas map --brief` |

## Read records correctly

- **Status.** `active` binds. `possibly-stale`: the code under it changed; check before relying on it. `superseded`: follow `superseded_by`. `deprecated`: its code was deleted.
- **Evidence.** `stated` means a PR body, review comment or commit message gave the reason; quote it with its source URL. `inferred` is Atlas's deduction (confidence ≤ 0.6): label it as inferred and never present it as the author's reason.
- **Line history** shows the last meaningful commit per line; dependabot, bare lint/format commits and wide renames are skipped. A commit message is its author's stated reason for those lines, and a terse subject is only a what. When the last touch is a small fix, the original intent sits further back: `git log -L <from>,<to>:<path> origin/main`.
- **Freshness.** Every page prints `main@<sha>`. If `git rev-parse origin/main` is ahead, say Atlas may lag; syncing runs only when the user asks (`atlas-sync` skill).
- **Hooks.** At session start you get the brief map; on the first edit of each file you get its subsystem, top rules, decisions and Paul's flags. That is a digest, not the full record.

## Rules

- Cite only code you opened in this session. Atlas line numbers describe main; your branch may differ.
- Active decisions bind. If the task conflicts with one, stop: quote it (id, source, stated/inferred) and propose a supersession.
- `inferred` reasons are deductions: label them. Check `possibly-stale` items against the code.
- Never copy Atlas text into code or comments.

## Write back

- **New structural choice** (architecture, data-model, type-system, api-contract, convention, dependency, performance, security, testing, naming, ux): `atlas pending add --title … --statement … --rationale … --kind … --subsystem … [--path …] [--symbol …] [--alternative …] [--supersedes D-…] [--by <handle>]`. It waits on the pending branch for the current code branch and becomes `D-<pr>-P<n>` when the PR merges. `atlas pending list` shows what is waiting.
- **Commit messages feed line history.** When opening a PR, rebuild the branch into small commits whose bodies say why (`ship` skill, "Open a PR").
