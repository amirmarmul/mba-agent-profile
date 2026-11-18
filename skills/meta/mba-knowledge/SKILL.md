---
name: mba-knowledge
description: "Manage MBA Knowledge Base (FAQs, Websites, Files) and Skills."
version: 1.0.0
author: Amir Marmul (amirmarmul), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [meta-business-agent, whatsapp, ai-agent, knowledge, faq, skills]
    related_skills: [mba-onboard, mba-connectors, mba-runtime, mba-setup]
---

# MBA Knowledge & Skills Operator

## Overview
This skill manages what the agent knows (Knowledge: FAQs, Websites, Files) and how it behaves (Agent Skills/Instructions, UI Skills). Knowledge grounds the agent's answers; Skills define tone, behavior constraints, and interactive components.

## When to Use
- Creating, updating, listing, or deleting FAQs, Website sources, or File uploads
- Authoring or mutating Agent Skills (behavior instructions) and UI Skills (interactive components)
- Auditing company information validity across all knowledge sources
- Verifying crawl status of Website knowledge before relying on it

Don't use for:
- Onboarding, eligibility, settings, allowlist → use `mba-onboard`
- Creating connectors or connector tools → use `mba-connectors`
- Running test messages, evals, handoffs, events → use `mba-runtime`

## Prerequisites
- Profile workspace config at `workspace/mba/config.json` (created by `mba-setup`)
- If config missing: run `mba-setup` skill to create it
- Token must have:
  - Permission: `whatsapp_business_messaging`
  - Capability: `bizai_wa_enterprise_api_3p_access`
- Python 3.10+ with stdlib only (scripts use `urllib`, `json`, `pathlib`, `mimetypes`)
- **Config template:** `templates/config.example.json` — reference only; use `mba-setup` to create config
- Payload templates in `templates/` — copy to `/tmp`, modify, pass via `--body-file`

### Missing Configuration
If any script reports "Missing required env" or "ConfigError: Missing required env", **run the `mba-setup` skill immediately**:
```
skill_view(name="mba-setup")
```
Then follow the skill's guided setup to create `workspace/mba/config.json` with your `access_token` and `entity_id`. All MBA scripts auto-detect this config on subsequent runs.
- Payload templates in `templates/` — copy to `/tmp`, modify, pass via `--body-file`

## How to Run
All operations go through the `terminal` tool invoking the skill's Python scripts.

### Example invocations
```
terminal(command="python3 scripts/mba_faq.py list", timeout=30)
terminal(command="python3 scripts/mba_knowledge.py faq create --body-file /tmp/faq.json", timeout=30)
terminal(command="python3 scripts/mba_knowledge.py web list", timeout=30)
terminal(command="python3 scripts/mba_files.py upload /path/to/file.pdf --name \"Policy 2026\"", timeout=60)
terminal(command="python3 scripts/mba_skills.py list", timeout=30)
terminal(command="python3 scripts/mba_ui_skills.py list", timeout=30)
```

## Quick Reference
| Operation | Command |
|-----------|---------|
| FAQ list | `terminal(command="python3 scripts/mba_faq.py list", timeout=30)` |
| FAQ get | `terminal(command="python3 scripts/mba_faq.py get <id>", timeout=30)` |
| FAQ create | `terminal(command="python3 scripts/mba_faq.py create --body-file /tmp/faq.json", timeout=30)` |
| FAQ update | `terminal(command="python3 scripts/mba_faq.py update <id> --body-file /tmp/faq.json", timeout=30)` |
| FAQ delete | `terminal(command="python3 scripts/mba_faq.py delete <id> --yes", timeout=30)` |
| Website list | `terminal(command="python3 scripts/mba_websites.py list", timeout=30)` |
| Website get | `terminal(command="python3 scripts/mba_websites.py get <id>", timeout=30)` |
| Website create | `terminal(command="python3 scripts/mba_websites.py create --body-file /tmp/web.json", timeout=30)` |
| Website update | `terminal(command="python3 scripts/mba_websites.py update <id> --body-file /tmp/web.json", timeout=30)` |
| Website delete | `terminal(command="python3 scripts/mba_websites.py delete <id> --yes", timeout=30)` |
| File list | `terminal(command="python3 scripts/mba_files.py list", timeout=30)` |
| File upload | `terminal(command="python3 scripts/mba_files.py upload /path/to/file.pdf --name "Policy 2026"", timeout=60)` |
| File delete | `terminal(command="python3 scripts/mba_files.py delete <id> --yes", timeout=30)` |
| Agent Skill list | `terminal(command="python3 scripts/mba_skills.py list", timeout=30)` |
| Agent Skill get | `terminal(command="python3 scripts/mba_skills.py get <id>", timeout=30)` |
| Agent Skill create | `terminal(command="python3 scripts/mba_skills.py create --body-file /tmp/skill.json", timeout=30)` |
| Agent Skill update | `terminal(command="python3 scripts/mba_skills.py update <id> --body-file /tmp/skill.json", timeout=30)` |
| Agent Skill delete | `terminal(command="python3 scripts/mba_skills.py delete <id> --yes", timeout=30)` |
| UI Skill list | `terminal(command="python3 scripts/mba_ui_skills.py list", timeout=30)` |
| UI Skill get | `terminal(command="python3 scripts/mba_ui_skills.py get <id>", timeout=30)` |
| UI Skill create | `terminal(command="python3 scripts/mba_ui_skills.py create --body-file /tmp/uiskill.json", timeout=30)` |
| UI Skill update | `terminal(command="python3 scripts/mba_ui_skills.py update <id> --body-file /tmp/uiskill.json", timeout=30)` |
| UI Skill delete | `terminal(command="python3 scripts/mba_ui_skills.py delete <id> --yes", timeout=30)` |

## Procedure
### A. Knowledge: FAQs
1. **List existing FAQs**
   - Run: `terminal(command="python3 scripts/mba_faq.py list", timeout=30)`
   - Completion: Returns array of FAQ objects with `id`, `question`, `answer`, `status`.

2. **Create FAQ**
   - Copy `templates/faq.request.example.json` → `/tmp/faq.json`
   - Modify `question`, `answer` (max 1024 chars each), set `status: "ACTIVE"`
   - Run: `terminal(command="python3 scripts/mba_faq.py create --body-file /tmp/faq.json", timeout=30)`
   - Completion: Response contains new `id`; re-run `list` to confirm.

3. **Update FAQ**
   - Run: `terminal(command="python3 scripts/mba_faq.py get <id>", timeout=30)` → save response → modify `question`/`answer`/`status` → Run: `terminal(command="python3 scripts/mba_faq.py update <id> --body-file /tmp/faq.json", timeout=30)`
   - Completion: Response echoes updated fields; re-run `get` to confirm.

4. **Delete FAQ**
   - Run: `terminal(command="python3 scripts/mba_faq.py delete <id> --yes", timeout=30)`
   - Completion: Returns empty success; re-run `list` to confirm removal.

### B. Knowledge: Websites
1. **List websites**
   - Run: `terminal(command="python3 scripts/mba_websites.py list", timeout=30)`
   - Completion: Returns array with `id`, `url`, `crawl_status`, `pages_crawled`, `last_crawled_at`.

2. **Create website source**
   - Copy `templates/websites.request.example.json` → `/tmp/web.json`
   - Set `url` (public, HTTPS), optional `name`, `crawl_frequency`
   - Run: `terminal(command="python3 scripts/mba_websites.py create --body-file /tmp/web.json", timeout=30)`
   - Completion: Response contains `id` and `crawl_status: "in_progress"`.

3. **Verify crawl readiness**
   - Run: `terminal(command="python3 scripts/mba_websites.py list", timeout=30)` repeatedly until `crawl_status: "completed"` AND `pages_crawled > 0`
   - If stuck at `in_progress` with `pages_crawled: 0` for >10 min: treat as stuck; see Pitfalls.

4. **Delete website**
   - Run: `terminal(command="python3 scripts/mba_websites.py delete <id> --yes", timeout=30)`
   - Completion: Re-run `list` to confirm removal.

### C. Knowledge: Files
1. **Upload file**
   - Run: `terminal(command="python3 scripts/mba_files.py upload /path/to/file.pdf --name \"Policy 2026\"", timeout=60)`
   - Completion: Returns `id`, `name`, `status: "PROCESSED"` (or `PROCESSING` → poll `get`).

2. **List/delete files** — analogous to FAQs.

### D. Agent Skills (Behavior Instructions)
1. **List skills**
   - Run: `terminal(command="python3 scripts/mba_skills.py list", timeout=30)`
   - Completion: Returns array with `id`, `name`, `instruction`, `status`.

2. **Create skill**
   - Copy `templates/skill.request.example.json` → `/tmp/skill.json`
   - Set `name`, `instruction` (max 8192 chars), `status: "ACTIVE"`
   - Run: `terminal(command="python3 scripts/mba_skills.py create --body-file /tmp/skill.json", timeout=30)`
   - Completion: Response contains `id`; re-run `list` to confirm.

3. **Mutate skill (update/delete)**
   - **Always inspect existing skills first** (`terminal(command="python3 scripts/mba_skills.py list", timeout=30)` + `terminal(command="python3 scripts/mba_skills.py get <id>", timeout=30)`)
   - Draft payload locally, ask approval with exact command + impact, then execute
   - See `references/agent-skill-mutation-workflow.md` for full protocol.

### E. UI Skills (Interactive Components)
1. **List UI skills**
   - Run: `terminal(command="python3 scripts/mba_ui_skills.py list", timeout=30)`
   - Completion: Returns array with `id`, `component_type`, `trigger_instruction`, `status`.

2. **Create UI skill**
   - Copy `templates/uiskill.request.example.json` → `/tmp/uiskill.json`
   - Set `component_type` (`button`, `list`, `flow`), `trigger_instruction`, `payload`
   - For `flow` type: verify referenced Flow ID exists and is published before enabling
   - Run: `terminal(command="python3 scripts/mba_ui_skills.py create --body-file /tmp/uiskill.json", timeout=30)`
   - Completion: Response contains `id`; re-run `list` to confirm.

### F. Audit Workflow: Company Information Validity
1. Run: `terminal(command="python3 scripts/mba_knowledge.py faq list", timeout=30)` — inspect for stale dates, unsupported claims, risky superlatives.
2. Run: `terminal(command="python3 scripts/mba_knowledge.py web list", timeout=30)` — verify `pages_crawled > 0` and `crawl_status: "completed"`.
3. Run: `terminal(command="python3 scripts/mba_knowledge.py skills list", timeout=30)` — check for behavior instructions that cause invented facts (e.g., "look up contact info" without fallback).
4. Run: `terminal(command="python3 scripts/mba_ui_skills.py list", timeout=30)` — ensure agent can send correct UI components instead of hallucinating links.
5. If runtime tests fail with `ELIGIBILITY_CHECK_FAILED`, pivot to `mba-onboard` checks first.
6. Categorize findings: stale facts, unsupported claims, missing sources, risky instructions, broken UI, blocked runtime.
7. For dated operational facts (holiday hours, "besok", event dates): recommend delete/replace unless current calendar provided.
8. For credibility claims (client counts, certifications, "only BSP"): require verifiable sources (website, PDF, certificates) before promoting.

## Pitfalls
- **Website crawl stuck at `in_progress` / `pages_crawled: 0`** — public URLs returning 200 can still fail to crawl. Treat FAQ + File Knowledge as primary grounding; delete stuck entries and recreate if user approves.
- **Skill mutations without inspection** — updating/deleting skills blindly can remove critical behavior constraints. Follow `agent-skill-mutation-workflow.md`.
- **Flow-type UI skills referencing unpublished Flow IDs** — agent will fail to render; verify Flow is published in Meta Business Manager first.
- **Connector-backed behavior skills** — must name the connector tool, define deterministic routing, include exception handling, prohibit invented data not from connector response. For promo/voucher flows: explicitly forbid listing promos/vouchers unless returned by connector.
- **Runtime test safety** — when opening `ai_audience` beyond `ALLOWLISTED_ONLY` for validation, save rollback payload first, run tests immediately, restore audience setting.
- **Destructive ops require `--yes`** — all `delete` commands refuse without it.
- **Payload generation** — never invent JSON; always use templates in `templates/`.

## Verification
- FAQ list/get/create/update/delete cycle completes with expected IDs and fields
- Website list shows `crawl_status: "completed"` and `pages_crawled > 0` for active sources
- File upload returns `status: "PROCESSED"` (poll `get` if `PROCESSING`)
- Agent Skill list returns expected instructions; create/update/delete persists
- UI Skill list returns expected components; flow-type references valid published Flow ID
- Audit workflow produces categorized findings with evidence, not assumptions
- No 401/403/404 on any operation