# Broadcasts and Stimulus

## Broadcast choice

Use broadcasts for record changes that happen outside the initiating request or must update multiple subscribers.

- Subscribe in the page with `turbo_stream_from` using the same streamable used by the model.
- Broadcast only after commit so subscribers never render rolled-back state.
- Use targeted `broadcast_replace_to` when a stable fragment can be rendered independently, as `Step#broadcast_agent_card` does for the step page and parent agent page.
- Use `broadcast_refresh`/`broadcast_refresh_to` with morph and scroll preservation when several areas derive from the same changing aggregate, as agent and run pages do.

Do not create both an explicit stream response and a broadcast for the same synchronous DOM mutation unless two distinct audiences genuinely need them.

Keep rendering details in partials. A model callback may name a partial, target, and locals, but it must not assemble HTML or contain presentation decisions unrelated to target selection.

## Stimulus boundary

Use Stimulus only for browser behavior that HTML and Turbo do not express cleanly. The server remains the source of persisted state.

- Declare targets, values, and actions in the controller and markup; avoid DOM lookup conventions hidden in arbitrary selectors.
- Add global listeners in `connect` and remove the exact bound handlers in `disconnect`.
- Destroy third-party instances such as Sortable in `disconnect`.
- Submit persisted changes through an existing Rails form with `requestSubmit`, including normal CSRF, authorization, and Turbo behavior.
- Preserve keyboard navigation, focus restoration, ARIA state, outside-click behavior, and reduced-motion expectations for interactive controls.
- Coordinate independent instances through a narrowly named custom event only when direct containment is insufficient, as menus use `logven:menu-open`.

Do not fetch JSON or maintain a second client-side model when a form submission and Turbo response already fit. Do not use Stimulus to implement lifecycle or policy decisions owned by Rails.
