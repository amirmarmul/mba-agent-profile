# Business Info Schema Constraints

When modifying Business Info via `mba_business_info.py`, you must use only the official Meta schema fields.

## Supported Fields (all strings)
- `business_description` (Max 2048 chars)
- `payment_method` (Max 1024 chars)
- `return_policy` (Max 1024 chars)
- `purchase_info` (Max 1024 chars)
- `delivery_and_shipping` (Max 1024 chars)
- `contact_email` (Max 1024 chars)
- `hours_of_operation` (Max 1024 chars)
- `address` (Max 1024 chars)

## Rules
- Do not invent fields outside of this list. If a detail does not fit (e.g. "CEO Name" or "Awards"), inject it into the `business_description` or create a dedicated FAQ.
- Null values are not supported. To clear a field, provide an empty string `""` or omit it.
- Keep the `business_description` tightly factual. The agent uses this text as its core identity and fact base.