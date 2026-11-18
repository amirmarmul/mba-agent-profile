# Installation Guide — MBA Copilot Profile (Human)

This installs the `meta-mba-agent@1.0.0` distribution: it turns Hermes into **MBA Copilot**, a DevOps assistant for Meta Business Agents (WhatsApp). Estimated time: 5–10 minutes.

Installed: `SOUL.md` identity, `config.yaml`, and the `mba-setup`, `mba-onboard`, `mba-knowledge`, `mba-connectors`, `mba-runtime` skills (`skills/meta/`). Your tokens, memories, sessions, and data are **never** installed or overwritten.

---

## 0. Prerequisites

| Requirement | Check | Notes |
|---|---|---|
| Hermes ≥ 0.23.0 | `hermes --version` | This machine: v0.23.2 ✓ |
| git | `git --version` | Only needed for a git-URL install |
| Distribution source | a local folder containing `distribution.yaml`, or `https://github.com/amirmarmul/mba-agent-profile.git` | Release tag: `v1.0.0` |
| Model / LLM provider | `hermes model` | Can be set after install; shipped `config.yaml` intentionally has `model: ""` |
| Meta token + Phone Number ID | Meta Business Portfolio System User | Configured via `mba-setup`, **not** via `.env` (see §2) |

> **Important:** `.env` is deprecated for `META_ACCESS_TOKEN` and `META_ENTITY_ID`. Those values belong in `<profile>/workspace/mba/config.json`, written by the `mba-setup` skill. Storing them in `.env` still works as a legacy fallback but prints a deprecation warning.

---

## 1. Install

### Option A — from git (recommended)

```bash
hermes profile install github.com/amirmarmul/mba-agent-profile \
  --name mba-agent --alias
```

### Option B — from a local folder

```bash
hermes profile install /path/to/mba-agent-profile \
  --name mba-agent --alias
```

What happens:
1. A **manifest preview** is printed (name, version, Hermes requirement).
2. You are asked `Proceed with install? [y/N]` — answer `y`.
3. The profile is created at `~/.hermes/profiles/mba-agent/` and **only** paths listed in `distribution_owned` are copied.
4. With `--alias`, a `mba-agent` wrapper script is added to PATH (optional).

For CI/automation only, add `-y` — this **skips the preview confirmation**, so use it only after a human has approved the manifest.

If the profile already exists:

```bash
hermes profile update mba-agent          # recommended
# or: hermes profile install ... --name mba-agent --force   (user data is preserved)
```

---

## 2. Choose a model

The shipped `config.yaml` deliberately has `model: ""`, so you pick your own provider.

**Option 1 — wizard (safest):**

```bash
hermes -p mba-agent setup       # or: hermes -p mba-agent model
```

**Option 2 — bundled custom LLM endpoint:**
Copy `config.yaml.example` → `config.yaml` in the profile folder, then set `HERMES_CUSTOM_LLM_API_KEY` in `.env`. This env var is a **provider credential**, not MBA config, so `.env` is the right place for it. Example provider: `llm` at `https://llm.matahari.my.id/v1`, model `fast`. Your `config.yaml` is **preserved** by `hermes profile update`.

---

## 3. Configure the Meta credentials (once)

Use `mba-setup`. It writes `<profile>/workspace/mba/config.json`, which every other MBA skill auto-detects.

**Recommended: enter the token at the interactive prompt in a real terminal.**

```bash
export HERMES_PROFILE_DIR=~/.hermes/profiles/mba-agent
cd "$HERMES_PROFILE_DIR/skills/meta/mba-setup"
python3 scripts/mba_setup.py            # prompts for token + entity ID
python3 scripts/mba_setup.py --verify   # expect "✓ Config verification passed"
python3 scripts/mba_setup.py --print-config-path
```

`HERMES_PROFILE_DIR` must be set when running outside Hermes; otherwise the script looks for config in the skill folder instead of the profile. Inside `hermes -p mba-agent ... chat`, Hermes sets it for you.

Avoid this form on shared machines — the token ends up in shell and chat history:

```bash
python3 scripts/mba_setup.py --force --access-token TOKEN --entity-id 123456789
```

**Never paste the token into chat.** The supported flow is the script's interactive prompt.

Two common traps:
- `META_ENTITY_ID` must be the numeric **Phone Number ID**, not the WABA ID. A WABA ID yields 404 on every endpoint.
- The token needs `whatsapp_business_messaging` **and** the `bizai_wa_enterprise_api_3p_access` capability. Missing the second one yields 403.

Pass criteria: `workspace/mba/config.json` contains `access_token`, `entity_id`, `api_version`, `base_url`, and `--verify` exits 0.

---

## 4. Verify

```bash
hermes profile list
hermes profile info mba-agent
hermes -p mba-agent doctor
hermes -p mba-agent skills list
hermes -p mba-agent chat -q "Who are you? State your identity and three core principles."
```

| Expected | Pass condition |
|---|---|
| `mba-agent` in the profile list | Profile registered |
| `Distribution: meta-mba-agent`, `Version: 1.0.0` | Manifest loaded |
| `mba-setup`, `mba-onboard`, `mba-knowledge`, `mba-connectors`, `mba-runtime` | `skills/meta/` copied |
| Answer says **MBA Copilot**, not "Hermes Agent" | `SOUL.md` is active |
| `python3 scripts/mba_setup.py --verify` exits 0 | Workspace config valid |

If the answer is still "Hermes Agent", you forgot `-p mba-agent`. Check `hermes profile list`, or run `hermes profile use mba-agent` to make it the default.

---

## 5. First use

Follow **`QUICKSTART.md`** for the `mba-setup` walkthrough — it uses plain chat only and stops there. Further skills are documented in their own `skills/meta/<skill>/SKILL.md` files.

Safe order:

```
mba-setup → mba-onboard (audit + allowlist) → mba-knowledge → mba-connectors → mba-runtime → only then ai_audience: EVERYONE
```

Do not open `EVERYONE` until test, eval, and allowlist checks pass.

---

## 6. Update, default, and uninstall

```bash
hermes profile update mba-agent                  # config.yaml preserved
hermes profile update mba-agent --force-config  # overwrite config.yaml from distro

hermes profile use mba-agent              # make default
hermes profile info mba-agent             # show version and source

# uninstall (destructive: removes profile data)
hermes backup
hermes profile alias --remove mba-agent   # only if --alias was used
hermes profile delete mba-agent
```

Update never touches `memories/`, `sessions/`, `auth.json`, `.env`, or `workspace/` — your `workspace/mba/config.json` survives updates.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Profile 'mba-agent' already exists` | Already installed | `hermes profile update mba-agent` or `--force` |
| `This distribution requires Hermes >=0.23.0` | Old Hermes | `hermes update`, then retry |
| `No distribution.yaml in ...` | Wrong source | Use a folder with `distribution.yaml` or a full git URL |
| Empty `model` / provider error | No model selected | §2 |
| `mba-*` skills not listed | Wrong profile / cwd | `hermes -p mba-agent skills list` |
| `Missing required env` / `ConfigError` | Workspace config missing — `.env` is deprecated | §3, run `mba-setup` |
| 401 / 403 / 404 from Meta | Token/permission/entity ID | §3 traps: Phone Number ID + `bizai_wa_enterprise_api_3p_access` |
| "Membrane"/HTTP 500 from API | Meta API behavior | See `mba-connectors`; verify with `get`/`list`, never guess the cause |

---

## Copy–paste summary

```bash
hermes profile install github.com/amirmarmul/mba-agent-profile --name mba-agent --alias
hermes -p mba-agent model
export HERMES_PROFILE_DIR=~/.hermes/profiles/mba-agent
cd "$HERMES_PROFILE_DIR/skills/meta/mba-setup" && python3 scripts/mba_setup.py && python3 scripts/mba_setup.py --verify
hermes profile info mba-agent
hermes -p mba-agent skills list
```
