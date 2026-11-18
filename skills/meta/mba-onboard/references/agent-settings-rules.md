# Agent Settings Constraints

When modifying the Agent configuration via `mba_settings.py`, observe the following schema constraints dictated by the Meta API.

## 1. Supported Settings Fields

- `ai_audience` (enum: `EVERYONE`, `ALLOWLISTED_ONLY`)
  Determines whether the agent answers anyone who messages or only those on the allowlist.
- `rollout` (object)
  - `enabled` (boolean): Master kill-switch. When `false`, the agent ignores all inbound messages regardless of audience.
- `handoff` (object)
  - `enabled` (boolean): Determines if the agent can offer to pass the thread to a human.
  - `message` (string, max 1024 chars): The exact message the agent sends before initiating the Thread Control pass protocol.
- `followup` (object)
  - `enabled` (boolean): Determines if the agent can send a re-engagement ping if the user stops responding.
  - `followup_interval_in_seconds` (integer, max 86400, min 300): Delay before follow-up.
  - `message` (string, max 1024 chars): The message text.

## 2. Best Practices
- Never set `ai_audience` to `EVERYONE` during initial configuration or if `agent_test` and `agent_eval` are returning bad answers.
- Ensure `handoff.message` is concise and accurately sets expectations for human availability.