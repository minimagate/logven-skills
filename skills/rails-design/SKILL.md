---
name: rails-design
description: Design or visually refine any page, component, interaction, or Tailwind styling in a Rails app. Use for all UI appearance work to keep the interface compact, operational, purposeful, consistent, and equally resolved in light and dark mode. Hands UI structure and behavior to rails-frontend.
---

# Rails Design

Design a precise, purposeful interface, not a generic generated dashboard. Every visual choice must improve hierarchy, comprehension, state awareness, or interaction.

Project-specific names, paths and decisions live in the project skill (`project-<name>`); where it differs from this skill, it wins.

If the project has a design reference (`project-<name>/references/design.md`) holding the concrete tokens, classes, geometry and status vocabulary, read it before any visual change; otherwise derive tokens and patterns from the existing styles and keep them consistent.

## Start from the current interface

Inspect the affected view together with neighboring screens, the token definitions, and the relevant component styles before proposing a new treatment. Reuse the established page shells, section headers, data tables, cards, wells, badges, menus, buttons, and view switchers. Promote a new pattern only when the existing system cannot express the product need.

Treat the application as an operational workspace:

- Lead with the objects users act on rather than with chrome or summaries.
- Prefer one continuous work surface with clear regions over a collection of freestanding dashboard cards.
- Keep the current state and next action visible. Put dense detail behind progressive disclosure without hiding the information needed to decide what to do next.
- Do not add summary metrics merely to make a page resemble a dashboard. Retain a page's established table or list focus unless the product requirement genuinely changes.

## Use the surface hierarchy deliberately

The interface is flat, but not divider-free. Use surface color and spacing first, then structural dividers where they clarify a real boundary: the app header, a section header, a table header, rows, cells, or adjacent full-width regions. Do not outline every card, nest bordered boxes, or build decorative divider grids.

Match geometry to the role:

- Full-width panels, lists, tables, and side regions remain square and edge-aligned.
- Standalone cards use the card radius.
- Inset notices and quiet wells use a tighter radius.
- Compact controls (buttons, fields, menus) use the control radius.
- Popovers and toasts use a popover radius plus a raised shadow because they are truly elevated.
- Reserve pill radii for badges and tags. Selects, buttons, tabs, and ordinary containers are not pills.

Preserve accessibility outlines and focus rings; they are interaction signals, not decoration. Ordinary panels and cards remain shadowless. Do not apply the raised shadow to static content.

## Keep scale fine and information-dense

- Use the project's sans font for UI; use monospace only for code, JSON, logs, identifiers, and other technical data.
- Keep page and entity headings at the heading size. Use the body, label, and card sizes for ordinary content, and caption/meta sizes only for genuinely secondary information.
- Prefer medium or semibold weight and good ink contrast over size inflation.
- Keep controls and rows compact: primary actions, icon-only micro actions, table headers, and table rows each have one established height.
- Use small, regular gaps and padding. Avoid large dead zones, oversized section margins, and roomy cards with little content.
- Use `tabular-nums` for numbers that are compared down a column or across rows (amounts, durations, counts).

## Compose pages as operational sections

Prefer full-width sections stacked in task order. A section normally has a compact header bar, an optional count or action, and content immediately below it. Keep primary entity context near the top, then the working collection, then its next action or recent activity.

Prefer inline summaries above the working collection over a persistent summary rail. Present attributes as compact labeled facts; names are usually clearer than decorative logo tiles. Use stacked panels with quiet header surfaces and direct row content for settings. Use segmented controls for a small mutually exclusive view or preference choice.

Navigation is compact, not promotional chrome. Group items into distinct sections with more space between groups than between items, keep navigation icons neutral, and use the established hover/selected surfaces.

## Treat tables as the primary dense-data pattern

- Use the semantic table header, divider, and row-divider roles. Do not improvise nearby neutral shades in markup.
- Keep general data rows on one surface; do not add zebra striping unless a specialized grid already owns that behavior.
- Make the whole row the primary target where it opens the record. Keep per-row secondary actions in a trailing micro menu.
- Align status cells consistently. Put operational numbers in stable columns, and place secondary timestamps at the trailing edge when space allows.
- Before adding a table grid template, reuse an existing class or token; do not add another near-identical arbitrary `grid-cols-[...]` string.
- At narrow widths, preserve the name, current status, and one useful secondary line. Hide lower-priority columns instead of squeezing the desktop table.
- Group rows by meaningful lifecycle state when scanning by state is more useful than a single undifferentiated list. Show a compact group heading, status icon, label, and count.

## Encode status consistently

Status color has a fixed meaning across the app, defined in the project's design reference. Use the existing semantic status, tone, and badge utilities rather than raw palette classes. Pair color with a text label or accessible name. Prefer a purpose-built status icon over a generic dot for lifecycle displays. Do not use a colored dot merely to decorate a label.

Badges must encode a real state, type, format, count, filter, or action-relevant distinction. Use the neutral badge for inactive/default states instead of assigning a color to everything unknown. If removing a badge would not reduce comprehension, remove it.

## Use controls with clear hierarchy

- Reuse the existing button, micro-button, menu, and field classes before composing new controls.
- Use a primary button for the page or section's committed action. Use a micro button for compact icon-only actions, always with an accessible label and title.
- Keep menus dense: compact padding, short icon/text gaps, and the established raised popover surface. Destructive actions belong in the menu's danger treatment.
- Use icon-only segmented switchers for familiar view choices such as table and grid; expose the selected state with `aria-current` and supply labels and titles.
- Keep action placement stable across empty, loading, failed, and completed states.

## Extend color through semantic tokens

Start with the existing palette and reuse the semantic utilities (surface, ink, tone, status, danger, interactive) before adding anything.

- One way to keep themes in step is to define palette values with `light-dark(...)` and have semantic tokens alias palette tokens, so markup never needs `dark:` variants. Follow whatever token architecture the project already uses.
- Raw palette values live only in the token file; add tokens there, not in templates.

When a new distinction genuinely needs color:

1. Add or extend a raw palette token.
2. Add a purpose-named semantic token.
3. Define every theme the app supports together (for example both values in one `light-dark(...)`).
4. Use the semantic utility in markup.

If the app supports dark mode, keep light and dark parity through tokens, never scattered `dark:` overrides when one semantic token can express both themes, and do not assume a light surface maps to the same numeric shade in dark mode. If it does not support dark mode, do not add it unasked.

## Reject UI slop

Do not introduce oversized hero copy, huge empty spacing, gradient blobs, glass effects, gratuitous shadows, fake metrics, ornamental charts, random pills, status dots without meaning, “online” labels without operational value, or invented metadata.

Do not use eyebrow text. A small uppercase label above a heading is not hierarchy; write one clear heading instead. Uppercase remains acceptable only where the content itself is a functional compact label, such as a table column heading.

Do not create a new design system, layout primitive, token family, or component variant for one screen or hypothetical reuse. Remove nested wrappers, competing hierarchies, and class proliferation that make the interface harder to maintain. The minimalism rules behind this are in [principles](../principles/SKILL.md).

## Review before finishing

Inspect the actual affected flow (in light and dark mode if the app supports both) at desktop and narrow widths. Check density, contrast, focus, hover, disabled and selected states, long technical content, empty and error states, table alignment, and whether each divider, badge, icon, and decoration earns its place. Use motion-safe transitions for entry effects and keep ordinary interaction motion restrained.

Verify UI changes in the browser. Do not add visual snapshots, DOM assertions, component tests, or exhaustive viewport/theme combinations to the automated suite. If the result resembles a template before it resembles the product, simplify it.
