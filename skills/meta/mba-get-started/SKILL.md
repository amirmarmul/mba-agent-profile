---
name: mba-get-started
description: "MBA get started: wizard, config gate, health, token change."
version: 1.0.0
author: Amir Marmul (amirmarmul), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [meta-business-agent, whatsapp, get-started, config, health-check]
    related_skills: [mba-onboard, mba-knowledge, mba-connectors, mba-runtime]
---
# MBA Get Started

Front door for the ops team and the config gate for every mba-* skill. The wizard takes a fresh install from zero to a proven Meta API connection; the health check then keeps recommending the single best next action. One installation serves one tenant (entity).

## When to Use
- First chat on a fresh install (no config) → run the wizard automatically; the user needs no magic phrase
- Any mba-* skill reports missing/invalid config → gate path
- User asks for status or "cek kesehatan agent" → health check
- Token or entity change (rotation, tenant switch) → change path

Don't use for:
- Eligibility/settings/allowlist operations → `mba-onboard`
- FAQs, websites, files, agent/UI skills → `mba-knowledge`
- Connectors and connector tools → `mba-connectors`
- Tests, evals, handoff, events → `mba-runtime`

## Credentials
Exactly two values, supplied by the IT team as one package:
- `META_ACCESS_TOKEN` — System User token with capability `bizai_wa_enterprise_api_3p_access`
- `META_ENTITY_ID` — numeric WhatsApp Business Phone Number ID (a WABA ID returns 404 on every endpoint)

`api_version` / `base_url` default to `2.0.0` / `https://api.facebook.com`; change only on user request.

Config lives at `workspace/mba/config.json` — the only credential source (env vars are never read). Resolution is cwd-independent: `HERMES_PROFILE_DIR` env, else the script's own location under the profile's `skills/meta/`.

## Procedure

### 1. Gate (first step of every run)
- Run: `terminal(command="python3 <skill_dir>/scripts/mba_setup.py --verify", timeout=15)`
- Exit 0 → config ready. Called by another skill: report entity_id and return to the caller. User-facing request: health check (step 4) or change (step 3).
- Exit 1 → wizard (step 2).
- Completion: branch selected by the exit code.

### 2. Wizard (fresh setup)
One question per turn.
1. Orient in 2–3 sentences: what the MBA bot is, and that we will connect credentials, prove the connection, then recommend the next step. Completion: orientation delivered.
2. Ask for the access token from the IT package. Completion: token received from the user — never guessed, fabricated, or reused from another tenant.
3. Ask for the entity ID (Phone Number ID). Completion: numeric ID received.
4. Write: `terminal(command="python3 <skill_dir>/scripts/mba_setup.py --access-token '<TOKEN>' --entity-id <ID>", timeout=30)` — terminal stdin is not a TTY, so pass values explicitly. Completion: `✓ Config written`.
5. Re-run `--verify`. Completion: exit 0.
6. Proof + next action: `terminal(command="python3 <skill_dir>/scripts/mba_status.py", timeout=90)`. Completion: eligibility check returns HTTP 200 → getting started is DONE, regardless of the `eligible` flag. Tell the user the connection result in plain language and present the report's single `next_action`.
   - `eligible: false` → a business condition, not a setup failure; relay the report's recommendation (contact IT/Meta).
   - HTTP 401/403/404 → credentials problem: load `mba-onboard`'s `references/common-api-requirements.md`, identify the cause, collect corrected values from the user/IT, rewrite with `--force` after explicit confirmation, then re-verify and re-prove.

### 3. Change credentials (existing config)
1. Show current state from `--verify` (entity_id, token prefix, api_version, base_url); ask which value to change; wait for the answer and the new value.
2. Entity switch = tenant switch: state explicitly that this installation will manage a different business, and get explicit confirmation before writing.
3. Rewrite with the full credential set (kept + changed values) plus `--force`. Completion: `--verify` exit 0 with the changed field visible.
4. Re-run `mba_status.py` to re-prove the connection. Completion: eligibility HTTP 200.

### 4. Health check (any time, read-only)
- Run: `terminal(command="python3 <skill_dir>/scripts/mba_status.py", timeout=90)`
- The script probes config, eligibility, settings, knowledge counts, allowlist, and saved test/eval history, then computes one `next_action`. The priority ladder lives in the script — present its output; re-deriving the ladder by hand invites drift.
- Present findings in plain language plus exactly one recommended next action.
- Tool-failure symptoms → connector logs on demand via `mba-connectors`.
- Completion: the user has the findings and one next action.

## Token handling
- Confirm with the token prefix only (first 4 characters); the full token stays out of replies.
- Pasted tokens persist in local chat history: tell the user once to keep chat exports private; a leaked token is rotated via step 3.
- `config.json` is gitignored and never enters the distribution payload.

## Quick Reference
| Action | Command |
|--------|---------|
| Gate / verify | `terminal(command="python3 scripts/mba_setup.py --verify", timeout=15)` |
| Write config | `terminal(command="python3 scripts/mba_setup.py --access-token '<TOKEN>' --entity-id <ID>", timeout=30)` |
| Overwrite after confirmation | add `--force` |
| Health + next action | `terminal(command="python3 scripts/mba_status.py", timeout=90)` |
| Config path | `terminal(command="python3 scripts/mba_setup.py --print-config-path", timeout=5)` |

## Pitfalls
- **Quote any frontmatter description containing a colon** — an unquoted colon breaks YAML parsing, the fallback parser mangles `platforms`, and the platform gate rejects the skill as "unsupported".
- **`--verify` checks structure, not validity** — placeholder values pass it. The eligibility proof (`mba_status.py`) is what proves credentials work.
- **Entity ID vs WABA ID** — `META_ENTITY_ID` must be the numeric Phone Number ID.
- **Token capabilities** — missing `bizai_wa_enterprise_api_3p_access` yields 403 even with `whatsapp_business_messaging`.
- **`--force` skips the overwrite guard** — use it only after the user confirmed in step 3.

## Verification
- `--verify` exits 0; `mba_status.py` shows eligibility HTTP 200; the report's `next_action` was presented to the user.
- First-run rehearsal without touching the live tenant: point `HERMES_PROFILE_DIR` at a scratch directory and run the same commands there.
