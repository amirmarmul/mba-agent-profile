---
name: mba-runtime
description: "Use to test Meta Business Agent (MBA) conversation routing, run evaluations, simulate test messages, and manage Thread Control (handoff to human agents)."
version: 1.0.0
author: Hermes Agent
license: MIT
prerequisites:
  commands:
    - mba
metadata:
  hermes:
    category: meta
    tags: [meta-business-agent, whatsapp, ai-agent, test, eval, handoff, thread-control]
---

# MBA Runtime & Eval Operator

## Overview
This skill manages the live runtime of a Meta Business Agent. You can test prompts, run predefined evaluation cases, pass thread control (handoff) to human inboxes, and trigger Agent Events.


Use the `python3 scripts/...` commands listed below for all operations.

## Commands

### 1. Test Agent
Send a test message directly to the agent (bypassing normal WhatsApp delivery rules) and save the output.
```bash
# Single turn
python3 scripts/mba_test.py "Apa jam operasional hari ini?" --save

# Multi-turn followup (requires conversation_id from previous run)
python3 scripts/mba_test.py "Dan besok?" --conversation-id <conv_id> --save
```
*Note: Saved results go to `workspace/tests/`. If it returns `ELIGIBILITY_CHECK_FAILED`, do not judge answer quality yet. First verify `ai_audience` and confirm the tester is allowlisted when audience is `ALLOWLISTED_ONLY` by running `python3 scripts/mba_settings.py get` and `python3 scripts/mba_allowlist.py list` from the `mba-onboard` skill. Use an allowlisted tester or add the intended tester before rerunning `mba_test.py`.*

### 2. Evaluations
Evaluate agent performance using predefined scenarios.
```bash
# List available eval scenarios
python3 scripts/mba_eval.py cases

# Run an eval job
python3 scripts/mba_eval.py run --eval-case-ids pfbid1,pfbid2 --body-file /tmp/eval.json
# (Ref payload: templates/eval.run.request.example.json)

# Check status of an eval job
python3 scripts/mba_eval.py status <job_id>

# Get results
python3 scripts/mba_eval.py summary --summary-ids <summary_id>
python3 scripts/mba_eval.py details --eval-ids <eval_id>
```
*Note: Results are auto-saved to `workspace/eval/` unless `--no-save` is passed.*

### 3. Thread Control (Handoff)
Transfer conversation control between the AI Agent and the Primary Receiver (e.g. human inbox app).
```bash
# Pass control from Agent to Human app
python3 scripts/mba_runtime.py thread-control pass <consumer_wa_id>

# Release control from Human app back to Agent
python3 scripts/mba_runtime.py thread-control release <consumer_wa_id>
```

### 4. Agent Events
Trigger asynchronous events (like manual handoff requests) into the conversation thread.
```bash
python3 scripts/mba_runtime.py event <consumer_wa_id> --body-file /tmp/event.json
python3 scripts/mba_runtime.py event-status <event_id>
```
*Ref payload: `templates/event.handoff.example.json`*

## Important Rules
- **Payload Generation**: Never invent JSON structures. Use the examples in `templates/` (inside this skill directory) as reference. Copy them to `/tmp`, modify, and supply via `--body-file`.
- **No Direct API**: Never use `curl`. Always use `python3 scripts/mba_runtime.py`.

### References
- `references/agent-test-eval-handoff-rules.md` - Test vs Eval payloads and thread handoff flow.
- `references/agent-events-rules.md` - Payload schema and rules for pushing events to agent memory.