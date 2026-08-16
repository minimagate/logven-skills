---
name: create-component
description: "Choose and create the right Logven UI primitive: Tailwind component class, Rails partial, or ViewComponent."
---

Decide which category a UI request belongs to, then build it there — reusing what already
exists before adding anything new.

## Steps (always in this order)

1. **Check for something to extend before creating anything new**:
   - `app/components/` — is there a ViewComponent close enough to add a new variant/slot to
     instead of a new class?
   - `app/assets/tailwind/components/*.css` — is there a class family (`button.css`,
     `input.css`, ...) close enough to add a new modifier class to?
   - `app/views/**/_*.erb` — is there an existing partial for this exact fragment already
     (e.g. a shared `_form` for `new`/`edit`, a layout-level `_flash`)?
   If yes, extend/reuse it and stop here.

2. **Pick the category**:
   - **Inline utilities**: styling owned by one component, partial, or view stays as Tailwind
     utilities in that markup, including single-tag patterns that are not reused elsewhere.
   - **CSS-primitive**: a class or base + modifier family shared by multiple independent markup
     owners (`class="btn btn-primary"`), with no conditional structure or slots.
   - **Partial**: composed markup scoped to one controller's view family (shared between
     `new`/`edit` for the same resource, split out of one long template for readability, or a
     small fragment rendered from a layout) — it can lean on the current request's context when
     that keeps it truly one-action-local, but prefer explicit inputs once the fragment is shared
     or its dependencies stop being obvious.
   - **ViewComponent**: composed/structured markup that needs to be reusable across unrelated
     view families, have an explicit input contract, or be free of implicit dependence on the current
     controller's instance variables/helpers — whether or not it needs to know about the app.
     This is one category with two flavors (general-purpose vs application-specific); the
     reference file below explains which one a given request needs.

   The partial/ViewComponent fork is really: **implicit vs explicit dependency on the calling
   context.** If the fragment is tightly coupled to one action's context and its inputs are
   obvious there, it's a partial. If it needs a declared contract — because it's reused
   somewhere that doesn't set the same ivars, or needs a test that doesn't require a controller
   — it's a ViewComponent.

3. **CSS-primitive**: see [`references/css-primitive.md`](references/css-primitive.md) for the
   `components/*.css` mechanics (naming, the `@apply`-nesting gotcha, rebuild/verify). If the
   request needs a new color or design token that doesn't exist yet, invoke the `style` skill
   first for the `@theme`/`@theme inline` layers — those remain owned by it — then come back and
   reference the new token from the component class.

4. **Partial**: see [`references/partial.md`](references/partial.md) for file layout/naming,
   implicit-ivar vs explicit-`locals:` data access, collection rendering, and why partials don't
   get a dedicated test file in this repo.

5. **ViewComponent**: see [`references/view-component.md`](references/view-component.md) for
   the generator command, file layout, the general-purpose vs application-specific distinction,
   `initialize`/slot rules, how to compose CSS-primitive classes, and test conventions. Load
   that file before doing any ViewComponent work.

6. **Finish**: run `bin/standardrb` on any new `.rb` files and verify the result in the browser.
   Do not add component, rendering, DOM, or system tests; this repository deliberately keeps UI
   behavior out of its automated test suite.

## Rules

- CSS-primitive mechanics (`components/*.css`) live in `references/css-primitive.md`; token/
  semantic-var/base-element layers (`@theme`, `@theme inline`, `base/base.css`) remain owned by the
  `style` skill — coordinate with it when a new color/token is needed, don't re-derive its rules
  here.
- Every ViewComponent is either general-purpose (plain values only, never touches
  `ActiveRecord`/`Current`/Pundit) or application-specific (may accept a model/`current_user`/a
  policy, but only to translate it into arguments for a general-purpose component or a
  CSS-primitive class — never to reimplement markup or hold business logic). The reference file
  covers the boundary in detail.
- A partial that starts getting reused across unrelated controllers, or accumulates more than a
  couple of explicit `locals:`, has outgrown the category — move it to ViewComponent instead of
  letting it keep growing as a partial.

## What NOT to do

- Don't create a new component, class, or partial without first checking `app/components/`,
  `app/assets/tailwind/components/*.css`, and `app/views/**/_*.erb` for one to extend/reuse.
- Don't build a ViewComponent for styling expressible directly as Tailwind utilities on one
  markup owner.
- Don't reach for a partial when the fragment needs to be reusable outside its view family or
  independently testable — that's what pushes it into ViewComponent territory instead.
- Don't restate the `style` skill's token/base rules, or a reference file's mechanics, inline in
  this file — link to them instead so they only load into context when needed.
- Don't add a new color/design token from within `references/css-primitive.md` — that belongs
  to the `style` skill's `@theme`/`@theme inline` layers.
- Don't skip updating `AGENTS.md` if this skill introduces a new structural convention, top-level
  directory, dependency, or component category; its self-maintenance rules require that update.
