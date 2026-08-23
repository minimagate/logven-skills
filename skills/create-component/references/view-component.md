# ViewComponent mechanics

This reference should be used once `create-component`'s decision tree has already placed a
request in the ViewComponent category: the UI needs composed/structured markup (multiple
elements, variants, slots), as opposed to a single tag/class (which belongs to the CSS-primitive
category — follow `references/css-primitive.md` instead).

## The two flavors

Per [ViewComponent's own best-practices guidance](https://viewcomponent.org/best_practices.html),
every ViewComponent in this app is one of two flavors. Decide which one a request needs before
writing it:

- **General-purpose** — implements a reusable UI pattern (a card, a badge, a modal) with zero
  knowledge of this app's domain. `initialize` accepts plain Ruby values only.
- **Application-specific** — owns a stable presentation mapping for a domain object when several
  unrelated callers genuinely need the same mapping. It may render its markup directly or
  compose an existing component or CSS primitive; it does not require a matching general-purpose
  wrapper.

Default to general-purpose. For one caller, extract plain display values in the caller. Reach for
application-specific only after the repeated domain-to-presentation mapping is clear; its job
stops at that mapping and it must still reuse an existing primitive when one already fits.

## File layout

A ViewComponent is a pair of files under `app/components/`:

- `app/components/x_component.rb` — the Ruby class, subclasses `ViewComponent::Base`.
- `app/components/x_component.html.erb` — the sidecar template, same basename as the class file.

Generate both with:

```
bin/rails generate view_component:component ComponentName arg1 arg2
```

The generator may also create `test/components/component_name_component_test.rb`; delete that
generated file because this repository does not keep component or rendered-output tests. The
generator infers accessor methods from positional arguments (`arg1 arg2` above become
`initialize(arg1:, arg2:)` with matching readers) — pass the constructor arguments the component
actually needs; add/edit the generated files afterward for anything the generator can't infer
(slots, conditional classes, etc.).

## Naming

- Component class names end in `-Component` (e.g. `CardComponent`, not `Card`).
- Name a component for **what it renders, not what it accepts** — prefer `AvatarComponent` over
  `UserComponent`, even for an application-specific component whose `initialize` takes a `User`.
- Namespace module names are plural for grouping, e.g. `Users::AvatarComponent`.

## `initialize` and slot rules

- A **general-purpose** component's `initialize` accepts plain Ruby values only — strings,
  symbols, numbers, booleans, arrays of plain values, or an existing small immutable value object
  that makes a repeated input contract clearer. Do not create a value object merely to satisfy a
  component. It never accepts an `ActiveRecord` instance, `Current`, or a Pundit policy object,
  and never calls `ActiveRecord`, `Current`, or Pundit methods internally.
- An **application-specific** component's `initialize` may accept an `ActiveRecord` model,
  but only for a proven repeated presentation mapping. It must not call associations or scopes,
  authorize, or contain business logic that computes or mutates domain state. Pass authorization
  outcomes as plain booleans or values from the caller. The component may own the mapping's markup
  directly or compose an existing primitive; do not create another component solely as a relay.
- Use ViewComponent slots for composable content areas: `renders_one :header`,
  `renders_one :footer`, `renders_many :items`, declared in the component class and consumed in
  the caller as `component.with_header { ... }` / block content.
- Prefer slots over passing raw HTML as a plain string argument — a string argument goes through
  normal auto-escaping (safe but inert), while a slot lets the caller pass real markup/content
  without needing to mark it `html_safe` by hand, which is where sanitization bypasses tend to
  creep in.

## Styling components

A ViewComponent keeps styles it alone owns as Tailwind utility strings in its template or in
literal Ruby class mappings for dynamic variants. Reuse existing primitives from
`app/assets/tailwind/components/*.css` when they already represent a shared pattern. Promote a
component's utilities into that shared layer only after a second independent markup owner needs
the same pattern; do not create a semantic class merely to shorten one component template.

## Other conventions from the official best-practices guide

- **Composition over inheritance** — keep small duplication local until a stable shared behavior
  is demonstrated. Then prefer composing an existing component or a small focused helper over a
  base class or framework.
- **Keep template logic in methods, not inline Ruby** — push anything beyond simple
  interpolation into an instance method (private is fine; it's still template-accessible) rather
  than writing conditionals/loops directly in the `.html.erb` file.
- **Extract general-purpose components once proven, not upfront** — implement a single-use
  version first. Wait for stable repetition, usually across three uses, before generalizing its
  API; two superficially similar call sites may remain local when their responsibilities differ.

## Verification

Verify components in the browser at the relevant application page. Do not create
`ViewComponent::TestCase` files or assert rendered text, selectors, classes, markup, slots, or
variants. If a component exposes important non-presentation business behavior, move that behavior
out of the component when appropriate and cover it through the repository's logic-focused Rails
test workflow.

## What NOT to do

- Don't pass an `ActiveRecord` instance, `Current`, or a policy object into a **general-purpose**
  component's `initialize` — extract plain values in the caller first.
- Don't let an **application-specific** component hold onto a model to traverse further
  associations from the template, authorize, or embed business logic. Do not add a paired
  general-purpose component unless it has its own demonstrated callers.
- Don't promote single-owner Tailwind utilities into a CSS-primitive class before the pattern is
  shared by another independent markup owner.
- Don't build a ViewComponent for something expressible as a single CSS class on a plain HTML
  tag — that belongs to the CSS-primitive category.
- Don't pass raw HTML as a plain string argument when a slot would work instead.
- Don't keep the component test emitted by the generator.
- Don't add rendered-output, selector, DOM, or presentation assertions.
