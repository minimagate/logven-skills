---
name: rails-design
description: Design and refine interfaces, layouts, spacing, nested surfaces, typography, palettes and interactions in any stack. The main agent designs directly without plan approval.
---

# Design

The main agent designs and edits the interface itself. Start from the request and existing screens, styles, components and project design reference; proceed without asking approval for a plan. Keep technical delegation separate from visual judgment.

- Follow the product's existing design system, palette, typography, spacing, radii and component conventions. Improve consistency; do not import another UI system or invent a competing one.
- Use the fewest visual elements and implementation layers that deliver the intended interaction; preserve accessibility, useful content and the established system.
- Make hierarchy serve the user's task: clear context, working content and next action. Reuse established layouts; omit arbitrary previews, decorative metrics, invented metadata and redundant containers.
- Render user-entered names verbatim. Preserve source units/currency and useful numeric precision; do not humanize names, guess units or round away meaningful differences.
- Keep spacing compact and regular. Avoid oversized padding, empty cards, inflated controls and large dead zones. Preserve readable grouping, touch targets and narrow-screen usability.
- Nest geometry deliberately: an inner card/control radius should fit inside its parent's curve, usually smaller by the inset spacing. Avoid equally large radii at every level, pill-shaped rectangles, doubled borders and box-inside-box clutter. Use spacing or surface contrast when another container adds no meaning.
- Use existing semantic colors and supported themes. Keep status meanings consistent, contrast readable and focus visible. Pair color with labels; restraint applies to borders, shadows, gradients, icons and motion without banning established product treatments.
- Use type weight, alignment and proximity before increasing font size. Align comparable numbers; prioritize useful content at small widths. Keep action placement stable across states.
- Resolve empty, loading, error, disabled, selected and long-content states. Preserve semantic HTML, accessible names, keyboard navigation, escape behavior and focus restoration.

Verify the actual result in a browser at desktop and narrow widths, in supported themes. Check interactions and console errors; run the existing asset build if applicable. Report any unavailable browser verification honestly. **Do not add UI, DOM, snapshot, component or browser tests**; [rails-tests](../rails-tests/SKILL.md) defines the boundary.

For Rails implementation, use [rails-frontend](../rails-frontend/SKILL.md).
