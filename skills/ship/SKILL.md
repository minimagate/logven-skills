---
name: ship
description: Slice authorized work into coherent commits and PRs, verify local checks, and write concise history from the actual diff. Controls push and publication boundaries.
---

# Ship

Deliver a coherent, verified change with history that explains the resulting behavior. Read branch history and the full diff against its base; follow project conventions and existing authorization.

## Delivery boundaries

| Action | Authorization |
|---|---|
| Create commits | Requested or already authorized |
| First push with a requested PR | Included in the PR request |
| Push or later update | Explicit authorization for that push, or ongoing push authorization |
| Rewrite pushed history, force-push or bypass hooks | Explicit permission |
| Publish with failing required checks | User's informed approval |

Work stays local until push or PR publication is authorized. Prepare a concrete reviewable result before seeking any approval still needed. A requested PR does not need another approval for its prose; ask only for unresolved material details.

## Shape the change

Give each commit and PR one coherent concern. Sequence necessary preparation, schema/domain contracts, integration, HTTP/policies and complete UI. Tests travel with the behavior they protect. Separate pure moves from edits when useful; avoid empty skeletons and a commit for every method.

Keep unrelated follow-ups separate and stack only dependent work. Remove superseded paths within scope. Fold fixes into unpushed commits only when history cleanup is authorized.

## Verify the result

Check each changed line against the request. Trace one complete user path through ownership/permissions, submitted state and failure response. Passing checks alone do not prove a working flow. Remove orphaned paths, speculative knobs and unnecessary layers created by the change; preserve user edits.

Before committing or publishing, run relevant tests/lint and applicable nonvisual CI checks. Inspect aggregate commands first: if they invoke forbidden system/browser/UI suites, run nonvisual equivalents without changing CI or deleting tests. Inspect UI in the browser and run the asset build. Report excluded/unrun checks and failures; never label filtered checks as full CI.

## Write and publish

Stage only work within the authorized scope, even if a generic git helper proposes staging everything. Inspect staged changes before committing. Default subjects are short, descriptive and unprefixed unless project rules override. No tool/model names, generated-with lines or attribution trailers in commits or PRs.

Build the PR title and body from all branch commits and the full diff. Default to a plain title under 70 characters and a short paragraph explaining behavior and reason, followed by one truthful check-result line. Explain meaningful representation or ownership changes so removed glue is reviewable. Follow required repository templates.

After an authorized commit or push, verify the resulting git state and report what was delivered, checks and material limits.
