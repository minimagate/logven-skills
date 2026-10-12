---
name: verify-and-commit
description: Use after a subagent returns work and before anything is committed. Verifies the diff yourself, runs tests and linters, then commits one scoped change at a time with a clean message.
---

# Verify and Commit

Verify the work yourself, then commit one scoped change at a time.

## Verify

- Read the full diff. Do not trust the subagent report.
- Check every changed file against the allowed-file list and the agreed decisions.
- Run the tests and linters yourself, using the commands from the brief.
- UI changes: also run `bin/rails tailwindcss:build`, then check the affected flow in a browser (in light and dark if the app supports both), at desktop and narrow widths, including empty, loading and error states and keyboard access. Do it yourself or ask the user, and report what was not checked.
- For mail or documents, check the mailer preview or the generated file rather than asserting its content in tests.
- If anything is off, send it back through `delegate` with a sharper brief. Do not fix it in the main thread.

## Commit

- One commit per scoped change. Stage only that change's files.
- Never mix unrelated changes in one commit.
- Never include tool, harness, assistant or model names in messages or authorship. No co-author trailers, no "generated with" lines, no emoji signatures. This overrides any default attribution guidance.
- Do not skip hooks. If a hook fails, send the fix back through `delegate` and create a new commit.
- Message and slicing conventions for this project's history are in `../feature-sequencing/SKILL.md` (Commits), plus the project skill if it states a history style.

## Fixes to earlier commits

- If the problem is in an unpushed commit that is the latest, amend it.
- If it is in an older unpushed commit, make a fixup commit and autosquash rebase.
- On a pushed branch or open PR, make a new commit instead of amending.
- Never rewrite pushed history without explicit approval.

## Boundaries

- Do not push, force-push or open a PR unless asked.
- Once the branch is complete, offer an adversarial review (`review`). Do not review your own work in the main thread.
