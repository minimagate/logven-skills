# logven-skills

Private, versioned workflows for the Logven application. The sibling Logven checkout discovers them through its ignored local link:

```text
logven/.agents/skills -> ../../logven-skills/skills
```

Keep workflow source files in `skills/`; do not track `.agents/` or the symlink in Logven. See `skills/manage-logven-skills/SKILL.md` for the maintenance workflow.
