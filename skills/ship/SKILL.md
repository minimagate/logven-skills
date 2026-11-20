---
name: ship
description: Slice authorized work into coherent commits and PRs, verify local checks, and write concise history from the actual diff. Use when asked to commit, push or open a PR; opening a PR starts by rebuilding the branch into small explained commits. Controls push and publication boundaries.
---

# Ship

Deliver a coherent, verified change with history that explains the resulting behavior. Read branch history and the full diff against its base; follow project conventions and existing authorization.

## Delivery boundaries

| Action | Authorization |
|---|---|
| Create commits | Requested or already authorized |
| First push or opening a PR | The user says so explicitly; "build a PR" or "build a draft PR" is not permission |
| Later push or update | Explicit authorization for that push, or ongoing push authorization |
| Rebuild and force-push the branch's own history while opening its PR | Included in the request to open the PR ([Open a PR](#open-a-pr)) |
| Any other history rewrite, force-push or hook bypass | Explicit permission |
| Publish with failing required checks | User's informed approval |

Work stays local until the user asks to push or open a PR. Prepare a concrete reviewable result first. Once asked, the PR needs no further approval for its prose; ask only for unresolved material details. A PR opens as a draft unless the user says otherwise.

## Shape the change

While building, make each slice one focused commit on a single branch and keep going until the implementation is finished; do not pause for review between commits. Split into a stack of PRs only when the user asks. Give each commit and PR one coherent concern. Sequence necessary preparation, schema/domain contracts, integration, HTTP/policies and complete UI. Tests travel with the behavior they protect. Separate pure moves from edits when useful; avoid empty skeletons and a commit for every method.

Keep unrelated follow-ups separate. Remove superseded paths within scope. Fold fixes into unpushed commits only when history cleanup is authorized.

## Verify the result

Check each changed line against the request. Trace one complete user path through ownership/permissions, submitted state and failure response. Passing checks alone do not prove a working flow. Remove orphaned paths, speculative knobs and unnecessary layers created by the change; preserve user edits.

Before committing or publishing, run relevant tests/lint and applicable nonvisual CI checks. Inspect aggregate commands first: if they invoke forbidden system/browser/UI suites, run nonvisual equivalents without changing CI or deleting tests. Inspect UI in the browser and run the asset build. Report excluded/unrun checks and failures; never label filtered checks as full CI.

Apply [tsk's Git exclusion check](../tsk/SKILL.md#keep-board-state-out-of-git): board state must be ignored and absent from the index, including any local exports or backups. Reconcile active and delegated tasks, link deferred findings and record branch/PR and verification evidence. Leave verified tasks in `review` unless the user authorized completion; committing or opening a PR does not itself mark work done.

## Open a PR

When the user asks to open a PR, the first step is rebuilding the branch history from its final state. Atlas pins each commit message to the lines that commit last touched (`atlas why <path>:<lines>`), so write history for someone reading one line months later.

1. **Index the final state.** Fetch, read the complete `git diff origin/main...HEAD` and the existing commits, and group the hunks into concerns, one per future commit, in the [Shape the change](#shape-the-change) order. Record each new structural choice with `atlas pending add` ([atlas](../atlas/SKILL.md)).
2. **Rebuild the commits.** Keep the tip as `backup/<branch>`, `git reset --soft` to the merge base with `origin/main`, unstage, and recommit hunk by hunk in that order. Each commit is small, coherent and carries one reason.
3. **Explain each commit.** The subject says what changed, short and plain. The body says why whenever the diff doesn't: the constraint, the rejected alternative or the consequence, in one to three plain sentences ("Only one usage, does not pay rent."). Never restate the diff; leave the body out when there is nothing to add. Put mechanical changes (lint, wide renames, pure moves) in their own commits with bare subjects ("Linting", "Renaming X to Y") so line history skips them.
4. **Prove the tree is unchanged.** `git diff backup/<branch> HEAD` must be empty; otherwise stop and fix before pushing.
5. **Publish.** `git push --force-with-lease -u origin <branch>`, open the PR, confirm the remote branch and PR head match local `HEAD`, then delete `backup/<branch>`.

Skip the rebuild when the PR already exists with review activity or another person has commits on the branch; say so and push the history as it is.

## Write and publish

Stage only work within the authorized scope, even if a generic git helper proposes staging everything. Inspect staged changes before committing. Default subjects are short, descriptive and unprefixed unless project rules override; bodies follow [Open a PR](#open-a-pr). No tool/model names, generated-with lines or attribution trailers in commits or PRs.

Build the PR title and body from all branch commits and the full diff. Default to a plain title under 70 characters and a short paragraph explaining behavior and reason, followed by one truthful check-result line. Work for a Linear issue names it in the body and updates the issue per [linear](../linear/SKILL.md#link-the-pr). Explain meaningful representation or ownership changes so removed glue is reviewable. Follow required repository templates.

After an authorized commit or push, verify the resulting git state and report what was delivered, checks and material limits.
