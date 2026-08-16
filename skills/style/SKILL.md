---
name: style
description: Edit Logven's Tailwind design tokens, fonts, semantic colors, sizing scales, base selectors, or shared stylesheet imports. Use for `app/assets/tailwind/base/*`, `@theme`, `@theme inline`, typography/dimension tokens, global focus or disabled states, and deciding whether styling belongs in base CSS or the `create-component` workflow.
---

# Style

Preserve the raw token → semantic utility → base/component chain in the order imported by `application.css`.

## Layers

1. `application.css` imports Tailwind, declares the available `dark` custom variant, then imports variables, base rules, and each component family explicitly.
2. `base/variables.css` defines fonts, the explicit raw color palette, typography/leading/tracking, radii, named spacing/containers, and shadows in `@theme`.
3. The same file maps semantic colors in `@theme inline`, producing utilities such as `bg-page`, `bg-column`, `bg-well`, `text-ink-body`, `bg-tone-orange-surface`, and `text-tone-orange-text`.
4. `base/base.css` owns `@font-face` declarations and global element/pseudo-class/attribute defaults: `html`, `body`, `:focus-visible`, and disabled form controls. It contains no custom component classes.
5. `components/*.css` owns repeated class families or centralized behavioral selectors. Use the `create-component` skill for that layer.

## Workflow

1. Inspect the current token, every usage, and the nearest component family before adding anything.
2. Reuse an existing scale or semantic token when it expresses the same meaning.
3. Add a raw palette value only when the palette lacks the needed value; keep it named by hue/step and represented in hex when possible.
4. Add or change a semantic alias only when the product meaning is repeated independently. Map it to a raw token in `@theme inline`.
5. Add typography, radius, spacing, container, or shadow tokens only for repeated product-specific values. Prefer Tailwind's normal scale for ordinary measurements.
6. Put fonts and truly global selector defaults in `base/base.css`; keep one-owner styling inline in ERB/ViewComponent markup.
7. Run `bin/rails tailwindcss:build` and verify affected pages in the browser.

## Rules

- Declare every raw palette color the app depends on; do not rely implicitly on Tailwind's default palette.
- Use semantic utilities in markup and component classes. Do not spell a semantic color as `bg-(--color-x)` or use a raw `bg-neutral-*` token when a semantic role exists.
- Literal alpha colors are allowed narrowly where hex without alpha cannot express a shadow/mask/gradient need; do not turn incidental values into semantic tokens.
- Keep `@custom-variant dark` available, but do not add `.dark` overrides or toggle behavior unless requested.
- Import every new component-family stylesheet explicitly from `application.css` after base layers.

## Do Not

- Do not add a custom class to `base/base.css`.
- Do not create a theme token merely to shorten one markup owner.
- Do not move shared component mechanics into this skill; invoke `create-component`.
- Do not use arbitrary numeric values when the scale or a meaningful repeated token fits.
- Do not add dark-mode product behavior as a side effect of another style change.
