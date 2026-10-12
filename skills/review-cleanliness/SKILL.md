---
name: review-cleanliness
description: Use when reviewing a diff for code hygiene the change itself introduces, such as dead code, leftover debug output, stale comments, unrelated edits, or unreferenced files. Covers only hygiene of the change, not pre-existing mess.
---

# Review Cleanliness

Find hygiene problems that the diff adds or leaves behind, and nothing the diff did not touch.

## Scope

- This lens covers only hygiene introduced by the change: dead code, leftovers, debug output, unclear names, stale comments and scope creep.
- Leave design, abstraction size, conventions, correctness and security to other lenses and do not report them.
- Read the repo guidelines (AGENTS.md, CLAUDE.md or equivalent) you were pointed to before reviewing.
- Review only the diff scope you were given, plus the code that the diff touches.

## What to look for

- Dead code added or left behind: unused methods, parameters, variables, imports, constants and routes.
- Leftovers from a superseded implementation: old paths, aliases, feature flags that are always on, or commented-out code.
- Debug output, temporary logging, `binding.pry`, `console.log`, or `puts` added by the change.
- TODO, FIXME, XXX or stray notes added by the change without an owner or ticket.
- Unclear or misleading names introduced by the change, and comments that restate the code or no longer match it.
- A missing comment only where a non-obvious why exists and the code would mislead a reader without it.
- Duplicated logic inside the change itself, such as the same block written twice in one file.
- Methods or nesting the change made overly long or deep, where the change is the cause.
- Files added that nothing in the repo references.
- Unrelated edits mixed into the change, such as reformatting or renaming code the feature did not need to touch.

## What is NOT a finding

- Pre-existing mess in lines the diff did not touch.
- Formatting that the configured linter or formatter handles.
- A comment that explains a real non-obvious constraint, even if it is long.
- Code that is unused only in this diff but is an intentional public API that the repo exports.
- Naming choices that are consistent with neighbouring code, even if you would name them differently.

## Report

- Return findings exactly as specified in `../review/references/finding-format.md`.
- For each finding, give the exact file and line range and the specific artifact, such as the unused import or the debug line.
- For unused code, show that no reference exists by searching the repo, and say what you searched.
- Stay read-only: do not edit files, run git, or change state.
- Try to falsify each finding first by searching for dynamic or external references to the code. Drop it if something still uses it.
