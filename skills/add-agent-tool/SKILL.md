---
name: add-agent-tool
description: Add or change a Logven agent tool or external provider integration. Use for `Tools::Base` metadata/registration, tool input/output shapes, tool execution, provider branding, credential STI, OAuth authorization/callbacks, token refresh or revocation, API wrappers, settings connections, and boundary tests.
---

# Add Agent Tool

Treat the tool metadata and shapes as a boot-validated contract, and isolate provider authentication/HTTP behavior behind reusable credential and API objects.

## Workflow

1. Inspect `Tools::Base`, existing tools for the provider, `Nodes::Tool`, `Runner::Tool`, shapes, credentials/API wrappers, settings UI, and tests.
2. Reuse an existing provider credential/API boundary. Add provider infrastructure only when the first tool genuinely requires it.
3. Define metadata and shapes before implementation; keep `run!` returning exactly the output contract.
4. Resolve credentials through the run user and keep tokens out of tool inputs/outputs.
5. Use `add-web-resource` for credential endpoints, `use-turbo` for settings feedback, and `generate-tests` throughout.
6. If seeded showcase agents use the tool, update the idempotent development seed and its contract test.

Read [`references/tool-contract.md`](references/tool-contract.md) for registration, metadata, shapes, and tool tests. Read [`references/provider-integration.md`](references/provider-integration.md) when adding/changing credentials, OAuth, API HTTP behavior, provider assets, or settings connections.

## Core Rules

- Fail fast at boot for invalid named tool metadata or shapes.
- Keep tool names globally unique and stable because node bodies persist them.
- Use string-keyed plain hashes at tool boundaries.
- Share provider credentials and API wrappers across tools.
- Validate ownership at every credential route and callback boundary.

## Do Not

- Do not register anonymous production tools or silently replace a named registration.
- Do not accept LLM-provided Tool node shapes over registry metadata.
- Do not put OAuth tokens into prompts, node bodies, logs, or returned tool data.
- Do not issue live provider requests from tests.
