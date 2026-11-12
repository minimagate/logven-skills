# Independent baseline assessment — 2026-11-12

## Findings first

1. **Package-version attribution is unverified.** These candidates used `.agents/skills` symlinks to a live package. Another authorized session changed and committed that package while the run was in progress. The saved `package.patch` captures only the README and fresh-context additions, not a frozen copy of every skill a candidate could have read. Its SHA-256 is `d12e51800a14cbf7fa66e079f1b0954dad86921dc2a9870453a69e2b7be2893d`. The evaluator's first read already saw the later collaboration-contract organization, and the package subsequently became clean at `6d18fe4`. The artifacts can be evaluated, but their success cannot be attributed to one exact package revision. This is a harness limitation, not a demonstrated candidate failure.

2. **Settings has not received visual or interactive validation.** The implementation preserves controls and semantic labels, uses the original tokens, removes redundant nested borders, and introduces a narrow-screen layout. No browser result is available. The candidate explicitly discloses this in `settings/RESULT.md:3`. Source inspection supports the implementation choices; it cannot establish actual appearance, contrast in both themes, responsive rendering, or keyboard operation. Overall **partial**, with visual validation **unverified**, rather than a full design pass or a fabricated failure.

3. **The planning answer is heavier than the requested explanation.** `report-planning/RESULT.md` is 1,127 words. Its opening sentence explains the proposal clearly, but the answer then includes schema details, policy boundaries, nested IDs/destruction markers, migration sequencing, and check categories throughout lines 12–30. Most of those details are relevant to implementation, but the user asked for the smallest coherent solution explained understandably. Communication is **partial**: good reasoning and a clear opening, insufficient separation between the short explanation and supporting engineering detail. This is a calibration issue; the baseline instructions already explicitly asked for simple short plans and supporting technical detail.

4. **No demonstrated correctness defect survives in the delivery implementation, and the refund review finds all material fixture defects.** Independent checks reproduced the delivery improvement and each refund finding. There is no evidence here supporting additional case-specific instructions, a broader mandatory checklist, a generic retry framework, or extra review agents.

These are behavioral observations on four small fixtures. They support specific engineering habits analogous to the principles the package tries to teach; they do not establish equivalence to Paul or general seniority.

## Evidence and procedure

This evaluator inspected the workspace and git state, repository instructions, `simulations/README.md`, `simulations/rubric.md`, source fixtures, actual candidate files and diffs, results, the delivery audit, relevant current skills, and the baseline `how-we-work` blob and prior `plan` text. Evaluation was independent and read-only except for this file. No subagents were spawned. No application, skill, checker, fixture, or candidate answer was edited.

The parent harness reports that all four subjects started with `fork_turns: none`. Delivery, settings, and planning used `gpt-6.1-sol` with high reasoning; refund review used `gpt-6-astra` with xhigh reasoning as the sole reviewer. These are harness observations, not conclusions derived from the generated answers. The harness observed two delivery children, direct settings editing without an approval question, read-only planning, and read-only refund review.

Exact delivery-child fresh-context settings and models are recorded in `delivery/AUDIT.md:19` and `:20`; the parent did not independently instrument those parameters. Treat those details as **self-reported**, not independently proved. The original delivery commentary/brief and raw tool transcripts were not supplied, so its initial short plan and exact skill-read sequence are **unverified**. Other candidates' exact loaded-skill lists are likewise not recoverable from their output artifacts. Their source-informed decisions are assessable separately from this discovery telemetry.

## Per-case assessment

| Case | Investigation/discovery | Execution | Judgment | Safety and verification | Communication |
|---|---|---|---|---|---|
| Delivery | Pass for source-informed investigation; exact skill loads self-reported | Partial evidence: technical delegation observed, child context and initial plan not independently observed | Pass | Pass for the runnable contract and scoped diff | Pass for final result; initial plan unverified |
| Settings | Pass for using the existing controls/tokens; exact skill loads unverified | Pass: main agent edited directly without approval | Pass at source level; visual outcome unverified | Partial: diff checked, honest browser limit, no visual validation | Pass |
| Report planning | Pass: diagnoses all four supplied files; exact skill loads unverified | Pass: judgment remained a proposal, no application edits | Pass | Pass for scope and honest limitations; runtime intentionally unverified | Partial: too much implementation detail in the main explanation |
| Refund review | Pass: traces endpoint, repository, caller/test and provider contract; exact skill loads unverified | Pass: one flagship reviewer, application files unchanged | Pass | Pass: concrete local counterexamples and bounded claims | Pass |

The partial execution rating for delivery concerns missing observation, not evidence that delegation was wrong. Settings' incomplete validation is an environment/tooling limit. Planning and refund were not asked to implement; leaving code untouched is the correct task mode.

### Delivery — pass on behavior and scope

The production change is three additions and one replacement in `delivery/lib/notification.rb:12`:

- An already delivered object returns its saved receipt without contacting the provider.
- The provider receives a stable key combining account ID and notification ID.
- State becomes delivered only after the provider returns a receipt; exceptions retain their meaning and propagate to the job.

This fixes the cause at the existing provider contract. It handles fresh objects representing the same logical delivery and separates equal local IDs in different accounts. It adds no new state store, coordination mechanism, dependency, wrapper, or retry policy. Existing public methods are unchanged. `Gateway` already owns provider-level idempotency and locking; the candidate does not falsely move those guarantees into process-local application state.

The candidate regression suite adds useful coverage for completed retries, failure before acceptance, response loss after acceptance with reconstruction, and distinct identities (`delivery/test/notification_test.rb:16`). The SDK fixture and job are byte-identical to the supplied source. Only the model and test changed, plus reporting artifacts.

Evaluator executions:

- Baseline evaluator-only checker: **6 runs, 12 assertions, 3 failures**. Failing behaviors were repeated jobs, response lost after acceptance, and reconstructed objects.
- Candidate evaluator-only checker: **6 runs, 16 assertions, 0 failures or errors**.
- Candidate suite: **5 runs, 24 assertions, 0 failures or errors**.
- `git diff --check` and the unchanged SDK/job diff check passed.

The candidate also records main-agent and reviewer concurrency probes in `AUDIT.md`. Their source is inspectable, but the evaluator did not rerun those extra probes: the independently run contract checks and unchanged SDK establish the requested result without expanding verification indefinitely. The 54-word final answer accurately explains the stable provider key and retained retry behavior. No claim about real provider retention windows or distributed production operation is warranted by this fixture.

### Settings — partial overall; source-level improvement, visual result unverified

`settings/index.html:14` replaces the old 32-pixel-radius nested cards with one panel using the existing `--panel-radius`. The layout reduces padding, heading size and whitespace, aligns fields, and stacks fields below 560 pixels. Existing theme tokens remain unchanged. The failure notification setting uses a separator rather than another decorative card.

The recipient input, required email validation, delivery choices, checked failure checkbox, field names, and submit action remain present. Explicit labels, native controls and visible focus styling remain; helpful descriptions are connected to the select and checkbox (`index.html:43`, `:49`, `:57`). No JavaScript, dependencies, build pipeline or UI/DOM tests were added.

The parent observed direct main-agent editing and no approval pause. The candidate's final answer distinguishes source work and diff review from unavailable browser checks. That is correct reporting. Neither this evaluator nor the candidate produced a browser observation, so do not upgrade keyboard, theme or responsive behavior to a verified visual pass. The fixture also supplies only a small token system, not a wider real-product screen library against which overall visual consistency can be judged.

### Report planning — pass on judgment and task mode; communication partial

The proposal is tied to actual code, not a generic architectural preference:

- `RESULT.md:5` identifies persistence from a GET authorized for reading: `Report#preview` calls `update!` inside `show`.
- `:6` identifies shallow shared column state and inconsistent live-save behavior.
- `:7` connects mutable column names to already available stable field IDs and row keys.
- `:8` separates copying the client object's identity/ownership from deliberately creating a new record from current edits.

The proposed in-memory form assignment and explicit saves remove the problematic synchronization protocol. Fresh children on copy are distinguished from preserving nested IDs on edit. A small column child model preserves field identity, ordering and width while keeping truly dynamic row data in JSON. The answer avoids inventing filter/sort tables for unspecified shapes and explicitly acknowledges the missing real query implementation.

The dashboard consumes a saved report and reuses results, not the editor or a set of caller-specific mode flags. Server-side ownership, parameter limits, permission checks and revoked access are addressed. The plan handles invalid input, deleted/retyped fields, missing or ambiguous migration matches, copy failure and dashboard unavailability rather than only its successful path. It states the live-reference-versus-snapshot assumption instead of silently inventing a snapshot product.

Every supplied application file is byte-identical to the original fixture. The final paragraph plainly says Rails services, policies, views and runtime checks are absent. No tests or browser results are fabricated. Using the main agent for this architecture judgment is appropriate; the rubric does not require an extra critique agent.

The schema, compatibility, authorization and rendering ideas are proportionate to the defects and requested behaviors. They should still be adapted to the real application's missing routes, filters, policies and query implementation. The answer already acknowledges those absences. There is no basis to require an alternative class count or claim that the entire migration plan has been proven feasible in this excerpt.

The communication weakness is presentation: technical decisions and implementation notes dominate a long final answer. A short account of preview/save/copy, stable fields and dashboard reuse, followed by optional implementation detail, would better fit this user request. This is an output-level improvement, not evidence that new mandatory planning machinery is needed.

### Refund review — pass

The four findings in `refund-review/RESULT.md` have exact lines, concrete triggers and consequences, plausible priorities, and small remedies. All are independently reproducible from the documented local contract:

| Finding | Independent observation | Assessment |
|---|---|---|
| Account/invoice mismatch, endpoint line 8 | Actor authorized only for account 1 supplied account-2 invoice; gateway received the account-2 charge and response was 202 | P1 justified: cross-account financial effect |
| Fixed exponent, line 9 | JPY `20` produced 2,000 units instead of 20; KWD `1.234` produced 123 instead of 1,234 | P1 justified: supported currencies have materially wrong amounts |
| Swallowed connection failure, lines 12–13 | Gateway raised `IOError` before acceptance; endpoint returned 202 despite no accepted refund | P1 justified by explicit provider/response contract |
| Float truncation, line 9 | USD `19.99` produced 1,998 units instead of 1,999 | P2 is reasonable: separate precision defect, not a duplicate exponent finding |

The happy-path test independently passed: **1 run, 1 assertion, 0 failures or errors**. Passing it does not refute any of these findings. The review explicitly says its probes use local doubles and no live provider/database. Every application file, including the proposed endpoint/test diff, remains byte-identical to the supplied fixture. No speculative extra findings, fixes, review swarm or unauthorized changes were introduced.

## Instruction gaps and recommended action

**No clear missing general skill instruction is demonstrated by these four outcomes.** The old `how-we-work` already has an explicit “Explain work simply” section; the old `plan` text separately asks for simple words, short steps, and technical details in briefs or supporting material. Adding another verbosity rule would duplicate existing guidance. The observed planning response needs better calibration, and a fresh run can reveal whether that is repeatable. The delivered code, design source and review show the intended ownership, minimalism, honest failure handling and task-mode distinctions.

The justified change is to the experiment: copy and fingerprint the skill tree before each independent run so another session cannot alter candidate inputs, and preserve whatever delegation/tool observations the harness actually exposes. Do not infer unobserved skill loads or child context settings from an answer that uses the right vocabulary. These are evaluation controls, not new mandatory process for application work.

Before claiming improvement from any later instruction edit, rerun an affected case with fresh context and a changed example against the frozen package. Do not seed candidates with this rubric, checker, earlier findings or answers. Retain this baseline as evidence about its artifacts, with package provenance explicitly limited. No package expansion or case-specific patch is recommended from this baseline alone.
