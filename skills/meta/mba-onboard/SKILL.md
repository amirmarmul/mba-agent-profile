---
name: mba-onboard
description: "Use to onboard a phone number to Meta Business Agent (MBA), check eligibility, manage high-level agent settings, and configure the allowlist for testing."
version: 1.0.0
author: Hermes Agent
license: MIT
prerequisites:
  commands:
    - mba
metadata:
  hermes:
    category: meta
    tags: [meta-business-agent, whatsapp, ai-agent, onboard, allowlist]
---

# MBA Onboard Operator

## Overview
This skill guides the agent to perform onboarding and environment setup for a Meta Business Agent. You manage entity eligibility, generic settings, and the rollout allowlist.


Use the `python3 scripts/...` commands listed below for all operations.

## Commands

### 1. Check Eligibility
Check if the current entity ID is eligible to operate an MBA.
```bash
python3 scripts/mba_eligibility.py
```

### 2. Manage Settings
Manage high-level agent settings (like AI Audience, Handoff availability).
```bash
python3 scripts/mba_settings.py get
```
*To update settings, read `templates/settings.response.example.json` (inside this skill directory), modify values, save to a temp file (e.g. `/tmp/settings.json`), and run:*
```bash
python3 scripts/mba_settings.py update --body-file /tmp/settings.json
```

### 3. Allowlist Management
For safety, MBA rollouts often start in `ALLOWLISTED_ONLY` mode.
```bash
python3 scripts/mba_allowlist.py list
python3 scripts/mba_allowlist.py add --entity +628****7890
python3 scripts/mba_allowlist.py remove <entry_id> --yes
```

## Important Rules
- **Destructive Actions**: Always require the `--yes` flag (e.g., `remove`).
- **No Direct API**: Never use `curl` or manual python requests. Always use `python3 scripts/mba_onboard.py`.
- **Payload Generation**: Never invent JSON structures. Use the examples in `templates/` (inside this skill directory) as your reference.
### References
- `references/agent-settings-rules.md` - Schema for AI audience, handoff, and rollout settings.
- `references/common-api-requirements.md` - Required tokens, capabilities, and shared error codes.

