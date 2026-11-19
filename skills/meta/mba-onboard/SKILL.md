---
name: mba-onboard
description: "Onboard phones: eligibility, settings, rollout allowlist."
version: 1.0.0
author: Amir Marmul (amirmarmul), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [meta-business-agent, whatsapp, ai-agent, onboard, allowlist]
    related_skills: [mba-knowledge, mba-connectors, mba-runtime, mba-get-started]
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
**Config gate (first step of every run):** check `workspace/mba/config.json` via `mba-get-started`'s verify command:
```
terminal(command="python3 <mba-get-started skill_dir>/scripts/mba_setup.py --verify", timeout=15)
```
- Exit 0 → config ready; proceed with this skill's procedure.
- Exit 1 (missing/invalid config, or any script reports "Missing required env" / ConfigError) → load `skill_view(name="mba-get-started")` and follow it. That is the only next step; mba-get-started collects the two credentials (`META_ACCESS_TOKEN`, `META_ENTITY_ID`) from the user and writes the config. Resume this skill after verify passes.
- **Operating context:** the end users are a non-technical ops team, and both credential values are provisioned to them separately by their IT team. Collect the supplied values; do not walk users through self-service System User token creation in Meta Business Manager unless they explicitly ask.

Scripts resolve config cwd-independently (HERMES_PROFILE_DIR env, else script location); no environment setup needed. Python 3.10+ stdlib only.

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
### 0. Config gate
- Run: `terminal(command="python3 <mba-get-started skill_dir>/scripts/mba_setup.py --verify", timeout=15)`
- Completion: exit 0 (`✓ Config verification passed`). On exit 1, load and follow `mba-get-started` (it asks the user for the two credentials), then re-run verify before continuing.

### 1. Check eligibility
- Run: `terminal(command="python3 scripts/mba_eligibility.py", timeout=30)`
- Completion: JSON shows `is_eligible: true` (live API shape; older docs show `eligible`). An HTTP 200 proves the connection even when the flag is false.

### 2. Inspect current settings
- Run: `terminal(command="python3 scripts/mba_settings.py get", timeout=30)`
- Completion: Output shows `rollout.enabled`, `followup.enabled`, `ai_audience` (plus `handoff.enabled` when present) — record these as baseline. The live response is an array of agent config objects.

### 3. Update settings (if needed)
- **Settings schema:** load `references/agent-settings-rules.md` before drafting `/tmp/settings.json`.
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
- **Placeholder config passes verify** — config.json is the only credential source (env vars are never read); dummy values pass `--verify` but fail API calls. Prove credentials with mba-get-started's `mba_status.py` (eligibility HTTP 200).
- **api_version must exist on Meta** — "2.1.0" returns 404 "API version not found"; use the skill default "2.0.0" unless Meta documents otherwise.
- **META_ENTITY_ID must be the Phone Number ID** — using the WABA ID returns 404 on all endpoints.
- **500 on settings update can be partial success** — always re-run `get` to verify the write landed.
- **Allowlist changes propagate asynchronously** — a newly added number may not be recognized for ~30 seconds.
- **Missing token capabilities yield 403** — `bizai_wa_enterprise_api_3p_access` is required; `whatsapp_business_messaging` alone is insufficient.
- **Destructive ops require `--yes`** — `allowlist remove` refuses without it; this is intentional.
- **Unexpected 401/403/404:** load `references/common-api-requirements.md` for the shared error matrix and required token capability.

## Verification
- Eligibility check returns HTTP 200 with `is_eligible: true` (or `eligible: true` on older payloads)
- Settings get shows `rollout`, `followup`, `ai_audience` (and `handoff` when configured)
- Allowlist list returns an array containing each test number with a stable `id`
- No 401/403/404 errors on any of the above calls