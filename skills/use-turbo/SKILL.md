---
name: use-turbo
description: Add or change Logven Turbo Frames, Turbo Stream responses, model broadcasts, morph refreshes, or small Stimulus behaviors. Use for inline editing, collection insertion/removal, async build/run progress, stable Turbo targets, drag-and-drop persistence, menus, toasts, and other server-driven browser interactions.
---

# Use Turbo

Keep Rails authoritative and choose the narrowest Turbo mechanism that updates the required UI.

## Choose the Mechanism

1. **Normal navigation/redirect** — use when the whole page changes and no partial interaction is needed.
2. **Turbo Frame** — use when one stable record region switches between display and form states.
3. **Turbo Stream response** — use when the initiating request must mutate one or more explicit targets.
4. **Broadcast replace** — use when an async or cross-request record update has one independently renderable target.
5. **Broadcast refresh/morph** — use when several page regions depend on an aggregate and targeted replacement would duplicate orchestration.
6. **Stimulus** — add only the remaining ephemeral browser behavior; persist through Rails forms.

Read [`references/frames-and-streams.md`](references/frames-and-streams.md) for request-driven interactions. Read [`references/broadcasts-and-stimulus.md`](references/broadcasts-and-stimulus.md) for asynchronous updates or JavaScript behavior.

## Workflow

1. Trace the record, controller response, subscribing page, partial boundaries, and any existing Stimulus controller.
2. Reuse `turbo_id`, existing partials, and an existing stream/broadcast pattern before adding another target or response path.
3. Preserve a functional HTML path unless the action is deliberately Turbo-only.
4. Keep lifecycle and authorization on the server. Turbo chooses delivery, not whether an operation may occur.
5. Use `create-component` for markup ownership decisions and `generate-tests` for non-visual contracts.
6. Build Tailwind when markup introduces new utilities/classes and verify the interaction in the browser.

## Do Not

- Do not duplicate persisted state in JavaScript.
- Do not introduce custom DOM IDs when `turbo_id` or `dom_id` already expresses the target.
- Do not broadcast before commit.
- Do not add a Stimulus controller for a normal link, form, frame, or stream operation.
- Do not add DOM, stream-markup, selector, or system tests; exercise those details in browser verification.
