---
name: mba-runtime
description: "Test MBA routing, run evals, manage handoff, trigger events."
version: 1.0.0
author: Amir Marmul (amirmarmul), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [meta-business-agent, whatsapp, ai-agent, test, eval, handoff, thread-control]
    related_skills: [mba-onboard, mba-knowledge, mba-connectors, mba-setup]
---

# MBA Runtime & Eval Operator

## Overview
This skill manages the live runtime of a Meta Business Agent. It covers sending test messages (bypassing WhatsApp delivery rules), running predefined evaluation cases, passing thread control (handoff) between the AI Agent and human inboxes, and triggering asynchronous Agent Events into conversation threads.

## When to Use
- Sending test messages to validate agent routing and answers
- Running evaluation jobs against predefined scenarios
- Checking eval job status and retrieving results (summary/details)
- Passing thread control from Agent to human (handoff) or releasing back to Agent
- Triggering asynchronous events (e.g., manual handoff requests) into a thread

Don't use for:
- Onboarding, eligibility, settings, allowlist → use `mba-onboard`
- Knowledge base (FAQs, Websites, Files, Skills) → use `mba-knowledge`
- Connectors or connector tools → use `mba-connectors`

## Prerequisites
- Profile workspace config at `workspace/mba/config.json` (created by `mba-setup`)
- If config missing: run `mba-setup` skill to create it
- Token must have:
  - Permission: `whatsapp_business_messaging`
  - Capability: `bizai_wa_enterprise_api_3p_access`
- Python 3.10+ with stdlib only (scripts use `urllib`, `json`, `pathlib`)
- For test/eval: agent must be eligible (`mba-onboard` eligibility check passes) and tester must be allowlisted if `ai_audience: "ALLOWLISTED_ONLY"`
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
terminal(command="python3 scripts/mba_test.py \"Apa jam operasional?\" --save", timeout=30)
terminal(command="python3 scripts/mba_eval.py cases", timeout=30)
terminal(command="python3 scripts/mba_eval.py run --eval-case-ids pfbid1,pfbid2 --body-file /tmp/eval.json", timeout=60)
terminal(command="python3 scripts/mba_runtime.py thread-control pass <consumer_wa_id>", timeout=30)
terminal(command="python3 scripts/mba_runtime.py event <consumer_wa_id> --body-file /tmp/event.json", timeout=30)
```

## Quick Reference
| Operation | Command |
|-----------|---------|
| Test agent (single turn) | `terminal(command="python3 scripts/mba_test.py \"message\" --save", timeout=30)` |
| Test agent (multi-turn) | `terminal(command="python3 scripts/mba_test.py \"followup\" --conversation-id <conv_id> --save", timeout=30)` |
| List eval cases | `terminal(command="python3 scripts/mba_eval.py cases", timeout=30)` |
| Run eval job | `terminal(command="python3 scripts/mba_eval.py run --eval-case-ids pfbid1,pfbid2 --body-file /tmp/eval.json", timeout=60)` |
| Eval job status | `terminal(command="python3 scripts/mba_eval.py status <job_id>", timeout=30)` |
| Eval summary | `terminal(command="python3 scripts/mba_eval.py summary --summary-ids <summary_id>", timeout=30)` |
| Eval details | `terminal(command="python3 scripts/mba_eval.py details --eval-ids <eval_id>", timeout=30)` |
| Handoff: pass to human | `terminal(command="python3 scripts/mba_runtime.py thread-control pass <consumer_wa_id>", timeout=30)` |
| Handoff: release to agent | `terminal(command="python3 scripts/mba_runtime.py thread-control release <consumer_wa_id>", timeout=30)` |
| Trigger event | `terminal(command="python3 scripts/mba_runtime.py event <consumer_wa_id> --body-file /tmp/event.json", timeout=30)` |
| Event status | `terminal(command="python3 scripts/mba_runtime.py event-status <event_id>", timeout=30)` |

## Procedure
**Rollout gate:** load `references/agent-test-eval-handoff-rules.md` before any test, eval, or thread-control run.

### A. Test Agent
1. **Single-turn test**
   - Run: `terminal(command="python3 scripts/mba_test.py \"Apa jam operasional hari ini?\" --save", timeout=30)`
   - Completion: Returns `conversation_id`, `response_text`, `tool_calls` (if any), `elapsed_ms`. Saved to `workspace/mba/<ENTITY_ID>/tests/`.

2. **Multi-turn follow-up**
   - Use `conversation_id` from previous run
   - Run: `terminal(command="python3 scripts/mba_test.py \"Dan besok?\" --conversation-id <conv_id> --save", timeout=30)`
   - Completion: Returns continued conversation with new response; same `conversation_id`.

3. **Eligibility/allowlist gate**
   - If response contains `ELIGIBILITY_CHECK_FAILED`: **do not judge answer quality**.
   - Run `mba-onboard` → `mba_settings.py get` (check `ai_audience`) and `mba_allowlist.py list`
   - If `ai_audience: "ALLOWLISTED_ONLY"`, add tester via `mba_allowlist.py add --entity <tester_wa_id>`
   - Re-run test after allowlist propagation (~30s).

### B. Evaluations
1. **List available eval cases**
   - Run: `terminal(command="python3 scripts/mba_eval.py cases", timeout=30)`
   - Completion: Returns array of case objects with `id`, `name`, `description`, `turns`.

2. **Run eval job**
   - Copy `assets/eval.run.request.example.json` → `/tmp/eval.json`
   - Set `eval_case_ids` (array), optional `config_overrides`
   - Run: `terminal(command="python3 scripts/mba_eval.py run --eval-case-ids pfbid1,pfbid2 --body-file /tmp/eval.json", timeout=60)`
   - Completion: Returns `job_id`; job runs asynchronously.

3. **Check job status**
   - Run: `terminal(command="python3 scripts/mba_eval.py status <job_id>", timeout=30)`
   - Completion: Returns `status` (`PENDING`/`RUNNING`/`COMPLETED`/`FAILED`), progress metrics.

4. **Retrieve results**
   - Summary: `terminal(command="python3 scripts/mba_eval.py summary --summary-ids <summary_id>", timeout=30)` — aggregate metrics.
   - Details: `terminal(command="python3 scripts/mba_eval.py details --eval-ids <eval_id>", timeout=30)` — per-turn breakdown.
   - Completion: Results auto-saved to `workspace/mba/<ENTITY_ID>/eval/` unless `--no-save`.

### C. Thread Control (Handoff)
1. **Pass control from Agent to Human (Primary Receiver)**
   - Run: `terminal(command="python3 scripts/mba_runtime.py thread-control pass <consumer_wa_id>", timeout=30)`
   - Completion: Returns `thread_control_state: "HUMAN"`; human inbox now owns the thread.

2. **Release control from Human back to Agent**
   - Run: `terminal(command="python3 scripts/mba_runtime.py thread-control release <consumer_wa_id>", timeout=30)`
   - Completion: Returns `thread_control_state: "AGENT"`; agent resumes ownership.

### D. Agent Events
1. **Trigger asynchronous event (e.g., handoff request)**
   - **Event schema:** load `references/agent-events-rules.md` before drafting the payload.
   - Copy `assets/event.handoff.example.json` → `/tmp/event.json`
   - Set `type: "handoff_event"`, `description`, `payload` (JSON string with `reason`, `priority`)
   - Run: `terminal(command="python3 scripts/mba_runtime.py event <consumer_wa_id> --body-file /tmp/event.json", timeout=30)`
   - Completion: Returns `event_id`; event queued for delivery.

2. **Check event status**
   - Run: `terminal(command="python3 scripts/mba_runtime.py event-status <event_id>", timeout=30)`
   - Completion: Returns `status` (`DELIVERED`/`FAILED`/`PENDING`), timestamps.

## Pitfalls
- **ELIGIBILITY_CHECK_FAILED on test** — not an answer quality issue. Verify `mba-onboard` eligibility, `ai_audience`, and allowlist membership first.
- **Allowlist propagation delay** — newly added testers may not be recognized for ~30 seconds after `mba_allowlist.py add`.
- **Eval job async** — `run` returns `job_id` immediately; poll `status` until `COMPLETED` or `FAILED` before fetching results.
- **Handoff requires valid consumer_wa_id** — must be a WhatsApp user who has messaged the business; unknown IDs return 404.
- **Event payload must be JSON string** — `payload` field in `event.handoff.example.json` is a stringified JSON object, not a nested object.
- **Destructive ops** — no destructive commands in this skill, but eval jobs consume quota; avoid unnecessary runs.
- **Payload generation** — never invent JSON; always use templates in `assets/`.

## Verification
- Test single-turn returns `conversation_id`, `response_text`, no `ELIGIBILITY_CHECK_FAILED`
- Test multi-turn continues same `conversation_id` with new response
- Eval cases list returns non-empty array with valid case IDs
- Eval run → status → summary/details chain completes with `COMPLETED` status and metrics
- Handoff pass returns `thread_control_state: "HUMAN"`; release returns `thread_control_state: "AGENT"`
- Event trigger returns `event_id`; event-status eventually shows `DELIVERED`
- All results auto-saved to `workspace/mba/<ENTITY_ID>/tests/` and `workspace/mba/<ENTITY_ID>/eval/` respectively
- No 401/403/404 on any operation