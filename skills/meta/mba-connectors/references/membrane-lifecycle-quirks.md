# Membrane Lifecycle Quirks for MBA Connectors

Session-derived operator notes from real connector CRUD testing.

## Reproduction Summary
- `POST /<entity_id>/agent_connectors/` succeeded with HTTP 201 when called manually via `curl`.
- `POST /<entity_id>/agent_connectors` (no trailing slash) returned HTTP 500.
- CLI create attempts against connector demo payloads could return HTTP 500 `Membrane API failed to create connector: Authorization failed` while the connector still appeared in `connectors list`.
- Tool create could return HTTP 500 `Membrane API failed to create action: Authorization failed` while the tool still appeared in `connectors tools list`.
- `tools run` could fail with HTTP 400 `Tool is not yet provisioned in Membrane (action_id is pending)` even after list/get succeeded.
- CLI delete for connectors and tools initially returned HTTP 500 archive/auth errors and left objects in place.
- Matching a known-good `curl` request more closely mattered in practice: setting an explicit `User-Agent` restored successful CLI delete behavior for connectors.
- Removing JSON `Content-Type` from body-less DELETE requests also improved parity with known-good curl reproductions.

## Operational Lessons
1. Treat config persistence and Membrane provisioning as separate phases.
2. After any create/update/delete, verify actual state with `list/get` before retrying.
3. For create endpoints, preserve trailing `/` during raw API reproduction.
4. A returned 500 on create does not prove the object is absent.
5. A returned 500 on delete does not prove the object is gone.
6. Tool usability requires `tools run` success, not only metadata presence.

## Suggested Verification Order
1. `connectors list`
2. `connectors get <id>`
3. `connectors tools list <connector_id>`
4. `connectors tools get <connector_id> <tool_id>`
5. `connectors tools run <connector_id> <tool_id> --body-file ...`

## Manual API Clues
- Compare trailing slash vs no trailing slash on create endpoints.
- Compare `User-Agent` between CLI and successful `curl` reproductions.
- For manual delete, record exact status code plus whether object still appears in follow-up list/get.
