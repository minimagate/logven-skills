---
name: linear
description: Start repository work from a Linear issue and keep the issue in step with it. Use when the user names an issue key ("we need to talk about ENG-93", "let's do ENG-93"), when a branch or PR belongs to a Linear issue, or when an out-of-scope bug turns up on a project that tracks its issues in Linear.
---

# Work from Linear issues

Linear is the team's shared record of what needs doing and why; [tsk](../tsk/SKILL.md) stays the local record of how this session does it (plan, steps, checks, handoffs). Use the available Linear connection, normally the Linear MCP server. If it is missing or unauthenticated, ask the user to connect it, continue with work that does not depend on it, and report the Linear updates still pending; never claim they were made.

This skill authorizes four kinds of Linear writes: status moves, PR links, backlog issues for findings and comments that add evidence to an existing issue. Anything else (editing an issue's title, description, priority, assignee or labels, commenting decisions, closing or deleting) waits for the user to ask. Delegates never write to Linear; they return findings for the main agent to file.

## Start from an issue

When the user names an issue key, the session starts from that issue.

1. Read it in full: title, description, status, priority, labels, project, assignee, parent and sub-issues, related issues, attached PRs and links, and every comment. Open related issues and documents when they change the scope.
2. Inspect the code it touches before answering, using [atlas](../atlas/SKILL.md) where the project has it. Then open the discussion: the problem in plain words, what the code does today, open questions and a recommended approach.
3. Talking about an issue changes nothing. When the user agrees on work, reuse or create its tsk task: the title starts with the key (`ENG-93: …`) and the notes carry the issue URL and the decisions settled in the discussion.

## Keep the status in step

List the team's workflow states before the first move and use the names the team actually has, matched by type (backlog, unstarted, started, completed). Move an issue forward only; leave it where it is if it already sits at or past the target, or if someone else moved it since you read it.

| Moment | Issue |
|---|---|
| Discussion, planning, questions | No change |
| Implementation of the agreed work begins | The team's in-progress state |
| PR opened, draft included | PR linked; the team's review state |
| PR merged | Done, normally moved by Linear's GitHub integration. Do not set it yourself unless the user says the work is complete |

## Link the PR

[ship](../ship/SKILL.md) opens the PR; this step names the issue in it. Keep the project's branch naming. Put the key on its own line in the PR body: `Fixes ENG-93` when merging completes the issue, `Part of ENG-93` when it does not (every PR of a stack but the last). Linear's GitHub integration links the PR from that line.

After opening, read the issue again. If the PR is not attached or the status did not move, attach the PR URL and set the review state yourself. Record the PR URL in the tsk task notes.

## File bugs found along the way

On a project that tracks issues in Linear (the session started from an issue, or the project's instructions say so), a bug or problem outside the current PR becomes a Linear issue instead of a deferred tsk task. Fix in-scope defects under the active work as usual; filing a finding does not authorize fixing it.

1. Search the team's open issues first. On a match, comment the new evidence there instead of filing a duplicate.
2. Otherwise create an issue in the same team, in its backlog state, unassigned. Give it a concrete title. The description holds the observed behavior and its consequence, a `path:line` or reproduction, whether it is confirmed or suspected, a suggested next step, and where it was found (originating issue key, branch or PR).
3. End the description with your signature on its own line, so readers know an agent wrote it under the user's account: `Filed by <agent> (<model>) while working on ENG-93.`, for example `Filed by Claude Code (Claude Opus 5.5) while working on ENG-93.` Without an originating issue, name the branch or PR instead.
4. Mark it related to the originating issue, add its key to the active tsk task's notes and mention it in the handoff.

Pick the team the project's other issues live in; ask once if that is unclear.
