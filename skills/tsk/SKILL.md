---
name: tsk
description: Track repository work on the relevant project's tsk board, capture deferred bugs and todos, and manage task handoffs during delegated workflows. Keep board state excluded from Git.
---

# Track work with tsk

The project's tsk board is the shared record of active work, blockers, review handoffs and deferred findings. Keep the work visible there at all times: progress, the current slice and what is next, so the user can watch it move. Update it as work happens; a chat summary alone is not enough. This workflow authorizes routine tracking of the requested work and capture of discoveries without separate approval for every board update. Recording a follow-up does not authorize implementing it.

## Connect to the right board

1. Run `tsk --version`, read `tsk guide` and run `tsk help <command>` before first using each command in the session. Use the CLI, never the interactive TUI or direct store edits. If unavailable, report the tracking gap and installation link (`https://gettsk.sh/docs/install.md`); do not install or invent a replacement board. Continue authorized work that does not depend on tsk.
2. Identify the repository that owns the work. Use `tsk list -p /absolute/project/root --json`, then read an existing task with `tsk list T12 --json`. Reuse the task supplied in a dispatch or brief. Check neighboring tasks before creating duplicates; preserve other agents' work and the user's notes.
3. In a worktree, use the canonical project's absolute path from the parent brief or verified Git/worktree metadata, not the worktree basename. Task IDs address tasks across projects. Do not create a second project for a worktree or put repository work on the desk. Scope the board to the target project, not this skills package merely because its instructions are installed there.
4. Keep the configured store. Do not change `TSK_STATE_DIR` or pass `--state-dir` to obtain a writable or empty board. If access fails, report the exact gap and retain task updates in the handoff for later reconciliation; do not claim they were saved.

## Keep board state out of Git

Before board writes and again before delivery, locate the actual store and any repository-local board artifacts using the installed CLI/configuration and filesystem. Current tsk normally stores data centrally in `~/.tsk`; a central store outside the repository needs no project ignore entry. Do not move it into the project or set up Git backups as part of this workflow.

Board databases, journals, locks, configuration, exports and backups must always be excluded from project Git. For local state, add precise rules to the project's `.gitignore` (for example `.tsk/` or `.tsk-state/` when those are the actual paths); preserve existing rules and avoid broad patterns that hide source or this `skills/tsk/` directory. Ignore known default local state locations proactively when establishing the workflow.

Verify with `git check-ignore -v -- <paths>` and `git ls-files -- <paths>`; ignore rules alone do not untrack existing files. If verified board artifacts are tracked, remove only those paths from the index with `git rm --cached -- <files>` (or `-r` for a board directory), preserving files on disk. Inspect staged content first; do not force removal over staged/user changes. If that conflicts or needs unavailable permissions, report remaining tracked paths as a delivery blocker. Never delete board data, rewrite history or commit/push to enforce exclusion without the corresponding authorization.

The parent owns exclusion changes. Delegates whose file ownership or read-only brief prevents them must report exact paths for the parent to reconcile; tracking never expands a delegate's write scope.

## Track the work

Use one task for a coherent requested outcome, and separate tasks for independently owned delegated slices or deferred findings. When building, express the plan as one task per focused commit on a shared thread ("Commit 1: …", "Commit 2: …"). Set each to `started` when work on it begins and to `review` as soon as it is committed, then carry on to the next without waiting. The task is also the plan and brief: its notes hold the spec (outcome, settled decisions, constraints, owned files), its steps (`tsk steps`) hold the work sequence, and its notes list the checks (verification commands and expected results). Tick steps as they finish. Avoid a task for every command or tiny edit. Notes should carry scope, acceptance criteria, owner identity, branch/PR when known, and related task IDs so another agent can resume.

| Event | Board action |
|---|---|
| Start authorized work | Reuse the matching task or `tsk add -p /absolute/project/root -t "Outcome" -n "Scope, acceptance, owner" --json`; then `tsk status T12 started --no-dispatch` |
| Meaningful progress or changed plan | Read first, then `tsk edit T12 --append-notes "Owner: …; progress/evidence: …; next: …"`; preserve existing notes |
| Concrete blocker | `tsk status T12 blocked --why "Reason" --needs "What unblocks it"`; use `--on T13` for a task dependency or the actual person/profile |
| Work ready for review | `tsk status T12 review --done "What changed" --check "What to verify" --next "Remaining handoff"`; include actual verification results and gaps in notes |
| Commit made | Move that commit's task to `review` as above and start the next; do not wait for the user between commits |
| Human accepts completion | Set `done` only when the user authorizes that task's completion; finishing code, passing review or opening a PR alone is not approval |

Always read lists as JSON and verify writes with `tsk list T12 --json`. Use `--no-dispatch` when starting work in this session: plain `started` on an assigned task can launch another agent. Use known agent profiles for `--assignee`; otherwise record the actual agent/session identity in notes without inventing a profile. Never override another worker's status or ownership silently. Do not unblock or approve your own task without authorization.

Read before retrying uncertain writes, especially `--append-notes`, replies and step toggles, which can duplicate or invert updates. Follow refusal codes and installed help. Add steps to commit tasks, where the user wants the sequence tracked; elsewhere add them only when asked. Dispatch, merge, cleanup, archive and backup operations require their own authorization; tracking does not imply it.

## Capture discoveries without expanding scope

Record bugs, problems, missing tests, todos and other actionable follow-ups as soon as they are found, including pre-existing defects and items outside the current PR. Search the project board first; append evidence to a matching task rather than duplicating it. New deferred tasks stay `open` and unassigned unless ownership or prioritization is already agreed.

Each finding needs a concrete title, observed behavior and consequence, source path or reproduction evidence, suggested next action, why it is deferred, and a backlink to the originating task/branch/PR. Distinguish confirmed defects from suspected issues needing investigation. Do not create vague speculative cleanup tasks or bury deferred work only in PR prose. Link the follow-up ID from the active task and mention material discoveries in the handoff. Fix in-scope defects under the active task; capture out-of-scope work without silently doing it.

## Delegated handoffs

The parent creates or reuses a task for each independently owned slice before dispatch, with the spec, steps and checks on the task. The fresh-context brief carries the task ID, canonical project path, owner, this skill's resolved path and only what the board cannot hold. The builder reads the task with `tsk list T<n> --json` and works from it. Do not invoke tsk dispatch merely because host subagents are in use.

Each builder reads its task, marks it `started --no-dispatch`, records discoveries and blockers, and moves **its own task** to `review` with implementation and verification evidence before reporting back. Direct the review to the actual parent/reviewer using `--on <profile-or-name>`. A blocked or incomplete slice must report its real state instead. If board access is unavailable to the delegate, it returns exact pending updates for the parent to apply and verify.

The parent inspects each slice and the integrated result, records review evidence and follow-up IDs, and leaves the overall task `started` until integration and required verification finish. Read-only research/review delegates may read the board but return findings and task updates for the parent to record unless explicitly allowed board writes. Rejected work goes back through the authorized feedback/resumption flow. Delegates never approve their own work or mark it `done`; the parent also leaves completed tasks in `review` for the user unless completion was authorized. `review` on a commit task is a marker, not a pause: work continues.

At handoff, reconcile task states with reality and report task IDs, what is ready for review, outstanding blockers and deferred findings. Board unavailability is a reported limitation, never a successful update.
