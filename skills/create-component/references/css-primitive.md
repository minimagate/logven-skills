# CSS-primitive mechanics

This reference should be used once `create-component`'s decision tree has placed a request in
the CSS-primitive category: expressible as one HTML tag, or a base class + modifier class
combined in markup, with no structure or slots. It covers only the `components/*.css` layer of
this app's layered Tailwind architecture. For adding a new color/design token (`@theme`/
`@theme inline`)
or editing bare-element defaults (`base/base.css`), invoke the `style` skill instead — those
layers remain owned by it.

## Reuse threshold

- Keep styling as Tailwind utilities in the component, partial, or view while it has one markup
  owner. Repeated elements inside that same owner do not make the styling shared.
- Promote utilities to this CSS-primitive layer only when the same visual primitive has at least
  two independent markup owners.
- Behavioral selectors and cross-browser rules that utilities cannot express cleanly may remain
  here when their centralized behavior is intentional.

## File location and naming

- One singularly named file per component family under `app/assets/tailwind/components/`
  (`button.css`, `input.css`; add a new file for a new family and import it from
  `application.css`).
- Each file is wrapped in `@layer components`.
- Classes follow a base + modifier pattern: a shared base class (`.btn`, `.card`, `.input`)
  holds structural/layout properties, and modifier classes (`.btn-primary`, `.btn-danger`,
  `.btn-secondary`) hold only the properties that vary. Callers combine them in markup:
  `class="btn btn-primary"`.

## Class-authoring rules

- Reference semantic colors through their generated named utilities (`bg-column`, `bg-well`,
  `text-ink`, `text-ink-body`, `bg-tone-green-surface`) — never through arbitrary
  custom-property syntax, a raw palette utility (`bg-neutral-100`), or a literal color value.
- If the semantic var a class needs doesn't exist yet, that's a gap in `style`'s layers, not
  something to work around here — invoke the `style` skill to add the `@theme`/`@theme inline` entries
  first, then come back and reference the new var from the component class.
- Tailwind v4 only allows `@apply` of real utilities. Never `@apply` one custom `@layer
  components` class from within another custom class (e.g. `@apply btn ...` inside
  `.btn-primary`) — it doesn't work reliably in v4. Combine classes in markup instead.

## Rebuild and verify

- Rebuild with `bin/rails tailwindcss:build` (or rely on `bin/dev`'s watcher) and confirm it
  compiles without "unknown utility class" errors.
- If the change is visible in the browser, verify with the preview tools (start the dev server,
  reload, screenshot/inspect) before reporting done.

## What NOT to do

- Don't `@apply` a custom `@layer components` class from within another custom class.
- Don't use a raw palette utility or a literal color value in a component class — go through a
  named semantic utility instead.
- Don't add a new color or design token here — that belongs in the `style` skill's `@theme`/
  `@theme inline` layers; invoke it first, then reference the result from here.
- Don't build a ViewComponent for something this reference already covers — a single tag/class
  with no structure belongs here, not in `app/components/`.
