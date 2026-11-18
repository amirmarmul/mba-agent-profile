---
name: mba-onboard
description: "Onboard phones to MBA, check eligibility, manage settings."
version: 1.0.0
author: Amir Marmul (amirmarmul), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [meta-business-agent, whatsapp, ai-agent, onboard, allowlist]
    related_skills: [mba-knowledge, mba-connectors, mba-runtime, mba-setup]
---

# MBA Onboard Operator

## Overview
This skill manages the initial onboarding and environment setup for a Meta Business Agent. It covers entity eligibility checks, agent settings (audience, rollout, handoff, follow-up), and the rollout allowlist for controlled launches.

## When to Use
- First-time MBA setup for a WhatsApp Business Phone Number ID
- Changing agent audience between `ALLOWLISTED_ONLY` and `EVERYONE`
- Enabling/disabling rollout, handoff, or follow-up features
- Adding or removing test numbers from the allowlist during validation
- Verifying eligibility before investing in knowledge/connectors/runtime work

Don't use for:
- Managing FAQs, websites, files, or agent skills → use `mba-knowledge`
- Creating connectors or connector tools → use `mba-connectors`
- Running test messages, evals, handoffs, or events → use `mba-runtime`

## Prerequisites
- Profile workspace config at `workspace/mba/config.json` (created by `mba-setup`)
- If config missing: run `mba-setup` skill to create it
- Token must have:
  - Permission: `whatsapp_business_messaging`
  - Capability: `bizai_wa_enterprise_api_3p_access`
- Python 3.10+ with stdlib only (scripts use `urllib`, `json`, `pathlib`)
- **Config template:** `mba-setup`'s `assets/config.example.json` — reference only; use `mba-setup` to create config

### Missing Configuration
If any script reports "Missing required env" or "ConfigError: Missing required env", **run the `mba-setup` skill immediately**:
```
skill_view(name="mba-setup")
```
Then follow the skill's guided setup to create `workspace/mba/config.json` with your `access_token` and `entity_id`. All MBA scripts auto-detect this config on subsequent runs.

## How to Run
All operations go through the `terminal` tool invoking the skill's Python scripts.

### Example invocations
```
terminal(command="python3 scripts/mba_eligibility.py", timeout=30)
terminal(command="python3 scripts/mba_settings.py get", timeout=30)
terminal(command="python3 scripts/mba_settings.py update --body-file /tmp/settings.json", timeout=30)
terminal(command="python3 scripts/mba_allowlist.py list", timeout=30)
terminal(command="python3 scripts/mba_allowlist.py add --entity +628xxxxxxxxx", timeout=30)
terminal(command="python3 scripts/mba_allowlist.py remove <entry_id> --yes", timeout=30)
```

## Quick Reference
| Operation | Command |
|-----------|---------|
| Check eligibility | `terminal(command="python3 scripts/mba_eligibility.py", timeout=30)` |
| Get settings | `terminal(command="python3 scripts/mba_settings.py get", timeout=30)` |
| Update settings | `terminal(command="python3 scripts/mba_settings.py update --body-file /tmp/settings.json", timeout=30)` |
| List allowlist | `terminal(command="python3 scripts/mba_allowlist.py list", timeout=30)` |
| Add to allowlist | `terminal(command="python3 scripts/mba_allowlist.py add --entity +628xxxxxxxxx", timeout=30)` |
| Remove from allowlist | `terminal(command="python3 scripts/mba_allowlist.py remove <entry_id> --yes", timeout=30)` |

## Procedure
### 1. Check eligibility
- Run: `terminal(command="python3 scripts/mba_eligibility.py", timeout=30)`
- Completion: JSON output contains `"eligible": true` and `"entity_id"` matching your `META_ENTITY_ID`.

### 2. Inspect current settings
- Run: `terminal(command="python3 scripts/mba_settings.py get", timeout=30)`
- Completion: Output shows `rollout.enabled`, `handoff.enabled`, `followup.enabled`, `ai_audience` — record these as baseline.

### 3. Update settings (if needed)
- Copy `assets/settings.response.example.json` → `/tmp/settings.json`
- Modify only the fields you intend to change (e.g., set `rollout.enabled: true`, `ai_audience: "ALLOWLISTED_ONLY"`)
- Run: `terminal(command="python3 scripts/mba_settings.py update --body-file /tmp/settings.json", timeout=30)`
- Completion: Response echoes updated settings; re-run `get` to confirm persistence.

### 4. Configure allowlist for controlled rollout
- Run: `terminal(command="python3 scripts/mba_allowlist.py list", timeout=30)` — note current entries.
- For each test number: `terminal(command="python3 scripts/mba_allowlist.py add --entity +628xxxxxxxxx", timeout=30)`
- Completion: Each add returns an object with `id` and `consumer_phone_number`; verify with `list`.

### 5. Verify end-to-end readiness
- Run eligibility → expect `eligible: true`
- Run settings get → expect `rollout.enabled: true`, `ai_audience: "ALLOWLISTED_ONLY"` (or intended value)
- Run allowlist list → expect your test numbers present
- Completion: All three checks pass; agent is ready for knowledge/connector/runtime work.

## Pitfalls
- **META_ENTITY_ID must be the Phone Number ID** — using the WABA ID returns 404 on all endpoints.
- **500 on settings update can be partial success** — always re-run `get` to verify the write landed.
- **Allowlist changes propagate asynchronously** — a newly added number may not be recognized for ~30 seconds.
- **Missing token capabilities yield 403** — `bizai_wa_enterprise_api_3p_access` is required; `whatsapp_business_messaging` alone is insufficient.
- **Destructive ops require `--yes`** — `allowlist remove` refuses without it; this is intentional.
- **Deprecated `.env`** — if scripts detect `.env` in cwd, they print a warning to migrate to `workspace/mba/config.json` via `mba-setup`.

## Verification
- Eligibility check returns `{"eligible": true, "entity_id": "<META_ENTITY_ID>"}`
- Settings get shows all four top-level keys: `rollout`, `handoff`, `followup`, `ai_audience`
- Allowlist list returns an array containing each test number with a stable `id`
- No 401/403/404 errors on any of the above calls