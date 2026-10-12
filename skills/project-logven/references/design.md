# Logven Design System

The concrete Logven visual vocabulary. General design discipline lives in `../../rails-design/SKILL.md`.

## Where things live

- Tokens: the two `@theme` blocks of `app/assets/tailwind/base/variables.css` (palette, semantic colors, radii, spacing, text sizes, shadows).
- Component CSS: `app/assets/tailwind/components/`.
- Palette values use `light-dark(...)`; semantic tokens alias palette tokens. There are no `dark:` variants.
- Font: Geist via `font-sans`. Monospace only for code, JSON, logs, identifiers.

## Palette and semantic tokens

- Palette families: neutral, blue, green, orange, pink, purple, red.
- Semantic families: page, column, well, card, panel, table, ink, tone, status, danger, interactive.
- Table roles: `bg-table-header-surface`, `border-divider`, `border-table-row-divider`.
- Status color meaning: neutral = pending, unknown, not yet active; blue = running or building; orange = paused or attention without failure; red = failed, destructive, blocking; green = completed, ready, healthy.

## Radii

- `rounded-card`: standalone entity cards, including kanban cards (or the role-specific card radius).
- `rounded-well`: inset notices, quiet wells.
- `rounded-ctl`: buttons, fields, menus, compact controls.
- `rounded-popover`: popovers and toasts, with `shadow-menu`.
- `rounded-badge`: badges and tags only.
- Full-width panels, boards, lists, tables, inspector regions: square and edge-aligned. Ordinary panels and cards are shadowless.

## Text sizes

- `text-title`: page and entity headings.
- `text-body`, `text-label`, `text-card`: ordinary content.
- `tabular-nums` for duration, cost, token measurements.

## Sizing

- Primary actions 2rem high. Icon-only micro actions 1.5rem square.
- Table headers 2.25rem. Table rows at least 2.5rem.

## Controls

- `.btn`, `.btn-primary`, `.btn-secondary`, `.micro-button`, `MenuComponent`, existing field classes.
- Micro button for compact icon-only actions (start a run, row menu).
- Icon-only segmented switchers for table and kanban (`aria-current`, labels and titles).
- Destructive menu items use the menu's danger treatment.
- Icons: `svg_tag "icons/..."`. Navigation icons stay neutral.

## Status display

- Run lifecycle: `RunStatusIconComponent` (segmented circular icon; increasing fill shows progression).
- Tone helpers: `run_status_tone`, `build_status_tone`; `badge_class_for`, `text_class_for`; fallback `:neutral`.
- Use the neutral badge for inactive/default states.

## Layout and pages

- Reuse the page shells, section headers, data tables, cards, wells, badges, menus, buttons and view switchers.
- Home is a cross-project runs workspace with a table or kanban focus; no summary metrics.
- Domain objects to lead with: runs, workers, steps, sheets, inputs, outputs, errors, logs.
- Worker detail: inline profile summary above steps and runs (no persistent summary rail). Category, tools and build metrics as compact labeled facts; provider names instead of logo tiles.
- Settings: stacked panels with quiet header surfaces and direct row content.
- Sections: full-width, compact header bar, optional count or action, content immediately below.

## Sidebar

- Compact navigation with three groups: General, Projects, Quick actions. More space between groups than between items.
- Neutral icons; project hierarchy and shortcut hints preserved.

## Tables

- No zebra striping, except the sheet-cell grid.
- Whole row is the primary target; secondary actions in a trailing micro menu.
- Narrow widths keep name, current status and one secondary line; hide lower-priority columns.
- Runs grouped by lifecycle state show a compact group heading with status icon, label and count.

## Rules for this system

- Raw palette values only in `base/variables.css`; add tokens there (palette, semantic, `light-dark(...)`), not in templates.
