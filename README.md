# mba-agent-profile — MBA Ops Assistant

A Hermes Agent profile distribution that turns Hermes into an ops assistant for
WhatsApp Meta Business Agents: guided get-started, knowledge and connector
management, testing/evals, and on-demand health checks with next-action
recommendations. Built for non-technical ops teams; technical detail stays
hidden unless you ask for "mode teknis".

Distribution: `meta-mba-agent@1.1.0` · profile name: `mba-agent`

## What you need from IT

One package, two values:

| Value | What it is |
|-------|-----------|
| Access token | Meta System User token with capability `bizai_wa_enterprise_api_3p_access` |
| Entity ID | Numeric WhatsApp Business **Phone Number ID** (not the WABA ID) |

One installation serves one tenant (one business number).

## Install

Prerequisite: Hermes is installed on your PC and your model/provider is already
configured (this distribution does not ship `config.yaml` and never touches
your model settings).

```bash
hermes profile install github.com/amirmarmul/mba-agent-profile --name mba-agent --alias
hermes -p mba-agent chat
```

On the first chat the agent automatically runs the get-started wizard:
a short orientation, then it asks for the token and entity ID (one question at
a time), proves the Meta API connection, and recommends your next action.
No commands to memorize.

## Update

```bash
hermes profile update mba-agent
```

Updates replace the shipped skills and SOUL.md; your `config.yaml`, `.env`,
`workspace/`, and memories are preserved.

## Skills

| Skill | Purpose |
|-------|---------|
| `mba-get-started` | Front door: wizard, credential gate, health check + next action |
| `mba-onboard` | Eligibility, agent settings, rollout allowlist |
| `mba-knowledge` | FAQs, websites, files, agent/UI skills |
| `mba-connectors` | Connectors, tools, auth, logs |
| `mba-runtime` | Test messages, evals, handoff, events |

## Daily use

Just talk to the agent: "cek kesehatan agent", "tambah FAQ tentang jam buka",
"test bot dengan pertanyaan refund". The agent reads real state before every
change and asks for confirmation in plain language before mutating anything.

## Where credentials live

`workspace/mba/config.json` — written by the wizard, gitignored, never
distributed. A leaked token is rotated by asking the agent to change
credentials (it confirms before overwriting).
