---
name: pull-request
description: Use when asked to open a pull request or write a PR title and description. Summarizes from the branch's commits and diff against the base branch, and reports checks factually.
---

# Pull Request

Write the PR from the branch's actual commits and diff, not from memory.

## Gather facts

- Read `git log <base>..HEAD` and `git diff <base>...HEAD --stat`, then the diff itself.
- Confirm the base branch. If unclear, ask.
- Collect the test and lint results from this session. Do not reuse old results.

## Title

- Short and imperative, under 70 characters.
- No tool, harness, assistant or model names.

## Body

Use these sections:

- **Summary**: what and why, 1-3 bullets.
- **Changes**: grouped by area (for example, API, UI, tests, config).
- **Testing**: what was run and the result. List anything not verified.
- **Notes for reviewers**: risks, decisions, follow-ups. Include only if relevant.

## Rules

- Never include a tool, harness, assistant or model name, or a "generated with" footer, in the title or body. This overrides any default attribution guidance.
- Report failing or skipped checks plainly. Do not claim verification that was not run.
- Open the PR only when asked. Confirm draft status if unclear.
- Do not push without approval.
- Show the title and body to the user before opening the PR, unless they have already approved the text.
