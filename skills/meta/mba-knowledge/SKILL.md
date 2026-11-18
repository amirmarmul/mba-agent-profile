---
name: mba-knowledge
description: "Use to manage Meta Business Agent (MBA) Knowledge Base (FAQs, Websites, Files) and Agent Skills (Instructions/Behavior)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    category: meta
    tags: [meta-business-agent, whatsapp, ai-agent, knowledge, faq, skills]
---

# MBA Knowledge & Skills Operator

## Overview
This skill manages what the agent knows (Knowledge) and how it behaves (Skills/Instructions). 
Knowledge facts (FAQs, PDFs, Websites) ground the agent's answers. Skills define its tone and behavior constraints.

## Environment & Tooling
Before executing operations, ensure the `.env` file containing `META_ACCESS_TOKEN` and `META_ENTITY_ID` exists in the user's current working directory.

Use the `python3 scripts/...` commands listed below for all operations.

## Commands

### 1. Knowledge: FAQs
```bash
python3 scripts/mba_faq.py list
python3 scripts/mba_faq.py get <id>
python3 scripts/mba_faq.py create --body-file /tmp/faq.json
python3 scripts/mba_faq.py update <id> --body-file /tmp/faq.json
python3 scripts/mba_faq.py delete <id> --yes
```
*Ref payload: `templates/faq.request.example.json`*

### 2. Knowledge: Websites
```bash
python3 scripts/mba_websites.py list
python3 scripts/mba_websites.py get <id>
python3 scripts/mba_websites.py create --body-file /tmp/web.json
python3 scripts/mba_websites.py update <id> --body-file /tmp/web.json
python3 scripts/mba_websites.py delete <id> --yes
```
*Ref payload: `templates/websites.request.example.json`*

### 3. Knowledge: Files
```bash
python3 scripts/mba_files.py list
python3 scripts/mba_files.py get <id>
python3 scripts/mba_files.py upload /path/to/file.pdf --name "Policy 2026"
python3 scripts/mba_files.py delete <id> --yes
```

### 4. Agent Skills (Behavior Instructions)
```bash
python3 scripts/mba_skills.py list
python3 scripts/mba_skills.py get <id>
python3 scripts/mba_skills.py create --body-file /tmp/skill.json
python3 scripts/mba_skills.py update <id> --body-file /tmp/skill.json
python3 scripts/mba_skills.py delete <id> --yes
```
*Ref payload: `templates/skill.request.example.json`*


### 5. UI Skills (Interactive Components)
```bash
python3 scripts/mba_ui_skills.py list
python3 scripts/mba_ui_skills.py get <id>
python3 scripts/mba_ui_skills.py create --body-file /tmp/uiskill.json
python3 scripts/mba_ui_skills.py update <id> --body-file /tmp/uiskill.json
python3 scripts/mba_ui_skills.py delete <id> --yes
```
*Ref payload: `templates/uiskill.request.example.json`*

## Audit Workflow: Company Information Validity
When auditing whether an MBA has valid company information, run read-only checks first and report evidence, not assumptions:
1. `python3 scripts/mba_knowledge.py faq list` — inspect all FAQ questions/answers for stale dates, unsupported claims, contact data, service descriptions, and risky superlatives.
2. `python3 scripts/mba_knowledge.py web list` — verify web sources have usable crawl output. Treat `pages_crawled: 0` or long-running `crawl_status: in_progress` as not yet useful grounding.
3. `python3 scripts/mba_knowledge.py skills list` — inspect behavior instructions that may cause invented customer/company facts (for example: “look up contact info” without fallback rules).
4. `python3 scripts/mba_ui_skills.py list` — review the agent's interactive UI components and their trigger instructions. Ensure the agent is permitted to send correct UI components (like a CTA button) instead of hallucinating links.
5. If runtime tests fail with `ELIGIBILITY_CHECK_FAILED`, pivot to `mba-onboard` checks (`settings get`, `allowlist list`) before judging answer quality.
6. Categorize findings as: stale/dated facts, unsupported claims needing source docs, missing grounding sources, risky behavior instructions, broken/missing UI components, and blocked runtime validation.

For dated operational facts (holiday hours, “besok”, event dates), recommend deleting or replacing with a source-of-truth answer unless the user provides current operating calendar data.
For big credibility claims (client counts, partner status, certifications, delivery rates, “only BSP”, notable clients), ask for verifiable company sources such as website pages, company profile PDF, certificates, case studies, or sales deck before promoting them as stable customer-facing knowledge.

## Important Rules
- **Destructive Actions**: Always require the `--yes` flag (e.g., `delete`).
- **No Direct API**: Never use `curl`. Always use `python3 scripts/mba_knowledge.py`.
- **Payload Generation**: Never invent JSON structures. Use the examples in `templates/` (inside this skill directory) as reference. Copy them to `/tmp`, modify, and supply via `--body-file`.
- **Website Knowledge Recreate Loop**: After `python3 scripts/mba_knowledge.py web create`, always verify with `python3 scripts/mba_knowledge.py web list`. If official public URLs return HTTP 200 but website knowledge remains stuck at `in_progress` with `pages_crawled: 0`, treat FAQ + File Knowledge as the primary grounding. If the user approves, delete the stuck website entries and recreate them, then recheck instead of assuming the URLs are bad.
- **Skill Mutations**: For `python3 scripts/mba_knowledge.py skills create/update/delete`, inspect existing skills first, draft and save payload locally, ask approval with exact command + impact, then execute and log outcome. See `references/agent-skill-mutation-workflow.md`.
- **UI Skill Setup**: Verify that flow-based UI skills (`component_type: flow`) actually reference an existing, published Flow ID before enabling them.
- **Connector-backed Behavior Skills**: When an agent skill describes behavior around connector tools, name the connector tool, define deterministic routing rules, include exception handling, and prohibit invented data not returned by the connector. For promo/voucher flows, explicitly forbid listing active promos, voucher codes, or offer names unless they were returned by the connector response.
- **Runtime Test Safety**: When opening `ai_audience` beyond `ALLOWLISTED_ONLY` for validation, save a rollback payload first, run the required tests immediately, and restore the original audience setting as soon as testing is done.
### References
- `references/faq-schema.md` - Schema limits and rules for FAQs.
- `references/business-info-schema.md` - Schema and constraints for Business Info.
- `references/file-knowledge-supported-types.md` - Supported extensions and size limits.
- `references/website-knowledge-crawl-status.md` - Crawl status enums and stuck behavior.
- `references/agent-skill-authoring-rules.md` - Schema and logical constraints for skill creation.
- `references/ui-skills-workflow.md` - Theory, benefits, and step-by-step workflow for configuring Interactive UI components.

