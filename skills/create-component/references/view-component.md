# ViewComponent mechanics

This reference should be used once `create-component`'s decision tree has already placed a
request in the ViewComponent category: the UI needs composed/structured markup (multiple
elements, variants, slots), as opposed to a single tag/class (which belongs to the CSS-primitive
category — hand off to the `style` skill instead).

## The two flavors

Per [ViewComponent's own best-practices guidance](https://viewcomponent.org/best_practices.html),
every ViewComponent in this app is one of two flavors. Decide which one a request needs before
writing it:

- **General-purpose** — implements a reusable UI pattern (a card, a badge, a modal) with zero
  knowledge of this app's domain. `initialize` accepts plain Ruby values only.
- **Application-specific** — bridges a domain object to one or more general-purpose components
  or CSS-primitive classes. The canonical example from the official docs: a
  `User::AvatarComponent` accepts a `User` ActiveRecord object and renders a general-purpose
  `Avatar::Component`. In this app that might look like a `WorkflowStatusBadgeComponent` that
  accepts a `Workflow` and renders it via the `.badge`/`.badge-*` CSS-primitive classes.

Default to general-purpose. Reach for application-specific only when the component's whole
purpose is translating a domain object into presentation — and even then, its job stops at that
translation; it must not reimplement markup that a general-purpose component or CSS-primitive
class already provides.

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
  symbols, numbers, booleans, arrays of plain values, or a small value object created
  specifically for this purpose. It never accepts an `ActiveRecord` instance, `Current`, or a
  Pundit policy object, and never calls `ActiveRecord`, `Current`, or Pundit methods internally.
- An **application-specific** component's `initialize` may accept an `ActiveRecord` model,
  `current_user`, or the result of a policy check — but only to immediately extract what it
  needs and delegate rendering to a general-purpose component or CSS-primitive class. It should
  not hold onto the model to call further associations/scopes from inside the template, and it
  must not contain business logic (nothing that computes or mutates domain state) — only the
  presentation-facing mapping (which variant/label/icon to show).
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

- **Composition over inheritance** — if two components need to share behavior, extract a shared
  method/module or compose one component inside another rather than building a base class for
  them to inherit from.
- **Keep template logic in methods, not inline Ruby** — push anything beyond simple
  interpolation into an instance method (private is fine; it's still template-accessible) rather
  than writing conditionals/loops directly in the `.html.erb` file.
- **Extract general-purpose components once proven, not upfront** — implement a single-use
  version first; only pull it into a reusable general-purpose component after it's needed in a
  second place (standard DRY "rule of three" applies before generalizing further).

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
  associations from the template, or embed business logic — it should extract what it needs and
  delegate to a general-purpose component/CSS-primitive class immediately.
- Don't promote single-owner Tailwind utilities into a CSS-primitive class before the pattern is
  shared by another independent markup owner.
- Don't build a ViewComponent for something expressible as a single CSS class on a plain HTML
  tag — that belongs to the CSS-primitive category.
- Don't pass raw HTML as a plain string argument when a slot would work instead.
- Don't keep the component test emitted by the generator.
- Don't add rendered-output, selector, DOM, or presentation assertions.
