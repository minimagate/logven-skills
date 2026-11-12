# Proposal

Make a report an explicitly saved configuration over a dataset. Editing and previewing use an assigned, unsaved version of that report; only **Save changes** writes to the original. **Save a copy** creates a new report from the current form values. A dashboard reads the saved report through the same query behavior, with no editor attached.

I would make those changes together. Fixing only the JavaScript copy would leave preview writing to the database, and fixing preview alone would leave column identity fragile.

## What the excerpt shows

- `Report#preview` calls `update!`, so displaying a preview changes the saved report (`app/models/report.rb:7`). The controller invokes it from `show`, under that action's read authorization (`app/controllers/reports_controller.rb:5`).
- The editor copies only the outer configuration object. Its `columns` array and column objects still belong to `report.config`; adding or removing a column changes that shared array (`app/javascript/report_editor.js:3`). Ordinary changes can also save immediately through `options.live`, while column additions/removals bypass that path.
- Columns identify fields by editable names, although fields already have stable IDs and row values use those IDs (`app/models/report.rb:4`, `app/models/dataset.rb:7`). A rename can therefore break the reference.
- `permit!` accepts an unspecified configuration shape. The client copy sends the whole report, including its identity, rather than a bounded set of copyable values (`app/controllers/reports_controller.rb:6`, `app/javascript/report_editor.js:8`).
- Both preview and display currently return every dataset row; the excerpt does not implement filtering or sorting. Their actual semantics, policies, routes, forms and database schema are not supplied.

## The smallest coherent design

**Give columns their own records.** Add `ReportColumn`, owned by a report, with `field_id`, `position` and `width`. The field supplies its current name and kind. Editing a column's width or position preserves its identity; removing a column removes that report's column record, never the dataset field. Validate sensible widths/positions and that each field belongs to the report's dataset. Do not add a redundant workspace or dataset reference to each column.

This is a small relational change for known structure with order, references and editing behavior. Keep arbitrary row values in `Row#data`; those values are genuinely dynamic. Do not invent a new filter system during this fix. Preserve existing filter/sort behavior, validate its actual supported keys, and move any field references to stable IDs too. Inspect the real shape before specifying further schema changes.

Use foreign keys for report and field references. Initially restrict deleting a referenced dataset field, explaining which reports use it; renaming it remains safe. If its kind changes, revalidate any affected filter/sort operation and return a useful error instead of silently changing the meaning or crashing. This avoids implementing snapshots or historical field versions for a requirement that does not ask for them.

**Let Rails forms own edits.** Use the real `Report` and nested column attributes in the existing server-rendered form. Load a fresh report for each request, assign permitted form values in memory, validate it, and render the same form and preview. Do not call `save`, `update!` or autosave children during preview. Preserve nested column IDs and `_destroy` for edits, including repeated add/remove/reorder previews and validation failures.

Remove the shared JavaScript draft and `options.live` persistence path. Keep only small existing-stack JavaScript needed for form interactions. Column additions, removals and reordering participate in the same form/preview flow as other changes. A deep clone would patch one aliasing bug but retain a second, unnecessary source of form state.

**Make each effect explicit.** Keep normal report display read-only. Use an explicit workspace/report URL, resolve the workspace through the current user's accessible workspaces, and load the report through it. Use a separate preview submission, an ordinary report update for saving, and a singular report-copy resource for creating a copy. Preview can use POST for the form payload while still making no persistent writes; GET display never saves.

Use explicit nested parameter allowlists rather than `permit!`. Existing column IDs must belong to the loaded report; submitted field IDs must belong to its authorized dataset. Neither ownership nor source identity comes from submitted attributes. Verify the existing report/dataset workspace invariant rather than assuming workspace membership alone proves every associated record is safe.

**Copy values, not identities.** Save a copy from the current form values, including unsaved edits. Build a new report against the same authorized dataset and explicitly duplicate its effective, non-destroyed column values without IDs or foreign ownership attributes. Copy supported filter/sort values independently. Persist the parent and children atomically. The source and its columns remain unchanged, including when creation fails. Render the form with errors on failure; redirect to the new report on success.

**Share reading, separate interactions.** Put the non-writing row selection on the report (extract a report-owned query object only if the real query warrants it). Both an in-memory preview and a saved dashboard report use this behavior. The dashboard has a read-only rendering entry point and never mounts the editor or receives save/copy callbacks. The server still enforces permissions regardless of the controls shown.

Pundit authorizes report viewing for display, editing for preview/update, and source viewing plus destination creation for copying. A dashboard viewer also needs access to the referenced report and dataset; dashboard access alone does not grant it. Reuse existing policies and keep workspace boundaries intact. A dashboard follows the saved report's current configuration after an explicit save; a separate copy is independent. Historical snapshots are outside this request.

## Implementation order and checks

1. Inspect the complete app's schema, forms, routes, policies and nearest tests. Add column structure and constraints in a structural migration. Separately backfill existing name references using the report's dataset: map only a unique exact match, report missing/ambiguous matches, and never guess or discard an old report. Keep the old configuration available until backfill verification and consumer cutover; remove superseded column JSON/accessors in a later safe step. Do not add permanent dual-write synchronization.
2. Change report assignment, querying and copying, then wire explicit controller operations and Pundit checks. Use nested assignment for edits and explicit identity-free construction for copies. Remove the writing preview and unrestricted parameters. Check that invalid submissions persist nothing and retain the submitted form state.
3. Connect the existing form and separate dashboard reader. Remove the shared editor/autosave path and any superseded client copy serialization. Keep preview errors understandable, action placement stable, and controls labelled and keyboard usable.

The focused regression cases should prove: preview leaves the report and children unchanged after reload; an explicit save persists edits; a copy contains the effective form values with fresh identities and leaves its source unchanged; failure rolls back the whole copy; a field rename preserves references; missing/invalid field references fail clearly; and unauthorized, foreign-workspace or foreign-child submissions cannot read or write protected data. Check read-only dashboard requests for absence of effects. These are model, policy and nonvisual HTTP contracts, with no HTML/DOM assertions.

In the complete app, run those targeted tests, the existing linter, route and Zeitwerk checks, and migrations against a safe local database, inspecting the generated schema. Verify the editor and dashboard manually in a browser, including add/remove/reorder, preview errors, save/copy, keyboard use and a narrow screen. No browser automation or new dependencies are needed.

This was source inspection and planning only. The fixture has no Rails/database runtime, schema, views, policies or test suite, so none of those runtime or browser checks were performed. No application files were changed.
