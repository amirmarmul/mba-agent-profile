# Connector Delete / Archive Workaround

Observed session pattern for Meta Business Agent connector tools:

- `python3 scripts/mba_connector_tools.py delete <connector_id> <tool_id> --yes` returned:
  - HTTP 500
  - `Failed to delete tool`
  - `Membrane API failed to archive action: Authorization failed`
- Immediate verification with `python3 scripts/mba_connector_tools.py list <connector_id>` showed the tool still existed.
- Manual raw DELETE against the same API endpoint succeeded with HTTP 204.

## Practical diagnosis

This points to a request-shape or platform-path quirk rather than a dead resource:

- Connector and tool remained readable via `list` / `get`.
- Third-party connector logs were empty.
- Manual DELETE worked against the same resource.

## Manual fallback pattern

If CLI delete fails with the Membrane archive/auth error, verify existence first:

```bash
python3 scripts/mba_connector_tools.py list <connector_id>
```

If the tool is still present, retry manually with raw DELETE and minimal headers:

```bash
curl --location --request DELETE 'https://api.facebook.com/<ENTITY_ID>/agent_connectors/<CONNECTOR_ID>/tools/<TOOL_ID>' \
  --header 'X-API-Version: 2.0.0' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer <TOKEN>'
```

Then verify again:

```bash
python3 scripts/mba_connector_tools.py list <connector_id>
```

## Working hypothesis

Manual DELETE succeeded without sending `Content-Type: application/json`, while the CLI's generic JSON request path may send that header even with no body. Treat this as a plausible cause when CLI delete fails but manual DELETE succeeds.

## Safe operating rule

Do not assume a 500 archive/auth error means the resource was deleted. Always re-check with `list` or `get` before proceeding to delete the parent connector.
