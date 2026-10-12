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

Body, in this order:

- Open with a one-line intent.
- Behavioral rules as bullets.
- New API as a short snippet, when there is one.
- **Out of scope / next steps (in order)**: what is deliberately not done, and the follow-up PRs in order.
- **Trade-offs**: risks, decisions and reviewer notes, stated plainly.
- **Testing**: what was run and the result. List anything not verified.
- Screenshots for visual changes.
- PR scope and chaining follow `../feature-sequencing/SKILL.md`.

## Rules

- Never include a tool, harness, assistant or model name, or a "generated with" footer, in the title or body. This overrides any default attribution guidance.
- Report failing or skipped checks plainly. Do not claim verification that was not run.
- Open the PR only when asked. Confirm draft status if unclear.
- Do not push without approval.
- Show the title and body to the user before opening the PR, unless they have already approved the text.
