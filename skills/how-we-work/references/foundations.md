# Paul's sheets rewrites: representation before machinery

Primary sources: Paul's descriptions of [#347 Sheet sti](https://github.com/logvenhq/logven/pull/347), [#352 Views cleanup](https://github.com/logvenhq/logven/pull/352), [#354 Enum choices](https://github.com/logvenhq/logven/pull/354), and related PRs below; checked against authored diffs reachable from local `main` at `8f8b5593` (11 November 2026). Paul is `psguazz` / Paolo Sguazzabia. GitHub returned no discussion comments for #347 or #352; the explicit explanations are in their descriptions and commit messages. The decision rules below are a synthesis, not a claimed quotation of a manifesto.

## The broader lesson

The original implementation repeatedly needed translation, synchronization and special cases because its representation did not fit the thing being edited. Paul changed the model and ownership, then deleted the supporting machinery. Keeping foundations dumb is one consequence; the broader method is to make the domain explicit, compose a general capability at the appropriate boundary, and let ordinary framework behavior do the work.

### 1. Store the domain facts; derive their technical representation

In #347, `09b6a5d2` changes `app/models/sheets/fields/plain.rb` from storing a generic shape and manipulating it through forms to storing `kind`, enum configuration and choices, then deriving the shape. The commit explicitly explains this reversal of direction.

This does not mean weakening the generic type system: [#118 Enum tweaks](https://github.com/logvenhq/logven/pull/118) allows more general enums in types while table fields expose a narrower supported subset. Infrastructure capability and product configuration need not be identical. Avoid parallel mutable representations and form-to-schema round trips.

### 2. Known structure deserves explicit data and ownership

#347 / `9e217679` replaces display JSON with columns; #352 / `6da7fde5`, `12db7f4c` replaces a JSON layout and `ColumnLayout` wrapper with `ViewColumn` records. #354 / local `31b9bc34`, `91a20184` gives enum choices a `FieldOption` owner for casting, validation and rename propagation.

Use columns for known attributes and child records for entities with identity, order, associations or behavior. JSON remains appropriate for dynamic user record payloads, unknown shapes and deliberately opaque data. The rule is not “never use JSON”. Stable child identity also removes the need to match renamed values by guesswork.

### 3. Distinguish a variant from an independent option

#347 makes plain, reference and attachment fields variants of one field resource (STI), while enum becomes an option on a plain field. `81e9761b` consolidates their shared controller and policy. `e4410119` reduces construction to a bounded class choice plus ordinary `new`, removing custom draft/build/apply machinery.

Choose structure by actual semantics: a new option need not be a new type; genuinely different relationships/behavior may need one. Use a common interface for a real common lifecycle, not a registry or one class per configuration combination. STI is this repository's solution, not a universal prescription.

### 4. Let real models and forms carry edit state

#347 / `ec2d478b`, `e4410119` removes the temporary `NewColumn` layer and custom draft constructors. The real unsaved/assigned model feeds a Turbo form preview; explicit save persists it. #352 / `37ad884b` removes controller-side normalization and manual child reconciliation in favor of model validation and nested attributes. `79b4fe10` consolidates parameter representations, preserving child IDs and destruction markers; copying duplicates records rather than reusing their identities.

Prefer native assignment, validation, nested forms and explicit save over a parallel draft protocol. Preview must not persist. Preserve child identity during edits, authorize nested ownership and distinguish submitted absence from intentional deletion. A copy is an identity-free domain operation, not merely URL serialization replayed as writes. Add custom editing machinery only for a demonstrated contract Rails cannot express.

### 5. Share a contract, not every surface using the data

#352 / `30f1be01` splits editable sheets and read-only board records; both use the view/query model. Common field CRUD is consolidated in #347, but these different interactions separate. The criterion is responsibility, not either “always DRY” or “always split”.

[Charts #317](https://github.com/logvenhq/logven/pull/317) describes the layers explicitly: chart library → generic component/controller → domain query-to-chart adapter → panel. [#364 Organizing suggestions](https://github.com/logvenhq/logven/pull/364) deliberately keeps different actions concrete and accepts one large feature view until repetition justifies more structure. No layer count, file length or caller-count rule should erase these distinctions.

### 6. Remove decisions that do not buy useful control

#347 / `fe1de8d6` removes link/email display settings because rendering already recognizes those values safely. `89ce9557` moves formatting into ordinary helpers and removes the formatter-class-plus-helper chain. Prefer one clear implementation over extra knobs or wrappers. Keep a configuration choice when it expresses a real user need; do not remove validation, safety or user intent in pursuit of fewer options.

Deterministic derivation from explicit data is useful. Guessing which workflow a caller intends is the problem: #352 / `1968bb05` removes automatic view-column initialization and puts default-view construction in `Table#add_default_view`. Model invariants and local integrity callbacks remain legitimate, as #354 demonstrates.

### 7. Match work to the actual interaction

#352 separates the page shell from lazy records/panels/charts (`cea931e9`, `c0c72097`, `d1237a8d`) so initial navigation and form feedback need not wait for every result. Query state travels through URLs. [#366 Aggregations](https://github.com/logvenhq/logven/pull/366) explicitly identifies the next simplification: put controls into the real form to remove URL-reconstruction helpers and reload only what changed. That is a stated direction, not a completed rewrite.

Use ordinary transport/form semantics and one coherent state representation. Keep GET previews read-only; save through authorized writes. Introduce deferred loading when actual cost warrants it, not as mandatory machinery for every page.

## Foundations and limits

Earlier `bed13c00a` isolates generic runtime mechanics from the application's runner; `d181ac52` extracts matching from domain clustering even with one caller. #366 / `af953c9e` gives aggregation one owner (`ViewColumn`), eliminating inconsistent independent references. These support the same question: can better contracts and ownership delete coordination code?

Before adding glue, ask: is the representation wrong, is the owner wrong, is the framework already solving this, or is the requirement actually distinct? Preserve demonstrated behavior and relevant regressions while simplifying. Do not copy incidental historical data-migration or testing choices: this package's schema/data separation and the user's explicit **no UI/DOM tests** policy still govern.
