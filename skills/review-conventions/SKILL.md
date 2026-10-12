---
name: review-conventions
description: Use when reviewing a diff for compliance with the repository's own written guidelines and neighbouring code patterns, such as AGENTS.md or CLAUDE.md rules, naming, file placement, framework conventions and test rules. Covers only convention compliance.
---

# Review Conventions

Check that the diff follows the rules the repo has written down and the patterns its neighbouring code already uses.

## Scope

- This lens covers only compliance with written guidelines and established local patterns.
- Leave abstraction size, dead code, correctness and security to other lenses and do not report them.
- Read the repo guidelines (AGENTS.md, CLAUDE.md or equivalent) you were pointed to before reviewing, and read the neighbouring files of each changed file.
- Review only the diff scope you were given, plus the code that the diff touches.

## What to look for

- Violations of an explicit rule in AGENTS.md, CLAUDE.md or repo docs. Quote the rule text in the finding.
- Naming, file placement, directory structure or module layout that differs from sibling files without a reason.
- Error handling, logging or return shapes that differ from how neighbouring code does the same job.
- Framework conventions broken without need. For Rails: RESTful controllers and routes, strong parameters, thin controllers, model invariants backed by database constraints, and Zeitwerk-compatible file names and constant names.
- New code that adds a second way to do something the repo already does one way, such as a second HTTP client, a second job pattern or a second form pattern.
- Tests that contradict the repo's testing rules, such as the wrong framework, the wrong file location or a forbidden mocking style.
- Commit or PR conventions the repo documents, when the diff includes them.
- New dependencies or a JavaScript build step introduced against `../principles/SKILL.md` or a repo rule against them.

## What is NOT a finding

- Personal taste with no written rule and no neighbouring pattern behind it.
- Patterns that appear only in legacy code the repo is clearly moving away from.
- Style the configured linter or formatter already enforces, unless the diff bypasses it.
- A rule that the diff does not touch and that was already broken before the diff.
- Choices the guidelines explicitly leave open.

## Report

- Return findings exactly as specified in `../review/references/finding-format.md`.
- Every finding must cite the specific guideline text (quoted) or the specific neighbouring file path that sets the convention.
- Name the convention, show the diff location that breaks it, and state the conforming form.
- Stay read-only: do not edit files, run git, or change state.
- Try to falsify each finding first by checking that the cited rule still applies to this file and was not overridden by a more specific document. Drop it if it does not.
