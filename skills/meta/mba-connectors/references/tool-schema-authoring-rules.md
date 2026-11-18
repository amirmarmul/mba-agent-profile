# Connector Tool Schema Authoring Rules

When creating or updating API Connector Tools via `python3 scripts/mba_connector_tools.py`, you must provide a highly rigid and descriptive JSON schema. The Meta Business Agent relies entirely on your schema descriptions to know *when* to invoke the tool and *how* to extract parameters from the human conversation.

## 1. Required Top-Level Fields
Every tool payload MUST include:
- `name`: Stable tool key (e.g., `check_order_status`). Avoid generic names.
- `description`: Detailed explanation of what the tool does and what it returns. **Vague descriptions cause the agent to never invoke the tool.**
- `user_auth_required`: Boolean.
- `request_definition`: The HTTP routing and schema body.

## 2. Request Definition Anatomy
Inside `request_definition`, you define:
- `path`: The relative endpoint (e.g., `/items`).
- `path_parameters`, `query_parameters`, `headers`: Objects defining the expected variables.
- `body`: Must include `content_type: "application/json"` and `params` (the schema of the JSON body).

## 3. Schema Node Constraints (`BizAIOmniChannelConnectorToolParameterNode`)
Every parameter or body field you define must include:
- `type`: Must be one of `string`, `integer`, `number`, `boolean`, `object`, or `array`.
- `description`: **Mandatory.** The agent uses this description to understand what data to extract from the user's message.
- `required`: Boolean for query/headers; array of keys for object bodies.

### The "No Vague Object" Rule
Never define a body node as type `object` without explicitly listing its `properties`.
- **Bad**: `{"type": "object", "description": "Customer data"}`
- **Good**: `{"type": "object", "properties": {"name": {"type": "string", "description": "Customer full name"}, "age": {"type": "integer", "description": "Customer age"}}}`
If you leave an object undefined, the agent will hallucinate the JSON structure and the API request will fail.

## 4. Supported Macros
You can instruct Meta's Membrane to inject system variables at runtime by setting a parameter's `kind` to `macro` and providing the `macro` ID:
- `WHATSAPP_PHONE_NUMBER`
- `WHATSAPP_IDENTITY_HASH`
- `WHATSAPP_CURRENT_STATUS_ID`