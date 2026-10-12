---
name: rails-design
description: Design or visually refine any page, component, interaction, or Tailwind styling in a Rails app. Use for all UI appearance work to keep the interface compact, operational, purposeful, consistent, and equally resolved in light and dark mode. Hands UI structure and behavior to rails-frontend.
---

# Rails Design

Design a precise, purposeful interface, not a generic generated dashboard. Every visual choice must improve hierarchy, comprehension, state awareness, or interaction.

Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs, it wins.

If the project has a design reference (`project-<name>/references/design.md`), read it before any visual change for concrete tokens, classes, geometry and status vocabulary. Otherwise derive tokens and patterns from the existing styles.

## Start from the current interface

- Inspect the affected view, neighboring screens, token definitions and component styles before proposing a treatment.
- Reuse the established page shells, section headers, tables, cards, wells, badges, menus, buttons, field classes and view switchers. Promote a new pattern only when the existing system cannot express the need.
- Treat the app as an operational workspace: lead with the objects users act on, not chrome or summaries.
- Prefer one continuous work surface with clear regions over freestanding dashboard cards.
- Keep the current state and next action visible. Put dense detail behind progressive disclosure without hiding what is needed to decide.
- Do not add summary metrics to make a page resemble a dashboard. Keep an established table or list focus unless the requirement genuinely changes.

## Surfaces and geometry

- The interface is flat, not divider-free. Use surface color and spacing first; add dividers only at real boundaries (app header, section header, table header, rows, cells, adjacent full-width regions). No outlined cards, nested bordered boxes or decorative divider grids.
- Geometry follows role:
  - Full-width panels, lists, tables and side regions: square and edge-aligned.
  - Standalone cards: the card radius.
  - Inset notices and quiet wells: a tighter radius.
  - Compact controls (buttons, fields, menus): the control radius.
  - Popovers and toasts: a popover radius plus the raised shadow, since they are truly elevated.
  - Pill radii: badges and tags only.
- Ordinary panels and cards stay shadowless. Never apply the raised shadow to static content.
- Preserve accessibility outlines and focus rings; they are interaction signals, not decoration.

## Scale and density

- Project sans font for UI; monospace only for code, JSON, logs, identifiers and other technical data.
- Page and entity headings at heading size; body, label and card sizes for ordinary content; caption/meta only for genuinely secondary information. Prefer medium or semibold weight and good ink contrast over size inflation.
- Each control and row kind has one established height: primary actions, icon-only micro actions, table headers, table rows.
- Small, regular gaps and padding. No large dead zones, oversized section margins or roomy cards with little content.
- Use `tabular-nums` for numbers compared down a column or across rows (amounts, durations, counts).

## Compose pages as operational sections

- Full-width sections stacked in task order. Each has a compact header bar, an optional count or action, and content directly below.
- Order: primary entity context at the top, then the working collection, then its next action or recent activity.
- Inline summaries above the working collection, not a persistent summary rail. Attributes as compact labeled facts; names over decorative logo tiles.
- Settings use stacked panels with quiet header surfaces and direct row content. Segmented controls only for a small mutually exclusive view or preference choice.
- Navigation is compact, not promotional: more space between groups than between items, neutral icons, established hover and selected surfaces.

## Tables

- Use the semantic table header, divider and row-divider roles. Do not improvise neutral shades in markup.
- General data rows share one surface; no zebra striping unless a specialized grid owns it.
- When a row opens its record, the whole row is the target. Per-row secondary actions go in a trailing micro menu.
- Align status cells consistently. Operational numbers sit in stable columns; secondary timestamps sit at the trailing edge when space allows.
- Before adding a `grid-cols-[...]` template, reuse an existing class or token rather than adding a near-identical string.
- At narrow widths keep the name, current status and one secondary line; hide lower-priority columns instead of squeezing.
- Group rows by lifecycle state when scanning by state helps. A group heading shows a status icon, label and count.

## Status, badges and controls

- Status color has a fixed meaning defined in the project's design reference. Use the semantic status, tone and badge utilities, never raw palette classes.
- Pair color with a text label or accessible name. Prefer a purpose-built status icon over a generic dot for lifecycle states; never add a colored dot just to decorate a label.
- Badges encode a real state, type, format, count, filter or action-relevant distinction. Use the neutral badge for inactive or default states. If removing a badge would not reduce comprehension, remove it.
- Primary button for the page or section's committed action. Micro button for icon-only actions, always with an accessible label and title.
- Menus stay dense on the established raised popover surface. Destructive actions use the menu's danger treatment.
- Icon-only segmented switchers for familiar view choices (table, grid): selected state via `aria-current`, plus labels and titles.
- Keep action placement stable across empty, loading, failed and completed states.

## Color and tokens

- Start from the existing palette and semantic utilities (surface, ink, tone, status, danger, interactive).
- Raw palette values live only in the token file. Do not invent one-off shadows or colors in markup.
- Follow the project's token architecture. If it defines palette values with `light-dark(...)` and aliases semantic tokens to them, markup needs no `dark:` variants.
- When a new distinction genuinely needs color: add or extend a raw palette token, add a purpose-named semantic token, define every supported theme together, then use the semantic utility in markup.
- If the app supports dark mode, keep light and dark parity through tokens, never scattered `dark:` overrides; do not assume a light surface maps to the same shade in dark mode. If the app has no dark mode, do not add one.

## Reject UI slop

- No oversized hero copy, huge empty spacing, gradient blobs, glass effects, gratuitous shadows, fake metrics, ornamental charts, random pills, meaningless status dots, "online" labels without operational value, or invented metadata.
- No eyebrow text. A small uppercase label above a heading is not hierarchy; write one clear heading. Uppercase is acceptable only for functional compact labels such as table column headings.
- Do not create a new design system, layout primitive, token family or component variant for one screen or hypothetical reuse. Remove nested wrappers, competing hierarchies and class proliferation.
- Minimalism rules: see the Principles section of [how-we-work](../how-we-work/SKILL.md).

## Review before finishing

Inspect the actual affected flow, in light and dark mode if the app supports both, at desktop and narrow widths. Check:

- Density, contrast, focus, hover, disabled and selected states.
- Empty, loading, error and failed states; long technical content; table alignment.
- Keyboard access, Turbo updates and browser console errors.
- Whether each divider, badge, icon and decoration earns its place.
- Motion: entry effects use `motion-safe` transitions; ordinary interaction motion stays restrained.
- If the result resembles a template before it resembles the product, simplify it.

Verify UI changes in the browser. Automated presentation tests are out of scope (see `../rails-tests/SKILL.md`).
