# Skill simulations

These are independent behavioral exercises, not tests for instruction wording. Fixtures use fictional domains and no production data. They check whether the package supports investigation, sound ownership, minimal changes and honest verification; they cannot establish equivalence to a particular engineer.

1. Run `python3 simulations/prepare.py /tmp/skills-simulation-<unique-name>`. The destination must be new. Each fixture becomes a temporary Git repository linked to a frozen copy of the skills. `PACKAGE.json` records its content fingerprint and source commit; later edits cannot silently change an active run.
2. Start one fresh-context agent per case. Give only its workspace and `TASK.md`, with ordinary task tools. It acts as the main agent for that isolated session; technical implementation may use fresh-context delegates. Never pass the rubric, checker, expected findings, earlier answers or the surrounding conversation. Limit writes to its workspace. The review case needs one flagship model; design stays with its main agent.
3. Preserve the candidate's final answer and actual diff. Record loaded skills, delegation/context choices, commands, outcomes and limitations from observable evidence. If the harness cannot observe something, mark it unverified.
4. After delivery work, run `ruby simulations/check_delivery.rb <delivery-workspace>`. Keep this evaluator-only checker outside candidate context. It tests nonvisual behavior. Inspect design manually if browser access exists; never add DOM or screenshot assertions.
5. Have one fresh flagship evaluator compare artifacts with the [rubric](rubric.md). Separate failures of the skills from fixture/environment limits. Small fixes must generalize; repeat an affected case with fresh context and a changed example before claiming improvement. A pass is evidence about these tasks, not proof of general seniority.

`delivery` is runnable Ruby; `settings` is a static design task; `report-planning` is a Rails excerpt without runtime services; `refund-review` is a read-only proposed diff. No live payments, notifications or deployments occur. Keep generated runs outside this repository.

Recorded run: [12 November 2026 results and limits](results/2026-11-12/REPORT.md).
