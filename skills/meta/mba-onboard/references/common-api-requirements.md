# Common API Requirements

When running `mba-*` skills, the following common constraints apply across almost all Meta Business Agent Configuration APIs.

## 1. Environment Requirements
Every Python script expects the `.env` file to provide:
- `META_ACCESS_TOKEN`
- `META_ENTITY_ID`

> Note: The `META_ENTITY_ID` refers strictly to the WhatsApp Business Phone Number ID. Do not use the WABA ID or the App ID for entity configuration endpoints.

## 2. Authorization Requirements
The System User token used must have the following properties granted by the Meta Business Portfolio:
- **Permission**: `whatsapp_business_messaging`
- **Capability**: `bizai_wa_enterprise_api_3p_access`

If these are missing, the Membrane API will return `401 Unauthorized` or `403 Forbidden`.

## 3. Common HTTP Error Codes
All endpoints share this standard error response matrix:
- `400 Bad Request`: Invalid parameters or badly formatted JSON payload. Usually user error.
- `401 Unauthorized`: Missing or invalid `META_ACCESS_TOKEN`.
- `403 Forbidden`: Token is valid, but lacks the necessary capability/permission.
- `404 Not Found`: The resource ID does not exist or the `META_ENTITY_ID` is invalid.
- `429 Too Many Requests`: Rate limit exceeded. Back off and retry.
- `500 Internal Server Error`: Meta Membrane API error. This often happens on Connector creation despite the backend commit succeeding. Verify via `get` before assuming total failure.