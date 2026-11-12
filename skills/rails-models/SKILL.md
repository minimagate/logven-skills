---
name: rails-models
description: Implement Active Record and plain Ruby domain behavior, associations, invariants, state transitions, callbacks and background effects.
---

# Rails Models

Apply the [shared principles](../how-we-work/SKILL.md#principles). Models own intrinsic invariants and domain behavior; explicit callers own composition and product defaults.

## Own facts and invariants

Do not populate optional children or product defaults implicitly. Initialize them, copy configuration and choose presets explicitly at the owning use case; avoid hidden initialization callbacks and caller-specific validation exceptions. Intrinsically required structure still belongs to the primitive contract.

Validate intrinsic configuration once at its owner. Keep required names, valid formats and ownership constraints consistent across callers. Back uniqueness with unique indexes and ownership with foreign keys ([migrations](../rails-migrations/SKILL.md)); permissions belong in [policies](../rails-authorization/SKILL.md).

Store simple domain facts and derive generic shapes/API representations from them, not the reverse. Use columns for known configuration and child records for behavior-rich choices; JSON suits unknown/opaque payloads or dynamic user data. Keep independent options separate from genuinely different types. Let concrete owners declare classifications; allow genuinely unknown/not-applicable states instead of forcing a misleading default. Protocol metadata must be distinguishable from valid ordinary data.

Make invalid combinations unrepresentable through ownership; derive context through one owner instead of storing independent references and policing their agreement. Use one short public operation, not a coordination protocol, when sufficient.

## Query and organize

Put state predicates and derived data on their owner; reuse canonical metrics instead of recomputing them. Query the entities the feature represents, not reference/join rows that multiply them. Use associations and `has_many :through`; count without loading whole collections and preload bounded associations when needed. Avoid parsed markdown and duplicate facts. Choose `dependent:` from actual lifecycle ownership and preserve required history. Soft deletion requires an established convention.

Keep declarations ordered: concerns, constants, associations/scopes, enums, normalization/validation, callbacks, nested attributes/broadcasts, class methods, instance methods, private methods. Use string statuses backed by an owning constant.

## Edit and transition

Prefer real unsaved models and nested attributes for drafts/previews; introduce a separate form contract only for a demonstrated need native assignment cannot express. Preserve nested IDs and destruction markers when editing; copy children explicitly without their identities rather than round-tripping through URL serialization.

Expose explicit transitions and guards. Use the project's `verb_now!`/`verb_later!` convention where applicable; jobs delegate domain behavior, retaining necessary execution concerns. Keep synchronous results synchronous.

## Control effects

Reserve callbacks for unavoidable local invariants. External effects happen after commit; mail uses `deliver_later`. Make enqueue decisions and state changes consistent, and retries idempotent. Attach generated files through Active Storage.

Broadcast background changes through established model mechanisms. Rescue narrowly; preserve failure meaning and avoid failure reporting that can fail validation again.

## Verification

Verify narrow behavior tests per [rails-tests](../rails-tests/SKILL.md), lint and Zeitwerk loading.
