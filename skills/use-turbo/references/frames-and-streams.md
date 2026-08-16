# Frames and stream responses

## Stable targets

Persisted records use `ApplicationRecord#turbo_id`, which yields a dasherized model prefix plus ID. The class method provides collection targets, and new records use the `-new` suffix. Reuse this contract for record frames and stream targets. Use Rails `dom_id` for unrelated local IDs such as a hidden reorder form.

## Frame editing

The step editor is the canonical pattern:

- The display and edit partials both wrap content in `turbo_frame_tag step.turbo_id`.
- `StepsController#show` and `#edit` render the matching card partial only for a frame request.
- `#update` returns the display card on frame success and the form card with an unprocessable status on frame validation failure.
- Full-page requests retain normal redirects and templates.

Keep frame identity identical across states. Render a controller-local partial with explicit locals rather than returning a second page shell into the frame.

## Stream templates

Use `.turbo_stream.erb` when one successful request performs a small set of explicit collection mutations. `steps/create` removes the empty state and appends a card; `steps/destroy` replaces the collection so positions and the empty state stay coherent.

Let Rails render the stream template implicitly when there is no useful HTML branch. Use explicit `respond_to` only where clients need intentionally different results. A reorder submission returns `head :no_content` to preserve the already-reordered client list rather than replacing it.

Forms that must request streams explicitly may set `data-turbo-stream`; forms leaving the app for OAuth set `data-turbo="false"`. Use `data-turbo-confirm` on destructive forms.

## Verification

Use `generate-tests` only for response status/format, persistence, enqueueing, and authorization when those are contracts. Never assert stream tags or rendered markup. Verify frame replacement, collection mutations, focus, and browser history interactively.
