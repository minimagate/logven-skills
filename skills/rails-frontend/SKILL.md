---
name: rails-frontend
description: Implement server-rendered Rails UI with ERB, ViewComponent, Turbo, Stimulus, Importmap, and Tailwind. Use for views, partials, components, Turbo Streams, browser behavior, or accessibility; pair visual changes with the rails-design skill.
---

# Rails Frontend

The application is server-rendered Rails. Use ERB and Rails helpers for markup, Turbo for navigation/replacement/refresh, and small Stimulus controllers for behavior the server cannot express. Do not add a client state framework, JSX layer, npm build, or parallel component system.

Avoid JavaScript whenever the same behavior can be implemented clearly with native HTML, CSS, Rails, or Turbo. Add JavaScript only when it provides necessary behavior that those tools cannot express, and keep it progressively enhanced so the underlying server-rendered flow remains usable whenever practical.

Before any visual change, read `../rails-design/SKILL.md` completely and apply it with this skill.

## Choose the smallest UI owner

- Keep controller-scoped fragments as partials under that controller's view directory.
- Use a top-level ViewComponent in `app/components/` only for reusable structured UI with multiple independent callers or a meaningful slot API.
- Use a helper for small formatting or tag-generation logic that does not own a visual structure.
- Keep record-derived display behavior on an existing model only when it is genuinely domain-facing and reused outside one template.
- Choose the lightest tool in this order: native HTML (popover, dialog, details, select), then Turbo/server action, then plain partial, then shared CSS class, then Stimulus, then ViewComponent. A component that only maps props to classes is a CSS class.
- Partials live under the resource they render. `_show` is the canonical per-record partial, reused by show pages, streams and collections; `_row` and `_card` are list variants; `_form` and `_new_dialog` pair with dialogs.
- Set page chrome with `content_for` (`:title`, `:page_title`, `:page_parent`, `:page_header`, `:page_header_actions`, `:body_class`).

Keep Ruby setup short and local; move complex queries to the controller and reusable domain calculations to models.

Every partial that takes arguments gets a strict locals comment (`<%# locals: (x:, y:) -%>`). Do not add mode flags (such as `compact:`) that transform a partial.

## Work with Turbo

- Preserve application morph refresh metadata and stable DOM identifiers.
- Take every Turbo target id from `ApplicationRecord` `turbo_id` / `details_turbo_id`; composite ids append a suffix such as `-details`, `-destroy` or `-editor`. Never hand-write a literal id string or use `dom_id`, in any stream template or partial.
- Subscribe with `turbo_stream_from` only to records that broadcast relevant updates.
- Use Turbo Stream templates for create/edit/update/destroy interactions that replace known fragments; keep ordinary redirects for full navigation.
- Turbo Frames are not used. Partial updates are `turbo_stream.replace` templates named per controller action (`create`, `update`, `destroy`) that render the same `_show`/`_form` partials as the full pages.
- Background-updated records use model-level `broadcasts_refreshes_to`. Do not broadcast interactive cards.
- Mark permanent elements only when their client state must survive morphing.
- Keep nested `form_with` model arrays aligned with the route hierarchy.

## Keep Stimulus narrow and accessible

Stimulus controllers should manipulate their own element through declared targets, values, and actions. Clean up timers, global listeners, and third-party instances in `disconnect`. Dispatch bubbling `change` events when another controller or form owns autosave.

Keep controllers generic and composable (`autosave` + `sortable`). Never branch on a known id or page (`if (id === "...")` means the design is wrong) and never hard-code feature-specific keys.

For menus and custom selects, maintain `aria-expanded`, roles, keyboard navigation, escape behavior, outside click/focus closing, and focus restoration. Prefer native HTML controls when custom behavior adds no product value.

Import browser dependencies through `config/importmap.rb`; there is no `package.json` workflow. The importmap holds only `sortablejs`, `lexxy` and `@rails/activestorage` beyond the framework. Every new pin needs a stated reason, and server rendering is preferred over adding one.

## Style at the correct layer

Keep a single-owner design in Tailwind utilities in its ERB. Promote stable classes to the application's shared component stylesheet only when multiple independent markup owners share the pattern. Add raw palette tokens, named semantic colors/radii/spacing, and base/component rules in their established layers; avoid arbitrary values when a named token or scale utility fits.

Single-use styles stay inline Tailwind in the template. Do not add a `components/*.css` file or `@apply` class for one feature; promote to a shared class only for a real primitive (badge, button, input). Do not invent one-off shadows or colors. Arbitrary values are for structure only (grid templates, anchor positioning), never color.

## Keep frontend code lean

- Use the smallest server-rendered change and extend an existing owner first. Do not add a client framework, generic state layer, wrapper component, or abstraction for a single interaction.
- Keep templates declarative, partial/component inputs explicit, and each Stimulus controller responsible for one behavior. Do not spread the same state across ERB condition trees, data attributes, multiple controllers, and CSS selectors.
- Do not add automated presentation coverage or duplicate non-visual contracts already tested in models, policies, or controllers. Browser-check only the affected interaction and meaningful states.
- Remove `console.log`, temporary instrumentation, and event chatter before finishing. Frontend failures should become purposeful UI state or be reported once by the existing server-side boundary, never by logging DOM content or user data.
- Map state to tone through helpers (`run_status_tone`, `build_status_tone`, ...); `badge_class_for` and `text_class_for` map tone to a class. Extend those helpers rather than branching in templates; unknown values fall back to `:neutral`.

## Verify in the browser

Do not add rendering, selector, CSS-class, ViewComponent, or system tests. Run the asset build, then verify the actual interaction in a browser at the established desktop size and a narrow viewport. Check light/dark themes, keyboard access, focus, loading/error/empty states, Turbo updates, and console errors.
