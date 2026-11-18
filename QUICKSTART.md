# First-Use Guide — `mba-setup`

This guide covers **one thing only**: starting a chat with the MBA Copilot profile and using the `mba-setup` skill. Stop there. The other skills are documented in their own `SKILL.md` files.

> Use plain chat throughout. No terminal commands, no extra flags.

## 1. Start the chat

```bash
hermes -p mba-agent chat
```

`-p mba-agent` is required. Without it you get the default Hermes identity instead of the MBA Copilot persona.

## 2. Ask for the skill by name

At the `❯` prompt, say:

> Use the `mba-setup` skill to create the MBA workspace config for me.

Or simply: *"Set up my Meta Business Agent workspace using mba-setup."*

The agent loads the skill and follows its `SKILL.md` — that file is the authoritative procedure. You do not need to dictate the individual steps.

## 3. What to expect

The skill will:

- ask for the Meta token and the numeric Phone Number ID;
- write `<profile>/workspace/mba/config.json` with `access_token`, `entity_id`, `api_version`, `base_url`;
- run its verification and report `✓ Config verification passed`;
- tell you where the config was written.

If it reports `Missing required env` or `ConfigError`, ask it to run `mba-setup` again. That is the supported way to create the config. **`.env` is deprecated for `META_ACCESS_TOKEN` and `META_ENTITY_ID`** — do not use it for these two values.

## 4. Two things to get right

- `META_ENTITY_ID` must be the numeric **Phone Number ID**, not the WABA ID. A WABA ID returns 404 on every endpoint.
- The token needs `whatsapp_business_messaging` **and** the `bizai_wa_enterprise_api_3p_access` capability. Missing the second one returns 403.

