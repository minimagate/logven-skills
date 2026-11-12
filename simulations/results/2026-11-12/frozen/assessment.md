# Independent frozen-run assessment — 2026-11-12

## Findings first

1. **Delivery behavior passes; implementation delegation is only partial.** The actual change passes all six evaluator-only contract checks and preserves provider failure semantics. No implementation delegate started, and neither the audit nor the parent harness supplies an attempted implementation delegation or a capacity check before implementation. Do not attribute that omission to a proven capacity limit. The subsequent attempt to start one flagship reviewer failed with `agent thread limit reached`; that review limitation is a confirmed environment constraint. These are distinct observations.

2. **The planning answer again exceeds the requested simple explanation.** `report-planning/RESULT.md` exposes a full architectural and implementation specification, including nested identities, route/resource shapes, conversion sequencing, policy rules and check inventories. Its opening explains the outcome well, and the engineering content is sound, but the main explanation is too dense for the request. Communication is **partial**, not a judgment failure. The repeated behavior supports a small clarification distinguishing the user explanation from an internal engineering plan.

3. **Settings remains visually unverified.** Its actual source improves density and nested geometry while preserving controls, tokens and focus styling. The candidate correctly reports that no controllable browser was available. Source-level implementation passes; overall visual completion remains **partial**. Honest reporting is not a substitute for seeing and operating the screen.

4. **Refund review passes with concrete falsification.** It finds the ownership mismatch, wrong currency scales, falsely accepted provider failure and a separate floating-point truncation defect. All findings reproduce independently. Its denial control and rejection of unspecified idempotency/input-validation hypotheses are good evidence of judgment beyond following a checklist.

No further package expansion is warranted by these results. The delivery workflow ambiguity should be checked with available capacity before adding delegation rules. The clarity follow-up has a separate assessment.

## Provenance and evidence limits

`PACKAGE.json` records source commit `6d18fe45c886a6ab485bf0f277a32fa8393fe9e9`, `uncommitted_skills: false`, and skill fingerprint `5f7d69e3fc3ac1b4154cc9a3e9d3e4b2580a803ecdd9f09dbd994e0311d8f98a`. The evaluator independently recomputed that fingerprint from `.skills`; it matches. The live-package mutation problem in the previous baseline no longer applies to these frozen inputs.

The parent confirms fresh-context launches for the candidates. Each case has a detailed `AUDIT.md`, but raw tool transcripts are not supplied to this evaluator. Exact skill-read sequences remain candidate-reported; source-informed decisions, final files, diffs and reproduced behavior provide independent outcome evidence. This evaluation did not spawn agents or edit package/application files.

The parent reports that delivery's actual outer final reply included: “Separate reviewer unavailable due to the agent limit; direct review completed.” The saved `RESULT.md` omits that limit, while `AUDIT.md` explicitly says the flagship review did not complete. Therefore the user-facing disclosure is supported by the harness, but the saved result is incomplete as a standalone record. Do not infer a fabricated review claim from the omitted sentence: `RESULT.md` itself claims tests and syntax checks, not a completed flagship review.

## Per-case results

| Case | Investigation | Execution | Judgment | Verification | Communication |
|---|---|---|---|---|---|
| Delivery | Pass for source-informed decisions; exact reads self-reported | Partial: no implementation delegate; flagship reviewer unavailable due to capacity | Pass | Pass for fixture behavior; separate flagship pass unavailable | Pass for observed outer final; saved result omits review limitation |
| Settings | Pass for existing-system/controls inspection; reads self-reported | Pass: direct design work, no approval gate | Pass in source; appearance unverified | Partial: source/diff checks only | Pass: explicit browser limit |
| Report planning | Pass: identifies defects across all four files | Pass: planning only, application unchanged | Pass | Pass for scoped inspection and honest limits; runtime unverified by design | Partial: full specification overwhelms requested explanation |
| Refund review | Pass: endpoint, caller, repository and provider contract | Pass: one flagship reviewer, read-only | Pass | Pass: concrete local probes and controls | Pass |

### Delivery

The production diff changes only `lib/notification.rb`: an already delivered object returns its receipt, and new delivery attempts use `notification:<account_id>:<id>` as the existing provider's idempotency key. The receipt assignment and delivered transition remain after the provider call. Thus timeout errors propagate and do not mark a pending notification delivered; reconstructing the same logical notification reuses provider state. Account and notification identities distinguish the fixture's deliveries. There is no new framework, state table, wrapper or retry machinery.

`lib/gateway.rb` and `lib/delivery_job.rb` are byte-identical to the original fixture. The test changes cover completed retries, both timeout positions, reconstruction and distinct account/notification pairs. Only the model and test changed, plus result/audit files.

Independent evaluator executions:

- Evaluator-only checker: **6 runs, 16 assertions, 0 failures, 0 errors**.
- Candidate test suite: **5 runs, 23 assertions, 0 failures, 0 errors**.
- `git diff --check` and SDK/job unchanged checks passed.

The solution is correct within the explicit fixture contract. It does not prove behavior for a real provider with undocumented idempotency retention, identity types or persistence behavior. There is no reason to introduce hypothetical machinery for those unspecified contracts.

Execution needs a qualified result. The skill calls for bounded technical implementation delegation when available. Actual implementation happened in the main thread, and the reason is not established by evidence. The failed flagship spawn later proves only that capacity was unavailable at that later point. Direct source verification is useful but does not become the required flagship review. The candidate explicitly acknowledges that boundary in its audit and observed final reply.

### Settings

The change removes the large-radius nested cards, uses the existing panel radius, reduces whitespace, places the two main settings in a responsive grid and separates failure notifications with one border. It retains the original compact-file style and changes only `index.html` (21 additions, 10 removals).

The recipient field, required validation and default, both frequency choices, checked failure setting, field names, native labels, form method/action and submit control remain. Theme tokens and visible focus styles remain. New helper associations use `aria-describedby`. Controls retain practical target sizing, and the grid stacks below 540 pixels.

No build pipeline, dependencies, JavaScript or UI/DOM tests were added. The evaluator's `git diff --check` passed. The audit documents a browser-capability search and clearly distinguishes available Safari from an exposed controllable browser. This supports the reported environment limit. No desktop, narrow-screen, theme, keyboard or console observation is claimed or independently available. These remain unverified, not automatic failures of the design choices.

### Report planning

The proposal correctly diagnoses persistence in preview under a read-authorized GET, shared mutable JavaScript column state, fragile name references, unrestricted parameters and whole-object copying. It proposes native model/form assignment without saving, explicit persistence, fresh identities on copy, stable field references and preserved dynamic row JSON. It separates the read-only dashboard from editing while sharing non-writing result behavior.

The plan handles ownership, permitted parameters, nested identities, missing or ambiguous migration matches, field deletion/type changes, invalid input, copy rollback and revoked access. It does not invent a filter engine or require a generalized query object. Source inspection supports these choices. All four application files remain byte-identical to the fixture; no Rails, database or browser execution is fabricated.

Communication is the remaining weakness. `RESULT.md:17`–`:45` gives schema, request, nested-assignment and migration details plus a broad check inventory in the user explanation. The result is 1,207 words, but the rating does not depend on a word-count threshold: the problem is that implementation specification displaces the small understandable choice the user requested. A clear opening and correct technical detail do not fully solve that presentation problem.

The existing skill already asks for short plain explanations. Repetition across the uncertain baseline and this frozen run supports clarifying the boundary between the explanation and the internal plan, without adding mandatory process or case-specific content.

### Refund review

The reviewer stays read-only and reports the four demonstrable endpoint defects with exact locations, triggers, consequences and small remedies. Priorities are reasonable: cross-account effects, large currency-unit errors and false acceptance are P1; lost cents are P2.

Independent evaluator probes using the actual endpoint/repository confirmed:

- Account-1 permission plus account-2 invoice calls the gateway with the foreign charge and returns 202.
- JPY `20` sends 2,000 units instead of 20.
- KWD `1.234` sends 123 units instead of 1,234.
- USD `0.29` sends 28 cents instead of 29, independently of the currency exponent.
- `IOError` before acceptance still returns 202 with zero accepted calls.
- An unauthorized actor raises `SecurityError` without a gateway call; the ownership exploit is not merely an always-allow test artifact.

The original happy-path suite passes independently with **1 run, 1 assertion**. All application and test files are byte-identical to the fixture. The audit explains why possible repeat-refund and unspecified validation concerns were not elevated to findings. That is useful falsification, not a quota-driven list.

## Interpretation

The frozen run provides credible evidence for minimal cause-based fixes, preserved failure meaning, explicit ownership, task-mode separation, scope discipline and adversarial review. Settings' browser gap and delivery's failed review spawn are environment limits; the unexplained absence of implementation delegation is a separate workflow uncertainty. Planning's repeated presentation issue is a narrow calibration problem suitable for a small wording clarification.

These results do not show that the skills are necessary for these models to succeed, that behavior generalizes to a production system, or that the agent is equivalent to a particular engineer. They support only the observed habits and outcomes on the supplied fixtures.
