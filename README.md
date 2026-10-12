# logven-skills

Private, versioned agent skills for Logven's Rails workflow.

The sibling Logven checkout discovers them through its ignored local link:

```text
logven/.agents/skills -> ../../logven-skills/skills
```

Keep workflow source files in `skills/`; do not track `.agents/` or the symlink in Logven.

## Skills

- **Workflow**: `plan`, `plan-feature`, `delegate`, `verify-and-commit`, `pull-request`
- **Principles**: `principles` (minimalism and dependency rules)
- **Review**: `review`, `review-overengineering`, `review-over-standardisation`, `review-conventions`, `review-cleanliness`, `review-correctness`
- **Plan critics**: `plan-simplicity`, `plan-future-proofing`, `plan-edge-cases`, `plan-fit`
- **Rails**: `design`, `frontend`, `generate-tests`
