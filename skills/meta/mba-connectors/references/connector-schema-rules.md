# Connector Schema Rules

Payload shapes for `mba_connectors.py create|update` and `mba_connectors.py auth`. Source: Meta Business Agent Connectors reference (https://developers.facebook.com/documentation/meta-business-agent/reference/configure/connectors/, updated 2026-11-11). When in doubt, re-check that page — this file is a cache, not the source of truth.

## 1. Connector create/update body
- `name`: letters, numbers, underscores only. No leading/trailing underscore, no double underscore. Example: `shopify_orders`.
- `description`: what the external service provides; the agent uses this to decide when to call its tools.
- `base_url`: root URL of the external API.
- `auth_type`: only `NONE`, `API_KEY`, `OAUTH2_CLIENT_CREDENTIALS` are accepted on create/update. `OAUTH2`, `BASIC`, and `CUSTOM` may appear in `get` responses but are rejected as input.

## 2. `auth_config` on create/update
- `NONE`: omit `auth_config`.
- `API_KEY`: `auth_config.api_key` with `headers`, `query_params`, `body_params` arrays. Each param: `field_name` (required), `value` (required), `prefix` (optional, e.g. `Bearer `).
- `OAUTH2_CLIENT_CREDENTIALS`: `auth_config.oauth2_client_credentials` with `token_url`, `scopes_to_request` (array), `token_request_content_type` (`application/x-www-form-urlencoded` or `application/json`), `client_id`, `client_secret`.

## 3. `auth` command uses a different wrapper
`mba_connectors.py auth` calls the `upsertApiKey` endpoint. Its body is `{"api_key_config": {"headers": [...], "query_params": [...], "body_params": [...]}}` — **not** `auth_config`, `api_key_auth`, `api_key_location`, or `api_key_name`. At least one of the three arrays must contain a populated param; an empty or missing `api_key_config` returns HTTP 400. `assets/connector.auth.example.json` is the working shape.

## 4. Security warning
Connector setups store credentials in Meta's backend. Do not echo `value`, `password`, or `client_secret` into logs or public chat.
