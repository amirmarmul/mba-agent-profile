# AGENTS.md — Meta Business Agent (MBA) Workspace

## 1. Project Context
This repository contains the Meta Business Agent (MBA) Skill Kit, a suite of isolated Hermes skills and embedded Python scripts used to configure, test, and operate Meta's WhatsApp Business AI Agents.

This workspace follows a strict Hermes-First architecture:
- every skill is self-contained
- every skill carries its own `SKILL.md`, `scripts/`, and `templates/`
- operational artifacts are isolated by tenant using the entity ID

You should follow `SOUL.md` for identity, priorities, and decision style.
You should follow this file (`AGENTS.md`) for repository-specific operating rules.

## 2. First Run
If you are newly spawned in this repository:

1. Source the environment:
   ```bash
   set -a; . ./.env; set +a
   ```
   Required variables:
   - `META_ACCESS_TOKEN`
   - `META_ENTITY_ID`

2. Verify Hermes can see the MBA skills:
   ```bash
   hermes skills list
   ```

3. If any MBA skills are missing, install them:
   ```bash
   hermes skills install ./skills/mba-onboard
   hermes skills install ./skills/mba-knowledge
   hermes skills install ./skills/mba-connectors
   hermes skills install ./skills/mba-runtime
   ```

4. Before mutating anything, determine the active tenant:
   - read `META_ENTITY_ID`

## 3. Repo Layout
- `skills/`
  - isolated Hermes skill bundles
  - each skill contains:
    - `SKILL.md`
    - `scripts/*.py`
    - `templates/*.json`
- `mba/<META_ENTITY_ID>/`
  - multi-tenant outputs and audit trail
  - includes tests, eval outputs, and changelog artifacts
- `docs/`
  - architecture decisions, research, tracker documents, and raw source material

## 4. Available Skills
| Skill | Domain / Purpose |
|-------|------------------|
| `mba-onboard` | Check eligibility, manage settings, manage allowlist, control rollout safety. |
| `mba-knowledge` | Manage FAQs, website knowledge, file knowledge, Meta Agent Skills (behavior instructions), and Agent UI Skills (interactive components). |
| `mba-connectors` | Manage connectors, auth payloads, connector tools, and connector logs. |
| `mba-runtime` | Run agent tests, evaluations, events, and thread control actions. |

## 5. Workflows
Map every user request to the correct skill domain and local script.

Example: “Update FAQ for the holiday promo.”
1. Identify the active `META_ENTITY_ID`.
2. Draft the JSON payload locally under:
   `mba/<META_ENTITY_ID>/changelog/payloads/YYYY-MM-DD_<action>.json`
3. Validate the payload quality before execution.
4. Explain what will happen and what the impact is.
5. Wait for explicit approval.
6. Execute the relevant local script, for example:
   ```bash
   python3 scripts/mba_faq.py update <id> --body-file <payload_path>
   ```
7. Append an audit entry to:
   `mba/<META_ENTITY_ID>/changelog/history.md`

Use similar workflow for:
- reviewing or updating agent skills
- configuring interactive UI components (UI Skills) to prevent link hallucination
- diagnosing connector failures from logs
- uploading knowledge files
- changing onboarding settings or allowlists

## 6. Approval Gates
Proceed automatically for:
- read-only checks (`list`, `get`, `logs`, `status`)
- creating local payload drafts
- saving payloads under `mba/<META_ENTITY_ID>/changelog/payloads/`
- writing markdown audit logs

Always ask before, and explain impact, for:
- any script that mutates Meta-managed state
- `create`
- `update`
- `delete`
- `upload`
- `auth`
- allowlist changes
- audience / rollout changes
- thread control changes that affect live conversation routing

When asking approval, state:
- exact script you will run
- target entity
- object being changed
- likely effect if the command succeeds

## 7. Logging & Multi-tenant Rules
This workspace is multi-tenant. Never mix customer/entity data.

All generated payloads, test outputs, eval outputs, and audit logs must be stored under:
`mba/<META_ENTITY_ID>/...`

Required audit trail location:
`mba/<META_ENTITY_ID>/changelog/history.md`

Required payload archive location:
`mba/<META_ENTITY_ID>/changelog/payloads/`

Each audit entry should include:
- Date/Time
- Entity ID
- Action
- Script executed
- Payload path
- Reason / Context
- Outcome / Response summary

Use the changelog as operational memory for future decisions.
Learn from previous changes instead of treating each run as stateless.

## 8. Known Issues / Error Handling
| Issue | Resolution |
|-------|------------|
| `500 Authorization Failed` on connector operations | Known Meta Membrane quirk. The DB commit may still succeed. Verify with `list` or `get` before retrying or assuming failure. |
| `ELIGIBILITY_CHECK_FAILED` during runtime tests | Check onboarding settings and allowlist first. The tester may not be allowed to access the agent. |
| Connector tool appears in list/get but fails on run | Treat metadata existence and runtime readiness as different states. Verify with an actual `run` request. |
| Local Python import issues | Execute scripts from the relevant skill directory so `mba_common.py` resolves locally. |
| Empty or missing `.env` | Stop and ask the user to provide the required Meta credentials and entity context before continuing. |

## 9. Important Paths
- Raw research/reference material:
  - `docs/`
- Payload templates:
  - `skills/<skill>/templates/`
- Tenant audit history:
  - `mba/<META_ENTITY_ID>/changelog/history.md`
- Tenant payload archive:
  - `mba/<META_ENTITY_ID>/changelog/payloads/`

Do not invent JSON schemas when templates already exist inside a skill.
Prefer reading the closest template and adapting it to the requested operation.
