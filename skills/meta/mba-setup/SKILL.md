---
name: mba-setup
description: Initialize Meta Business Agent workspace configuration.
version: 0.1.0
author: Amir Marmul (amirmarmul), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [meta-business-agent, setup, config, onboarding]
    related_skills: [mba-onboard, mba-knowledge, mba-connectors, mba-runtime]
---
# MBA Setup Skill

This skill guides you through initializing the Meta Business Agent workspace configuration. It creates `workspace/mba/config.json` with your `META_ACCESS_TOKEN` and `META_ENTITY_ID`, enabling all other MBA skills to auto-detect your environment.

## When to Use
- First-time setup for a Meta Business Agent
- Migrating from deprecated `.env` to workspace config
- Refreshing or rotating your META_ACCESS_TOKEN
- Any MBA skill reports missing or invalid configuration

Don't use for:
- Daily agent operations (use onboard/knowledge/connectors/runtime instead)
- Managing FAQs, websites, or files (use `mba-knowledge` instead)
- Creating connectors or tools (use `mba-connectors` instead)
- Running test messages or evals (use `mba-runtime` instead)

## Prerequisites
- Hermes profile active (or run from any directory with internet access)
- `HERMES_PROFILE_DIR` environment variable set, or cwd contains profile workspace
- Internet access to Meta Business API
- Your `META_ACCESS_TOKEN` and `META_ENTITY_ID` from Meta Business Portfolio System User

**Config template:** `assets/config.example.json` — this skill writes the final `workspace/mba/config.json`; copy the template first if you want a reference.

## How to Run
All operations go through the `terminal` tool invoking this skill's Python script.

### Setup (one-time)
```
terminal(command="python3 scripts/mba_setup.py", timeout=30)
```
This creates `workspace/mba/config.json` with your `access_token` and `entity_id`. Scripts will auto-detect this config on subsequent runs.

### If config already exists
Re-run this skill and choose `y` to overwrite, or update individual values via the workspace config file.

### Verify existing config
```
terminal(command="python3 scripts/mba_setup.py --verify", timeout=15)
```
Validates JSON structure, required fields, entity_id format, and MetaConfig.load().

## Quick Reference
| Action | Command |
|--------|---------|
| Run setup | `terminal(command="python3 scripts/mba_setup.py", timeout=30)` |
| Verify config | `terminal(command="python3 scripts/mba_setup.py --verify", timeout=15)` |
| Non-interactive setup | `terminal(command="python3 scripts/mba_setup.py --force --access-token TOKEN --entity-id 123456789", timeout=30)` |
| Print config path | `terminal(command="python3 scripts/mba_setup.py --print-config-path", timeout=5)` |

## Procedure
### 1. Run setup
- Run: `terminal(command="python3 scripts/mba_setup.py", timeout=30)`
- Completion: Config written to `workspace/mba/config.json`; scripts confirm auto-detection
- Verify: Config file exists at `workspace/mba/config.json` with required keys

### 2. Verify config
- Run: `terminal(command="python3 scripts/mba_setup.py --verify", timeout=15)`
- Completion: Exit code 0; output shows `✓ Config verification passed` with entity_id, api_version, base_url, token prefix
- Verify: All MBA scripts now read from workspace config (MetaConfig.from_env() succeeds)

## Pitfalls
- **Entity ID vs WABA ID:** `META_ENTITY_ID` must be the numeric Phone Number ID, not the WABA ID. Using WABA ID returns 404 on all endpoints.
- **Token capabilities:** Token must have `whatsapp_business_messaging` permission and `bizai_wa_enterprise_api_3p_access` capability. Insufficient tokens yield 403 errors.
- **Deprecated `.env`:** If `.env` exists in cwd, scripts print a warning to migrate to `workspace/mba/config.json` via this skill.
- **Overwrite prompt:** Config already existing prompts before overwriting — respond `y` carefully.
- **Keyboard interrupt:** Ctrl+C aborts; config is not written if interrupted mid-prompt.

## Verification
- `workspace/mba/config.json` exists with `access_token`, `entity_id`, `api_version`, `base_url` keys
- `python3 scripts/mba_setup.py --verify` exits 0 and shows `✓ Config verification passed`
- All other MBA skills (`mba-onboard`, `mba-knowledge`, `mba-connectors`, `mba-runtime`) auto-detect config and no longer show deprecation warnings
- No 401/403/404 on config-requiring API calls after setup