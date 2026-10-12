---
name: rails-design
description: Design or visually refine any Logven page, component, interaction, or Tailwind styling. Use for all UI appearance work to keep the technical workspace compact, operational, purposeful, consistent, and equally resolved in light and dark mode. Hands UI structure and behavior to rails-frontend.
---

# Rails Design

Design a precise technical workspace, not a generic generated dashboard. Every visual choice must improve hierarchy, comprehension, state awareness, or interaction.

## Start from the current interface

Inspect the affected view together with neighboring screens, `app/assets/tailwind/base/variables.css`, and the relevant component styles before proposing a new treatment. Reuse the established page shells, section headers, data tables, cards, wells, badges, menus, buttons, and view switchers. Promote a new pattern only when the existing system cannot express the product need.

Treat the application as an operational workspace:

- Lead with the objects users act on, such as runs, workers, steps, sheets, inputs, outputs, errors, and logs.
- Prefer one continuous work surface with clear regions over a collection of freestanding dashboard cards.
- Keep the current state and next action visible. Put dense detail behind progressive disclosure without hiding the information needed to decide what to do next.
- Do not add summary metrics merely to make a page resemble a dashboard. Home is a cross-project runs workspace; retain its table or kanban focus unless the product requirement genuinely changes.

## Use the surface hierarchy deliberately

The interface is flat, but not divider-free. Use surface color and spacing first, then structural dividers where they clarify a real boundary: the app header, a section header, a table header, rows, sheet cells, or adjacent full-width regions. Do not outline every card, nest bordered boxes, or build decorative divider grids.

Match geometry to the role:

- Full-width panels, boards, lists, tables, and inspector regions remain square and edge-aligned.
- Standalone entity cards, including kanban cards, use `rounded-card` or the role-specific card radius.
- Inset notices and quiet wells use the tighter `rounded-well` treatment.
- Buttons, fields, menus, and compact controls use `rounded-ctl`.
- Popovers and toasts use `rounded-popover` plus `shadow-menu` because they are truly elevated.
- Reserve `rounded-badge` pills for badges and tags. Selects, buttons, tabs, and ordinary containers are not pills.

Preserve accessibility outlines and focus rings; they are interaction signals, not decoration. Ordinary panels and cards remain shadowless. Do not apply the popover shadow to static content.

## Keep scale fine and information-dense

- Use Geist through `font-sans`; use monospace only for code, JSON, logs, identifiers, and other technical data.
- Keep page and entity headings at `text-title`. Use `text-body`, `text-label`, and `text-card` for ordinary content, and caption/meta sizes only for genuinely secondary information.
- Prefer medium or semibold weight and good ink contrast over size inflation.
- Keep controls and rows compact: primary actions are generally 2rem high, icon-only micro actions 1.5rem square, table headers 2.25rem, and table rows at least 2.5rem.
- Use small, regular gaps and padding. Avoid large dead zones, oversized section margins, and roomy cards with little content.
- Use `tabular-nums` for duration, cost, token, and comparable operational measurements.

## Compose pages as operational sections

Prefer full-width sections stacked in task order. A section normally has a compact header bar, an optional count or action, and content immediately below it. Keep primary entity context near the top, then the working collection, then its next action or recent activity.

Worker detail pages use an inline profile summary above steps and runs rather than a persistent summary rail. Present category, tools, and build metrics as compact labeled facts; provider names are usually clearer than decorative logo tiles. Settings use stacked panels with quiet header surfaces and direct row content. Use segmented controls for a small mutually exclusive view or preference choice.

The sidebar is compact navigation, not promotional chrome. Group General, Projects, and Quick actions as distinct sections with more space between groups than between items. Keep navigation icons neutral, use the established hover/selected surfaces, and preserve the project hierarchy and shortcut hints.

## Treat tables as the primary dense-data pattern

- Use the semantic `bg-table-header-surface`, `border-divider`, and `border-table-row-divider` roles. Do not improvise nearby neutral shades in markup.
- Keep general data rows on one surface; do not add zebra striping unless the specialized grid already owns that behavior.
- Make the whole row the primary target where it opens the record. Keep per-row secondary actions in a trailing micro menu.
- Align status cells consistently. Put operational numbers in stable columns, and place secondary timestamps at the trailing edge when space allows.
- Before adding a table grid template, reuse an existing class or token; do not add another near-identical arbitrary `grid-cols-[...]` string.
- At narrow widths, preserve the name, current status, and one useful secondary line. Hide lower-priority columns instead of squeezing the desktop table.
- Group runs by meaningful lifecycle state when scanning by state is more useful than a single undifferentiated list. Show a compact group heading, status icon, label, and count.

## Encode status consistently

Status color has fixed operational meaning:

- Neutral: pending, unknown, or not yet active.
- Blue: running or actively building.
- Orange: paused or attention-worthy without failure.
- Red: failed, destructive, or blocking.
- Green: completed, ready, or healthy.

Use the existing semantic status, tone, and badge utilities rather than raw palette classes. Pair color with a text label or accessible name. For run lifecycle displays, reuse the segmented circular `RunStatusIconComponent`; its increasing fill communicates progression more precisely than a generic dot. Do not use a colored dot merely to decorate a label.

Badges must encode a real state, type, format, count, filter, or action-relevant distinction. Use the neutral badge for inactive/default states instead of assigning blue to everything unknown. If removing a badge would not reduce comprehension, remove it.

## Use controls with clear hierarchy

- Reuse `.btn`, `.btn-primary`, `.btn-secondary`, `.micro-button`, `MenuComponent`, and existing field classes before composing new controls.
- Use a primary button for the page or section's committed action. Use a micro button for compact icon-only actions such as starting a run or opening a row menu, always with an accessible label and title.
- Keep menus dense: compact padding, short icon/text gaps, and the established raised popover surface. Destructive actions belong in the menu's danger treatment.
- Use icon-only segmented switchers for familiar views such as table and kanban; expose the selected state with `aria-current` and supply labels and titles.
- Keep action placement stable across empty, loading, paused, failed, and completed states.

## Extend color through semantic tokens

Start with the existing neutral, blue, green, orange, pink, purple, and red palette in `app/assets/tailwind/base/variables.css`. Reuse semantic page, column, well, card, panel, table, ink, tone, status, danger, and interactive utilities before adding anything.

- Raw palette values in `base/variables.css` already use `light-dark(...)`; semantic tokens alias palette tokens and inherit dark mode, so markup never needs `dark:` variants (there are none).
- Palette values, semantic colors, radii, spacing, text sizes and shadows live in the two `@theme` blocks of `app/assets/tailwind/base/variables.css`; component CSS lives in `app/assets/tailwind/components/`. Add tokens there, not in templates.

When a new distinction genuinely needs color:

1. Add or extend a raw palette token.
2. Add a purpose-named semantic token.
3. Define light and dark values together with `light-dark(...)`.
4. Use the semantic utility in markup.

Never solve dark mode by scattering `dark:` overrides when one semantic token can express both themes. Do not assume a light surface maps to the same numeric shade in dark mode.

## Reject UI slop

Do not introduce oversized hero copy, huge empty spacing, gradient blobs, glass effects, gratuitous shadows, fake metrics, ornamental charts, random pills, status dots without meaning, “online” labels without operational value, or invented metadata.

Do not use eyebrow text. A small uppercase label above a heading is not hierarchy; write one clear heading instead. Uppercase remains acceptable only where the content itself is a functional compact label, such as a table column heading.

Do not create a new design system, layout primitive, token family, or component variant for one screen or hypothetical reuse. Remove nested wrappers, competing hierarchies, and class proliferation that make the interface harder to maintain. The minimalism rules behind this are in [principles](../principles/SKILL.md).

## Review before finishing

Inspect the actual affected flow in light and dark mode at desktop and narrow widths. Check density, contrast, focus, hover, disabled and selected states, long technical content, empty and error states, table alignment, and whether each divider, badge, icon, and decoration earns its place. Use motion-safe transitions for entry effects and keep ordinary interaction motion restrained.

Verify UI changes in the browser. Do not add visual snapshots, DOM assertions, component tests, or exhaustive viewport/theme combinations to the automated suite. If the result resembles a template before it resembles Logven, simplify it.
