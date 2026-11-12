---
name: rails-frontend
description: Build or change Rails ERB, partials, Turbo, Stimulus and accessible interactions. Pair appearance work with rails-design; verify UI in the browser, never DOM tests.
---

# Rails frontend

Use [principles](../how-we-work/SKILL.md#principles) and [design](../rails-design/SKILL.md). Default to ERB, Rails helpers, Turbo and small Stimulus controllers; retain the project's existing stack.

- Use the fewest clear lines: existing primitives/native HTML, then server/Turbo and partials. Add Stimulus for behavior the server cannot express; ViewComponent for meaningful reusable structure. Preserve accessibility and product behavior; no parallel client framework or npm pipeline.
- Keep domain rules and queries with their model/domain owner. Templates compose explicit values; helpers format small values directly. Prefer safe deterministic formatting over redundant display configuration when no real user choice is lost. Reuse the canonical typed-field renderer instead of reimplementing input types per page; express genuine presentation differences through a small explicit contract. Resource partials use strict locals and are reused by pages and streams. Avoid mode flags that make one partial serve unrelated layouts.
- Generic UI primitives know only their mechanics: a dialog opens/closes; its caller supplies content, title and actions. Feature adapters handle feature behavior; no shared-controller branches on page IDs or domain types. Domain-specific shells retain required approval/error controls; custom content fills bounded slots and cannot replace those controls.
- Use native `form_with`/`fields_for`, nested attributes and server-rendered previews before bespoke draft state. Keep coherent form/URL state with boundary-specific allowlists: edits preserve child IDs and destruction markers; preview/copy endpoints do not automatically accept those identities. Avoid parallel state in hidden helpers or JavaScript.
- Use one established DOM-id helper everywhere. Preserve morph identifiers, layout refresh conventions and genuinely permanent client state. Keep forms aligned with nested routes.
- Streams use action templates and the same resource partials as ordinary pages. Prefer redirects for normal navigation. Broadcast only where background changes warrant it.
- Stimulus owns declared targets, values and actions; release timers, listeners and instances on disconnect. Compose independent behaviors through explicit events: sorting changes order; autosave decides persistence through bubbling change events when the form owns saving. Adding/removing unsaved rows must refresh derived/preview state just as changing an input does. Pagination must not teach unrelated components that a stream always means load-more.
- Prefer native accessible controls. Custom controls must support labels, keyboard, escape, outside closing, focus restoration and appropriate ARIA state.
- Single-owner styling stays with its markup; promote shared styles only for real shared primitives. Reuse semantic tokens and existing state/tone helpers. New importmap pins are dependencies and require approval.

Run the project's asset build and inspect the affected flow using the design checklist. **No UI/DOM tests**, including markup assertions inside controller tests; test extracted nonvisual rules under [rails-tests](../rails-tests/SKILL.md).
