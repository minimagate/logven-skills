---
name: atlas-sync
description: Maintenance. Update Atlas from origin/main (new merged PRs and direct commits), regenerate affected map pages, promote or archive pending decisions, re-check decisions, rebuild the index, and write a sync report. Run only when the user asks to sync Atlas.
---

# Atlas sync

1. Only main. If the user asks to sync any other branch, refuse: Atlas follows `origin/main` only. The Atlas repo itself must be on its `main` branch.
   It also runs daily at 07:30 (launchd `com.minimagate.atlas-sync`, `tools/daily.sh`): sync from logven `main`, then push the Atlas repo's `main`. Its log is `reports/daily.log`.
2. Run `atlas sync` (takes a lock; safe to re-run; idempotent). It:
   - fetches the mirror, finds PRs merged into main and direct commits since the cursor in `~/.atlas/logven/state.json`;
   - harvests, triages and extracts only the new items (resumable checkpoints);
   - re-blames main into line history (`atlas why <path>:<lines>`), looking through mechanical commits (dependabot, bare lint/format, wide renames);
   - links new commits that explain themselves to their PR's decisions, or records them as notes (`note/<sha>`), keeping only verbatim quotes;
   - scores Atlas against Paul's new review comments before learning from them (`reports/paul-eval.md`, holdout);
   - regenerates the map pages (subsystems, types, flows, data model, runtime) whose code changed and re-checks every `path:line` citation;
   - promotes `pending/<branch>` decisions whose PR merged (adjusted by a code check to what actually merged), archives pending branches whose code branch was closed or deleted;
   - re-checks decisions whose scope changed (supersede, deprecate when code was deleted, or `possibly-stale`); never deletes records;
   - refreshes Paul's patterns and playbook if he left new review comments; commits `records/`, `raw/`, `evals/`, `reports/` and `state.json` to the Atlas repo's `main`; rebuilds the index; moves the cursor. A manual sync does not push; `git -C ~/.atlas/logven push origin main` does.
3. Read the report it prints (`~/.atlas/logven/reports/sync-<date>.md`), plus `reports/paul-eval.md` when Paul left new comments, and summarise for the user: map changes, new decisions, items marked NEEDS HUMAN, possibly-stale decisions, and how well Atlas predicted Paul.
4. If it fails on the LLM usage limit, say so; re-running later resumes where it stopped.
