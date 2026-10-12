---
name: review-overengineering
description: Use when reviewing a diff for more machinery than the current requirement needs, such as speculative options, one-use layers, one-method classes, registries, or abstractions for hypothetical providers. Covers only over-engineering.
---

# Review Overengineering

Find machinery in the diff that the current requirement does not justify and name the simpler direct form.

## Scope

- This lens covers only excess machinery: abstraction, indirection, configurability and generality beyond what the requirement needs.
- Leave style, naming, duplication, shared-code placement, conventions and correctness to other lenses and do not report them.
- Read the repo guidelines (AGENTS.md, CLAUDE.md or equivalent) you were pointed to before reviewing.
- Review only the diff scope you were given, plus the code that the diff touches.
- Apply `../principles/SKILL.md`.

## What to look for

- Options, parameters, hooks, config keys or extension points that no caller uses today.
- Service, wrapper, adapter, decorator, form or query objects that only delegate to one call.
- Classes with one public method where a plain function or method on an existing object does the job.
- Registries, DSLs, plugin systems or metaprogramming where straight code reads fine.
- Abstractions built for hypothetical providers, scale, or future reuse.
- State machines or generic lifecycle handling for two states.
- Defensive checks for cases the framework, the type system or the callers already prevent.
- Compatibility shims, aliases or deprecation paths for callers that do not exist in this repo.
- Interfaces with a single implementation and no planned second one in the diff.
- New dependencies in the diff, including `Gemfile`, `Gemfile.lock`, `config/importmap.rb` and any `package.json`, that a small own implementation or existing code could replace.

## What is NOT a finding

- Complexity the requirement actually demands, such as concurrency, security or external integration constraints.
- Boundaries and layers that the repo already established and uses consistently.
- An abstraction with a real second caller that exists today in the repo.
- Framework-mandated structure, such as required base classes or generated code.
- Preference for a different but equally simple style. Only report when the simpler form is clearly less machinery.

## Report

- Return findings exactly as specified in `../review/references/finding-format.md`.
- For each finding, name the machinery, state why the current requirement does not need it, and suggest the simpler direct form.
- Stay read-only: do not edit files, run git, or change state.
- Try to falsify each finding first by searching for callers and requirements. Drop the finding if a real caller or requirement exists.
