---
name: mba-connectors
description: "Manage MBA Connectors and Tools for external API access."
version: 1.0.0
author: Amir Marmul (amirmarmul), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [meta-business-agent, whatsapp, ai-agent, connectors, api, tools]
    related_skills: [mba-onboard, mba-knowledge, mba-runtime, mba-setup]
---

# MBA Connectors Operator

## Overview
This skill manages Connectors and Connector Tools, which allow a Meta Business Agent to call external API endpoints (e.g., check order status, fetch live inventory, verify vouchers). A Connector defines the base URL, description, and auth type; Tools define specific endpoints, payload schemas, and response mappings under a Connector.

## When to Use
- Creating, updating, listing, or deleting Connectors (base API configuration)
- Managing Connector authentication (API key headers/params)
- Creating, updating, listing, or deleting Connector Tools (endpoint definitions)
- Testing tools with dry-run invocations
- Inspecting connector logs for third-party API failures
- Debugging Membrane API quirks (500 partial success, provisioning lag, delete/archive issues)

Don't use for:
- Onboarding, eligibility, settings, allowlist → use `mba-onboard`
- Knowledge base (FAQs, Websites, Files, Skills) → use `mba-knowledge`
- Test messages, evals, handoffs, events → use `mba-runtime`

## Prerequisites
- Profile workspace config at `workspace/mba/config.json` (created by `mba-setup`)
- If config missing: run `mba-setup` skill to create it
- Token must have:
  - Permission: `whatsapp_business_messaging`
  - Capability: `bizai_wa_enterprise_api_3p_access`
- Python 3.10+ with stdlib only (scripts use `urllib`, `json`, `pathlib`, `uuid`, `mimetypes`)
- **Config template:** `templates/config.example.json` — reference only; use `mba-setup` to create config
- Payload templates in `templates/` — copy to `/tmp`, modify, pass via `--body-file`

### Missing Configuration
If any script reports "Missing required env" or "ConfigError: Missing required env", **run the `mba-setup` skill immediately**:
```
skill_view(name="mba-setup")
```
Then follow the skill's guided setup to create `workspace/mba/config.json` with your `access_token` and `entity_id`. All MBA scripts auto-detect this config on subsequent runs.

## How to Run
All operations go through the `terminal` tool invoking the skill's Python scripts.

### Example invocations
```
terminal(command="python3 scripts/mba_connectors.py list", timeout=30)
terminal(command="python3 scripts/mba_connectors.py create --body-file /tmp/connector.json", timeout=30)
terminal(command="python3 scripts/mba_connectors.py auth <id> --body-file /tmp/auth.json", timeout=30)
terminal(command="python3 scripts/mba_connector_tools.py list <connector_id>", timeout=30)
terminal(command="python3 scripts/mba_connector_tools.py run <connector_id> <tool_id> --body-file /tmp/run.json", timeout=60)
```

## Quick Reference
| Operation | Command |
|-----------|---------|
| Connector list | `terminal(command="python3 scripts/mba_connectors.py list", timeout=30)` |
| Connector get | `terminal(command="python3 scripts/mba_connectors.py get <id>", timeout=30)` |
| Connector create (no auth) | `terminal(command="python3 scripts/mba_connectors.py create --body-file /tmp/connector.json", timeout=30)` |
| Connector update | `terminal(command="python3 scripts/mba_connectors.py update <id> --body-file /tmp/connector.json", timeout=30)` |
| Connector delete | `terminal(command="python3 scripts/mba_connectors.py delete <id> --yes", timeout=30)` |
| Connector auth (API_KEY) | `terminal(command="python3 scripts/mba_connectors.py auth <id> --body-file /tmp/auth.json", timeout=30)` |
| Connector logs | `terminal(command="python3 scripts/mba_connectors.py logs <id> --limit 100 --include-stats", timeout=30)` |
| Tool list | `terminal(command="python3 scripts/mba_connector_tools.py list <connector_id>", timeout=30)` |
| Tool get | `terminal(command="python3 scripts/mba_connector_tools.py get <connector_id> <tool_id>", timeout=30)` |
| Tool create | `terminal(command="python3 scripts/mba_connector_tools.py create <connector_id> --body-file /tmp/tool.json", timeout=30)` |
| Tool update | `terminal(command="python3 scripts/mba_connector_tools.py update <connector_id> <tool_id> --body-file /tmp/tool.json", timeout=30)` |
| Tool delete | `terminal(command="python3 scripts/mba_connector_tools.py delete <connector_id> <tool_id> --yes", timeout=30)` |
| Tool run (test) | `terminal(command="python3 scripts/mba_connector_tools.py run <connector_id> <tool_id> --body-file /tmp/run.json", timeout=60)` |

## Procedure
### A. Connectors CRUD
1. **List connectors**
   - Run: `terminal(command="python3 scripts/mba_connectors.py list", timeout=30)`
   - Completion: Returns array with `id`, `name`, `base_url`, `auth_type`, `description`.

2. **Create connector (auth_type: NONE)**
   - Copy `templates/connector.none.create.example.json` → `/tmp/connector.json`
   - Set `name`, `base_url` (must end with `/`), `description`, `auth_type: "NONE"`
   - Run: `terminal(command="python3 scripts/mba_connectors.py create --body-file /tmp/connector.json", timeout=30)`
   - Completion: Response contains `id`; **trailing slash on base_url is required** — see Pitfalls.

3. **Create connector (auth_type: API_KEY)**
   - Create connector with `auth_type: "API_KEY"` (no auth credentials yet)
   - Then run auth step below.

4. **Update connector**
   - Run `get <id>` → save response → modify fields → `update --body-file`
   - Completion: Response echoes updated fields; re-run `get` to confirm.

5. **Delete connector**
   - Run: `terminal(command="python3 scripts/mba_connectors.py delete <id> --yes", timeout=30)`
   - Completion: Re-run `list` to confirm removal; see Pitfalls for delete/archive quirks.

### B. Connector API Key Auth
1. **Upload API key credentials**
   - Copy `templates/connector.auth.example.json` → `/tmp/auth.json`
   - Set `api_key_location` (`HEADER` or `QUERY_PARAM`), `api_key_name`, `api_key_value`
   - Run: `terminal(command="python3 scripts/mba_connectors.py auth <id> --body-file /tmp/auth.json", timeout=30)`
   - Completion: Response confirms auth config; re-run `get <id>` to verify.

### C. Connector Logs
1. **Inspect third-party API failures**
   - Run: `terminal(command="python3 scripts/mba_connectors.py logs <id> --limit 100 --include-stats", timeout=30)`
   - Completion: Returns failure logs with timestamps, status codes, error bodies; stats summary included.

### D. Connector Tools CRUD
1. **List tools under a connector**
   - Run: `terminal(command="python3 scripts/mba_connector_tools.py list <connector_id>", timeout=30)`
   - Completion: Returns array with `id`, `name`, `description`, `method`, `path`, `status`.

2. **Create tool**
   - Copy `templates/tool.request.example.json` → `/tmp/tool.json`
   - Set `name`, `description`, `method` (`GET`/`POST`), `path` (relative to connector base_url), `input_schema`, `output_schema`
   - **Trailing slash on create endpoint matters** — see Pitfalls.
   - Run: `terminal(command="python3 scripts/mba_connector_tools.py create <connector_id> --body-file /tmp/tool.json", timeout=30)`
   - Completion: Response contains `id` and `status: "PROVISIONING"` (or similar).

3. **Update tool**
   - Run `get <connector_id> <tool_id>` → save → modify → `update --body-file`
   - Completion: Re-run `get` to confirm.

4. **Delete tool**
   - Run: `terminal(command="python3 scripts/mba_connector_tools.py delete <connector_id> <tool_id> --yes", timeout=30)`
   - Completion: Re-run `list` to confirm; see Pitfalls for delete/archive quirks.

### E. Connector Tool Run (Test)
1. **Dry-run a tool**
   - Copy `templates/tool.run.example.json` → `/tmp/run.json`
   - Set `input` matching the tool's `input_schema`
   - Run: `terminal(command="python3 scripts/mba_connector_tools.py run <connector_id> <tool_id> --body-file /tmp/run.json", timeout=60)`
   - Completion: Returns `output` matching `output_schema` or error details; tool is usable only when run succeeds.

### F. Operator Verification Workflow (Required After Every Mutation)
After any create/update/delete, verify real state in this order:
1. `list/get` for persisted object (connector or tool metadata)
2. `tools list/get` for tool metadata (if connector mutation)
3. `tools run` for runtime readiness (if tool mutation)
**Do not trust a single API response in isolation.** See `references/membrane-lifecycle-quirks.md`.

## Pitfalls
- **Trailing slash on create endpoints** — `POST .../agent_connectors/` succeeds; `POST .../agent_connectors` (no slash) can return HTTP 500. Same applies to `.../tools/` create. Preserve trailing `/` on create calls.
- **User-Agent affects Membrane behavior** — Python `urllib` default UA differs from `curl`. When troubleshooting parity issues, compare `User-Agent` explicitly; scripts send `User-Agent: curl/7.68.0` for consistency.
- **500 Membrane partial-success pattern** — HTTP 500 `Authorization failed` during create/update/delete can occur even when config-store mutation partially succeeds. Always verify with `list/get` before concluding total failure.
- **Provisioning lag / pending action_id** — A tool can appear in `list`/`get` yet fail `run` with `Tool is not yet provisioned in Membrane (action_id is pending)`. Treat list/get success as metadata-only; tool is not usable until `run` succeeds.
- **Delete/Archive quirk** — CLI delete can fail with internal Membrane archive/auth error (500) even when the same DELETE works manually. If delete returns 500, verify with `list` whether the object still exists before retrying. See `references/delete-archive-workaround.md`.
- **Destructive ops require `--yes`** — all `delete` commands refuse without it.
- **Payload generation** — never invent JSON; always use templates in `templates/`.

## Verification
- Connector list/get/create/update/delete cycle completes with expected IDs and fields
- Auth upload returns confirmed config; `get` shows `auth_type: "API_KEY"` with credentials masked
- Tool list/get/create/update/delete cycle completes
- Tool run succeeds with valid output matching `output_schema` (provisioning complete)
- Logs command returns failure entries with timestamps and error bodies (or empty if healthy)
- Operator verification workflow (list → get → run) passes after every mutation
- No 401/403/404 on any operation