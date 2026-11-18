---
name: mba-connectors
description: "Use to manage Meta Business Agent (MBA) Connectors, Connector Tools, and Authentication. Enables the agent to call external third-party APIs."
version: 1.0.0
author: Hermes Agent
license: MIT
prerequisites:
  commands:
    - mba
metadata:
  hermes:
    category: meta
    tags: [meta-business-agent, whatsapp, ai-agent, connectors, api, tools]
---

# MBA Connectors Operator

## Overview
This skill manages Connectors and Connector Tools, which allow a Meta Business Agent to hit external API endpoints (e.g., check order status, fetch live inventory).


Use the `python3 scripts/...` commands listed below for all operations.

## Commands

### 1. Connectors CRUD
Connectors define the base URL, description, and auth type (e.g., NONE, API_KEY).
```bash
python3 scripts/mba_connectors.py list
python3 scripts/mba_connectors.py get <id>
python3 scripts/mba_connectors.py create --body-file /tmp/connector.json
python3 scripts/mba_connectors.py update <id> --body-file /tmp/connector.json
python3 scripts/mba_connectors.py delete <id> --yes
```
*Ref payload: `templates/connector.none.create.example.json`*

### 2. Connector API Key Auth
If `auth_type` is `API_KEY`, you must upload the credentials (headers/params).
```bash
python3 scripts/mba_connectors.py auth <id> --body-file /tmp/auth.json
```
*Ref payload: `templates/connector.auth.example.json`*

### 3. Connector Logs
Check if external API calls failed (only logs failures/errors from the 3rd party API).
```bash
python3 scripts/mba_connectors.py logs <id> --limit 100 --include-stats
```

### 4. Connector Tools CRUD
Tools define the specific endpoints (paths) and payload schemas under a Connector.
```bash
python3 scripts/mba_connector_tools.py list <connector_id>
python3 scripts/mba_connector_tools.py get <connector_id> <tool_id>
python3 scripts/mba_connector_tools.py create <connector_id> --body-file /tmp/tool.json
python3 scripts/mba_connector_tools.py update <connector_id> <tool_id> --body-file /tmp/tool.json
python3 scripts/mba_connector_tools.py delete <connector_id> <tool_id> --yes
```
*Ref payload: `templates/tool.request.example.json`*

### 5. Connector Tool Run (Test)
Dry-run a tool with dummy input to ensure the API mapping works.
```bash
python3 scripts/mba_connector_tools.py run <connector_id> <tool_id> --body-file /tmp/run.json
```
*Ref payload: `templates/tool.run.example.json`*

## Important Rules
- **Trailing slash matters on create endpoints**: Manual testing showed `POST .../agent_connectors/` succeeds while `POST .../agent_connectors` can return HTTP 500. Apply same caution to tool creation under `.../tools/`. When reproducing or patching, preserve the trailing `/` on create endpoints.
- **User-Agent can affect Membrane behaviour**: Sessions found API behaviour could differ between raw `curl` requests and Python urllib defaults. When troubleshooting parity issues, compare `User-Agent` explicitly instead of assuming headers are equivalent.
- **500 Membrane Partial-Success Pattern**: Meta's Membrane API can throw HTTP 500 `Authorization failed` during connector create, tool create, update, or delete/archive even when the config-store mutation partially succeeds. Always verify with `connectors list`, `connectors get <id>`, or `connectors tools list <connector_id>` before concluding the operation fully failed.
- **Provisioning Lag / Pending Action ID**: A tool can appear in `tools list` / `tools get` yet still fail `tools run` with `Tool is not yet provisioned in Membrane (action_id is pending)`. Treat list/get success as metadata-only; tool is not usable until `tools run` succeeds.
- **Delete / Archive Quirk**: Connector or tool deletion can fail from the CLI with an internal Membrane archive/auth error even when the same DELETE works manually. If `python3 scripts/mba_connectors.py delete ... --yes` or `python3 scripts/mba_connector_tools.py delete ... --yes` returns a 500 archive/auth failure, verify with `connectors list` / `tools list` whether the object still exists before retrying. See `references/membrane-lifecycle-quirks.md`.
- **Operator Workflow**: After any create/update/delete, verify the real state in this order: `list/get` for persisted object, `tools list/get` for tool metadata, then `tools run` for runtime readiness. Do not trust one API response in isolation.
- **Destructive Actions**: Always require the `--yes` flag (e.g., `delete`).
- **Payload Generation**: Never invent JSON structures. Use the examples in `templates/` (inside this skill directory) as reference. Copy them to `/tmp`, modify, and supply via `--body-file`.
### References
- `references/connector-schema-rules.md` - Required fields and auth types for Connectors.
- `references/tool-schema-authoring-rules.md` - Required fields and schema constraints for Connector Tools.
- `references/tool-user-auth-patterns.md` - Configuration extraction rules for user authentication in tools.

