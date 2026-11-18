# Agent Event Rules

Events allow external business systems to push context updates (side-effects) into the agent's memory.

## Schema
- `to` (string, required): The target customer's phone number in E.164 format.
- `event` (object, required):
  - `type` (string, max 256): The stable event identifier (e.g. `purchase_completed`, `appointment_booked`, `order_shipped`).
  - `description` (string, max 1024): Human-readable event description.
  - `payload` (object, max 10000 chars JSON): The actual event data schema (e.g., order ID, amount, tracking number).

## Operational Rule
Do not use Agent Events as a direct messaging tool. Events are silent memory updates. The agent uses this injected memory to provide contextual answers the next time the user messages, or it may autonomously trigger a follow-up if follow-ups are enabled and the event logic warrants it.