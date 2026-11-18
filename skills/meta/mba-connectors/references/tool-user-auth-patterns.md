# Connector Tool User Auth Patterns

Use this reference when a connector tool needs per-user authentication rather than static connector authentication.

## 1. When `user_auth_required` Should Be `true`
Set `user_auth_required: true` only when the outbound request must use a token or credential belonging to the end-user, not the business system.

Examples:
- customer-specific CRM lookup using the customer's OAuth token
- user-scoped calendar access
- user-scoped commerce account access

Keep it `false` when the tool only needs server-to-server auth already configured at the connector level.

## 2. User Auth Action Types
Meta supports two auth action modes in the extraction config:
- `auth`: initial user authorization/login flow
- `refresh`: refresh an already-issued token

## 3. Required Extraction Paths
For login or refresh tools, define extraction paths carefully:
- `user_auth_token_path`: dot-path to access token in tool response
- `refresh_token_path`: optional dot-path to refresh token
- `expires_at_path`: optional dot-path to token expiry value
- `expires_at_type`: how to interpret expiry

## 4. Expiry Interpretation
Supported `expires_at_type` values:
- `absolute`: response already contains absolute expiry timestamp
- `relative_seconds`: response contains TTL in seconds from now

## 5. Practical Rules
- Always verify the real API response shape before writing these paths.
- Do not guess nested JSON paths.
- If refresh is unsupported by the external API, omit refresh config rather than inventing it.
- Keep auth and business-action tools separate. Do not overload one tool with both login and business behavior.
