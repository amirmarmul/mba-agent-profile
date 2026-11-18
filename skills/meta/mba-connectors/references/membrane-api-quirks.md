# Membrane API quirks — Aptana/MBA session notes

## Confirmed behavior

### 1. Create connector is sensitive to trailing slash
- `POST /<entity_id>/agent_connectors/` succeeded with `201`.
- `POST /<entity_id>/agent_connectors` could return `500` even when the object was created.

### 2. Create tool is sensitive to trailing slash
- Use `POST /<entity_id>/agent_connectors/<connector_id>/tools/`
- Avoid `.../tools` without trailing slash for create.

### 3. CLI requests worked after setting a curl-like User-Agent
A curl-like user agent was needed for reliable connector deletion from CLI in this environment.
Recommended request header:
- `User-Agent: curl/7.68.0`

### 4. Body-less requests should avoid forcing JSON Content-Type
For `GET`/`DELETE` without a body, avoid sending `Content-Type: application/json` unless required.

## Proven debugging sequence
1. If create returns `500`, immediately verify with:
   - `python3 scripts/mba_connectors.py list`
   - `python3 scripts/mba_connectors.py get <id>` if id is known
2. If tool create returns `500`, verify with:
   - `python3 scripts/mba_connector_tools.py list <connector_id>`
3. If tool run fails, inspect whether the tool was provisioned or whether the external service itself returned an error.
4. If delete fails in CLI but works in curl, compare:
   - trailing slash usage
   - `User-Agent`
   - `Content-Type` on body-less requests

## Proven lifecycle after fixes
After patching the CLI to:
- send curl-like `User-Agent`
- omit `Content-Type` on body-less requests
- use trailing slash for connector/tool create

This lifecycle succeeded:
1. create connector
2. create tool
3. run tool
4. delete tool
5. delete connector

## Notes
- A tool run can still fail because the external upstream service returns an HTTP error. That is different from connector provisioning failure.
- Keep this reference as implementation guidance for MBA connector tooling, not as a permanent claim about Meta APIs in all environments.
