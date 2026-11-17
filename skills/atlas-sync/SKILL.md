---
name: atlas-sync
description: Maintenance. Update Atlas from origin/main (new merged PRs and direct commits), regenerate affected map pages, promote or archive pending decisions, re-check decisions, rebuild the index, and write a sync report. Run only when the user asks to sync Atlas.
---

# Atlas sync

1. Only main. If the user asks to sync any other branch, refuse: Atlas follows `origin/main` only.
2. Run `atlas sync` (takes a lock; safe to re-run; idempotent). It:
   - fetches the mirror, finds PRs merged into main and direct commits since the cursor in `~/.atlas/logven/state.json`;
   - harvests, triages and extracts only the new items (resumable checkpoints);
   - re-blames main into line history (`atlas why <path>:<lines>`), looking through mechanical commits (dependabot, bare lint/format, wide renames);
   - regenerates the map pages (subsystems, types, flows, data model, runtime) whose code changed and re-checks every `path:line` citation;
   - promotes `pending/<branch>` decisions whose PR merged (adjusted by a code check to what actually merged), archives pending branches whose code branch was closed or deleted;
   - re-checks decisions whose scope changed (supersede, deprecate when code was deleted, or `possibly-stale`); never deletes records;
   - refreshes Paul's patterns and playbook if he left new review comments; commits `records/`; rebuilds the index; moves the cursor.
3. Read the report it prints (`~/.atlas/logven/reports/sync-<date>.md`) and summarise for the user: map changes, new decisions, items marked NEEDS HUMAN, possibly-stale decisions.
4. If it fails on the LLM usage limit, say so; re-running later resumes where it stopped.
