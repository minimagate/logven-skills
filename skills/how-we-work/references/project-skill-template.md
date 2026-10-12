---
name: project-<name>
description: Use only when working in the <Name> repo. <Name>'s project-specific names, paths, helpers and decisions. Read together with the general rails-* skills and how-we-work; it overrides general defaults where they differ.
---

<!--
Delete this comment after copying. Copy this file to skills/project-<name>/SKILL.md, replace every <placeholder>, delete
sections that do not apply. Record only facts true for this project. Also add skills/project-<name>/agents/openai.yaml:

interface:
  display_name: "Project <Name>"
  short_description: "<Name>-specific names, paths and decisions"
  default_prompt: "Use $project-<name> for <Name>'s project-specific conventions alongside the general rails-* skills."

Optionally add references/design.md for the design system.
-->

# Project <Name>

<One sentence: what the app is and what it is for.>

## How to use

- General rules live in the `rails-*` skills and `how-we-work`. This file holds only what is specific to <Name>.
- Where this file and a general skill differ, this file wins. Visual specifics go in [references/design.md](references/design.md) if present.

## Structure and naming

- <Domain namespaces, table naming, where non-domain infrastructure lives.>
- <Existing shared mechanisms to reuse instead of adding parallel ones.>

## Models

- <Shared concerns and their declaration order; status column and constant convention.>
- <Transition methods and the predicates that guard them.>

## Controllers and routes

- <Base controllers and the class macros they provide; how nested records are loaded.>
- <How state changes are modelled as resources.>

## Authorization

- <Which controllers opt out, and the default policy stance.>
- <Policy naming convention and role rules.>

## Migrations

- <Schema-only or backfill stance; migration class version; table naming.>
- <Verify commands.>

## Frontend

- <Stack and importmap pins, each with its reason.>
- <Partial names, shared UI helpers, build command.>

## Tests

- <Builders and where they live; stubbing helpers for external calls.>
- <Test commands and environment setup.>

## Commits and PRs

- <History style: subject wording, body use, housekeeping commits.>
- <Layer order for features and PR description contents.>

## Known legacy exceptions (do not copy)

- <Pattern that exists in the code but must not be copied, and why.>
- <Second legacy pattern, or delete this bullet.>
