---
name: rails-frontend
description: Implement server-rendered Rails UI with ERB, Turbo, Stimulus, Importmap, and Tailwind (ViewComponent only when earned). Use for views, partials, components, Turbo Streams, browser behavior, or accessibility; pair visual changes with rails-design; hands controller, route and policy questions to rails-controllers and rails-authorization.
---

# Rails Frontend

ERB and Rails helpers for markup, Turbo for navigation and updates, small Stimulus controllers for behavior the server cannot express. No client state framework, JSX layer, npm build, or parallel component system.

Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs, it wins.

Before any visual change, read `../rails-design/SKILL.md` completely and apply it here.

## Choose the smallest UI owner

- Use the lightest tool that works, in order: native HTML (popover, dialog, details, select), Turbo or server action, plain partial, shared CSS class, Stimulus, ViewComponent. A component that only maps props to classes is a CSS class.
- Use the smallest server-rendered change; extend an existing owner first.
- Keep controller-scoped fragments as partials under that controller's view directory. Use a top-level ViewComponent in `app/components/` only for reusable structured UI with multiple independent callers or a meaningful slot API.
- Use a helper only for small formatting or tag logic that owns no visual structure.
- Derived data and state predicates live on the model; complex queries stay in the controller (see `../rails-models/SKILL.md` and `../rails-controllers/SKILL.md`).
- Partials live under the resource they render. Follow the project's partial naming; by default `_show` is the canonical per-record partial, reused by show pages, streams and collections, and `_form` is the form.
- Use the project's `content_for` keys for page chrome if it defines them, not ad-hoc layout logic.
- Every partial that takes arguments declares strict locals (`<%# locals: (x:, y:) -%>`). No mode flags (such as `compact:`) that transform a partial.

## Work with Turbo

- Keep the layout's morph/refresh meta tags and DOM identifiers stable.
- Take every Turbo target id from one helper: `dom_id` in a fresh Rails app, or the project's id helper if the project skill names one. Never hand-write id strings. Composite ids append a suffix (`-details`, `-destroy`, `-editor`); the stream template and the partial use the same id.
- Use one Turbo Stream template per controller action (`create`, `update`, `destroy`) for interactions that replace known fragments, rendering the same `_show` and `_form` partials as the full pages. Keep ordinary redirects for full navigation. Whether Turbo Frames are used is a project decision.
- Subscribe with `turbo_stream_from` only to records that broadcast relevant updates. Background-updated records use model-level `broadcasts_refreshes_to`; never broadcast interactive cards.
- Mark permanent elements only when their client state must survive morphing.
- Keep nested `form_with` model arrays aligned with the route hierarchy.

## Keep Stimulus narrow and accessible

- Controllers manipulate their own element through declared targets, values and actions. Clean up timers, global listeners and third-party instances in `disconnect`.
- Dispatch bubbling `change` events when another controller or form owns autosave.
- Keep controllers generic and composable (for example `autosave` + `sortable`), each responsible for one behavior. Never branch on a known id or page (`if (id === "...")` means the design is wrong) and never hard-code feature-specific keys.
- Menus and custom selects keep `aria-expanded`, roles, keyboard navigation, escape behavior, outside click/focus closing and focus restoration. Prefer native controls when custom behavior adds no product value.
- Import browser dependencies through `config/importmap.rb`. Each new pin needs a stated reason; server rendering is preferred over a pin.

## Style at the correct layer

- Keep single-owner designs, including single-use styles, as inline Tailwind in the ERB. Do not add a `components/*.css` file or `@apply` class for one feature.
- Promote a class to the shared component stylesheet only for a real primitive (badge, button, input) or a pattern that multiple independent markup owners share.
- Add raw palette tokens, named semantic tokens and base/component rules in their established layers. Prefer a named token or scale utility to an arbitrary value. Arbitrary values are for structure only (grid templates, anchor positioning), never color.

## Keep frontend code lean

- No generic state layer, wrapper component or abstraction for a single interaction.
- Keep templates declarative and partial/component inputs explicit. Do not spread one state across ERB condition trees, data attributes, multiple controllers and CSS selectors.
- Do not duplicate non-visual contracts already tested in models, policies or controllers. Presentation tests are out of scope (see `../rails-tests/SKILL.md`).
- Remove `console.log`, temporary instrumentation and event chatter. Frontend failures become purposeful UI state or are reported once by the existing server-side boundary, never by logging DOM content or user data.
- If the project defines tone helpers, map state to tone through them and tone to class through its class helpers. Extend those helpers rather than branching in templates; unknown values fall back to a neutral tone.

## Verify in the browser

- Run the project's asset build (for example `bin/rails tailwindcss:build`).
- Check the affected interaction with the checklist in `../rails-design/SKILL.md` ("Review before finishing").
