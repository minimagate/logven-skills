---
name: integrations
description: Add or change Logven external tools, OAuth credentials, provider API adapters, tool registry metadata, or integration tests. Use for Tools, Credentials, Apis, OAuth callbacks, and provider-specific settings UI.
---

# Integrations

Keep provider concerns separated into credential lifecycle, HTTP adapter, callable tool contract, authorization endpoint, and settings UI. Consult the provider's current official API and OAuth documentation before implementation.

## Follow the existing layers

- `Credentials::Base` is STI on `credentials` and owns encrypted access/refresh tokens, expiry, per-user/type/key uniqueness, and revocation contract.
- A provider credential subclass defines supported keys/scopes, authorization URL, code exchange, refresh, and best-effort revocation.
- `Apis::<Provider>` owns authenticated HTTP mechanics, refresh-before-request behavior, response parsing, and provider error translation.
- `Tools::Base` is the runtime registry and metadata contract. Provider tool subclasses declare `tool_name`, display name, brand, description, input shape, output shape, and `run!`.
- Controllers initiate signed OAuth state or disconnect only the current user's credential. The callback verifies state before constantizing the credential class and persists tokens for the user encoded in that state.

Do not collapse these layers into controllers or node runners. `Runner::Tool` should continue to resolve a registered tool and execute it with only the run user and merged input.

## Define tools as strict contracts

- Choose a stable globally unique snake-case `tool_name`; registration rejects collisions.
- Make descriptions specific enough for the graph builder to select the tool correctly.
- Use Logven shapes exactly: string keys, homogeneous arrays, `string`/`number`/`bool`, and trailing `?` for optional inputs.
- Return a hash matching the declared output shape. Normalize missing provider values deliberately rather than leaking arbitrary response bodies.
- Fetch credentials through the executing user. Never use a credential from request parameters or another user's records.
- Validate provider input that enters protocol headers or URLs, including CR/LF injection boundaries.

## Handle tokens and network failures safely

Never log or render access tokens, refresh tokens, OAuth client secrets, authorization headers, or raw credential metadata. Keep secrets in environment configuration and encrypted columns.

Refresh only when expired. Preserve an existing refresh token when a provider omits it during a later exchange. Treat revocation as best effort during destroy so provider downtime does not strand the local record, but log only safe identifiers and error class/message.

Raise a concise error for non-success provider responses. Avoid exposing full response bodies when they may contain sensitive data.

## Verify without live services

Test registry validation, shape contracts, credential selection, query/request construction, token refresh, success parsing, provider errors, callback signature rejection, and per-user isolation using stubbed HTTP. Never call a live provider from the test suite.
