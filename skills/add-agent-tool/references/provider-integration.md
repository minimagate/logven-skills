# Provider integration

## Reuse before adding provider infrastructure

If the provider already exists, add only the new tool and any new credential key/scope or provider asset required. Gmail tools share `Credentials::Google`, `Apis::Google`, and the `gmail` brand; do not create per-tool credential or HTTP wrappers.

For a new provider, keep boundaries parallel to the existing Google integration where applicable:

1. Add a `Credentials::Base` STI subclass with allowed keys/scopes, expiry, refresh, and best-effort revoke behavior.
2. Add a focused `Apis::<Provider>` wrapper for authentication, token refresh, HTTP success checks, and JSON parsing.
3. Add resourceful credential routes/controllers under settings and a Pundit policy/ownership lookup.
4. Use a signed message-verifier state for OAuth callbacks. Include only server-trusted user/type/key context, verify it, then allowlist the credential class before constant use.
5. Persist access token, refresh token, expiry, and token type through the user's credential association.
6. Add provider presentation metadata only when the first branded tool requires it (`ToolsHelper::PROVIDER_ASSETS` plus the image asset).

OAuth authorization redirects deliberately leave the app with `allow_other_host: true`, and their forms disable Turbo. Callback endpoints are unauthenticated but explicitly skip Pundit verification because signed state is their entry contract. Preserve sign-in-independent callback completion without treating query parameters as trusted.

## Credential rules

- Credential STI type/key is unique per user.
- Resolve credentials through `user.credentials.find_by!` or `current_user.credentials.find`; never globally by ID without ownership scope.
- Refresh before an API request when expired.
- Prefer the refresh token for revocation, fall back to access token, and log/recover from revocation network failure so local destruction can complete.
- Keep secrets in environment/credential configuration and filtered parameters; never add tokens to logs, prompts, tool outputs, or fixtures.

## Boundary tests

Stub token exchange/provider HTTP methods and test request method, authentication/refresh, parsed response, non-success errors, signed-state rejection, create/update behavior, ownership isolation, revoke behavior, and Turbo response status. Do not make live provider calls.
