# Behavioral simulation results — 12 November 2026

The agents showed sound engineering judgment on these small exercises: they fixed a retry bug with very little code, found serious defects despite a green test, proposed coherent ownership and edit boundaries, and kept design work direct. Planning explanations were too detailed; a small general clarification produced a clearer answer on a fresh related request. These observations support the package, but do not establish equivalence to Paul or reliable performance on arbitrary work.

## What was exercised

Four task types ran in fresh independent contexts: a runnable Ruby delivery bug, a static settings redesign, architecture planning over a Rails excerpt, and a read-only refund review. Ordinary task agents used a capable reasoning model; refund reviewers and the independent evaluator used a flagship model. Candidates received their task, raw workspace and discoverable skills, without the evaluator rubric, checker or previous answers.

The initial four runs used live skill links. Another authorized session changed and committed the package during execution, so those results are exploratory and cannot be attributed to one version. The preparer now freezes and fingerprints the skills before launching candidates.

All four tasks were repeated against clean commit `6d18fe4`, frozen fingerprint `5f7d69e3fc3ac1b4154cc9a3e9d3e4b2580a803ecdd9f09dbd994e0311d8f98a`. A further planning trial and delivery rerun used the two small communication clarifications, fingerprint `5873cbb4c6350e30e86130e719876805e65254eeb57364edbf8e5a28907dccbb`. Both fingerprints were independently checked. No live application, notification, payment or database operation was performed.

| Task | Observed result | Qualification |
|---|---|---|
| Delivery | Every candidate passed six independent behavioral checks: repeats, both timeout paths, reconstructed objects and distinct account/notification identities. The unfixed fixture fails three. Production fixes took one or three added lines; SDK and job remained unchanged. | Uses a contract double, not a live provider or durable database. |
| Settings | Direct edits, no plan-approval pause, existing controls/theme tokens preserved, awkward nested surfaces removed. No UI/DOM tests added. | Source-level result only; browser appearance and keyboard interaction remain unverified. |
| Report planning | Correctly identifies mutating previews, shallow-copy aliasing, fragile name references and unsafe parameters. Proposes explicit saves/copies, stable identities, dynamic row JSON and ownership checks without changing application files. | Rails/database integration was not executable in the excerpt. Original explanations were too detailed. |
| Refund review | Both flagship runs found and reproduced cross-account refunds, wrong currency scaling, floating-point under-refunds and false acceptance after connection failure. The supplied happy-path test passes. | Local probes, not a live payment integration. |

## Adjustments and follow-up

- **Fresh context:** every harness-launched agent used `fork_turns="none"`. The skills explicitly require this for all delegates. Nested settings are recorded in candidate audits; raw nested-call transcripts were not independently captured.
- **Reproducibility:** live links were replaced by frozen copies and a `PACKAGE.json` fingerprint. Existing-run overwrite is rejected; later source edits do not change an active run.
- **Communication:** the only skill adjustment separates a short user-facing recommendation and steps from detailed internal engineering plans, retaining material decisions and risks. It contains no case-specific solution. The changed-request trial was clearer and shorter, with the important safeguards preserved. Task scope also changed, so this is not a controlled causal comparison or justification for a word limit.

One frozen delivery run implemented directly and could not start its flagship reviewer because of the agent limit. Its audit disclosed the review gap; implementation delegation was not established in that run. A final rerun with available capacity documented a fresh implementation delegate and one fresh flagship reviewer, passed all six independent checks, and left SDK/job unchanged. No extra workflow rule was added to explain away the earlier omission.

## Evidence and remaining limits

See the [frozen assessment](frozen/assessment.md), [clarification assessment](clarity/assessment.md), candidate answers/audits and actual patches beside them. The [rubric](../../rubric.md) grades decisions and artifacts rather than keyword matching. Reproduce the runnable check with:

```sh
ruby simulations/check_delivery.rb <completed-delivery-workspace>
```

These were small fictional tasks, not production integration tests. There was no no-skills control, no visual browser validation and no long-term maintenance exercise. The evidence demonstrates behavior with these skills; it does not measure how much the skills caused it. Keep further changes tied to repeated observed failures rather than adding rules for every fixture.
