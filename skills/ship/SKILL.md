---
name: ship
description: Slice authorized work into coherent commits and PRs, verify local checks, and write concise history from the actual diff. Controls push and publication boundaries.
---

# Ship

Read actual branch history and diff against its base. Follow project history conventions and existing user authorization.

- Order dependent work: necessary prep, schema/domain contracts, integration, HTTP/policies, complete UI. Tests travel with the behavior they protect. Keep pure moves separate from edits when useful; avoid ceremony, empty skeletons and a commit for every method.
- Before shipping, check each changed line against the request. Trace one complete user path, ownership/permissions, submitted state and failure response; verify real behavior rather than equating passing checks with a working flow. Remove your change's orphaned paths, speculative knobs and unnecessary layers; prefer a smaller complete implementation without unrelated cleanup. Explain any meaningful representation or ownership change in the PR so its deleted glue is reviewable.
- Each commit/PR has one coherent concern; remove superseded paths in scope. Keep unrelated follow-ups separate, stacked only when dependent. Do not create commits unless requested or already authorized.
- Default subjects are short, descriptive and unprefixed; project rules may override. No tool/model names, generated-with lines or attribution trailers in commits or PR text.
- Inspect staged changes and preserve user edits. Run relevant tests/lint and all applicable nonvisual CI checks before a PR. Inspect aggregate commands first; if they invoke forbidden system/browser/UI suites, run their nonvisual equivalents without changing CI configuration or deleting existing tests. Verify UI through browser inspection and asset build. Report excluded/unrun checks and failures; never label a filtered run as full CI.
- Fold fixes into unpushed commits only when history cleanup is authorized. Never rewrite pushed history or bypass hooks without explicit permission.
- Work remains local until the user asks to push/open a PR. Opening an authorized PR includes the first push. Later pushes each need explicit authorization unless the user has authorized ongoing pushes. Never force-push implicitly.
- Build the title/body from all branch commits and the full diff. Default title: plain, under 70 characters. Body: a short paragraph explaining the behavior and reason, then one truthful check-result line. Follow a required repository template when present.
- Prepare a concrete reviewable result before requesting any approval actually needed for publication. Opening a requested PR does not require another approval merely for its prose; ask only if a material detail is unresolved. Do not publish with failing required checks without the user's informed approval.
