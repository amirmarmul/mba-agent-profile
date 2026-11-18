# Connector Schema Rules

When registering or updating a Connector via `mba_connectors.py`, you are defining the HTTP bridge between Meta and the external business system.

## 1. Top-Level Schema
- `name` (string, max 64 chars): Human-readable name.
- `description` (string, max 1024 chars): What this connector connects to.
- `base_url` (string, max 2048 chars): The root URL for all tools in this connector.
- `auth_type` (string, enum: `NONE`, `API_KEY`, `BASIC`, `OAUTH2`): The authentication mechanism.

## 2. Auth Mechanisms

### NONE
Requires no `auth_config`.

### API_KEY
Requires `auth_config` to define how the key is passed.
- `api_key_auth`:
  - `inject_into` (enum: `HEADER`, `QUERY`)
  - `key` (string): The header/query parameter name (e.g. `X-Api-Key` or `token`).
  - `value` (string): The actual credential.

### BASIC
Requires `auth_config.basic_auth` containing `username` and `password`.

### OAUTH2
Requires `auth_config.oauth2_auth` with `client_id`, `client_secret`, `token_url`, `scopes` (array), and `auth_method` (e.g., `client_secret_post`).

## 3. Security Warning
Connector setups store credentials in Meta's backend. Do not echo `value`, `password`, or `client_secret` into logs or public chat.