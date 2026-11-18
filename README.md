# meta-mba-agent — Hermes Agent Distribution

A Hermes Agent skill pack for Meta Business Agent operations.

## Profile

- **Name**: `mba-agent`
- **Distribution**: `meta-mba-agent@1.0.0`
- **Active profile**: `mba-agent` (alias: `mba-agent` → `hermes -p mba-agent`)

## Model / Provider

This profile uses an **empty model sentinel** (`model: ""`). After install, configure your model via:

```bash
hermes setup          # interactive setup (picks provider, API keys)
# or
hermes model          # change model from CLI
# or
# Dashboard → Models → Change
```

Supported providers: OpenRouter, OpenAI, Anthropic, Google (Gemini/Vertex), Nous Portal, xAI, DeepSeek, and 20+ more via OpenRouter.

Your `HERMES_CUSTOM_LLM_API_KEY` env var is available if you wired a custom endpoint; otherwise the installer will set their own provider key in `.env`.

## Meta Credentials

Required env vars (set in `.env`):

| Variable | Description |
|----------|-------------|
| `META_ACCESS_TOKEN` | Meta Graph API access token |
| `META_ENTITY_ID` | Default Meta entity ID for API workflows |

See `AGENTS.md` (workspace operating rules) and `SOUL.md` (agent identity) for full context.

## Skills (installed)

| Skill | Category | Source |
|-------|----------|--------|
| `mba-onboard` | meta | local |
| `mba-knowledge` | meta | local |
| `mba-connectors` | meta | local |
| `mba-runtime` | meta | local |
| `hermes-agent-skill-authoring` | software-development | official |

## Usage

```bash
hermes -p mba-agent chat     # start chatting with the MBA agent
hermes -p mba-agent skills   # list installed skills
hermes -p mba-agent profile  # profile info
```

## Installation (for installers)

```bash
# From this repo (local):
hermes profile install /path/to/mba-agent --name mba-agent --alias

# Or from git (after push + tag):
hermes profile install github.com/you/meta-mba-agent --name mba-agent --alias
```

## Distribution Manifest (`distribution.yaml`)

Key fields:

```yaml
name: meta-mba-agent
version: 1.0.0
hermes_requires: ">=0.23.0"
author: Amir Marmul
license: MIT

env_requires:
  - name: META_ACCESS_TOKEN
    required: true
  - name: META_ENTITY_ID
    required: true

distribution_owned:
  - SOUL.md
  - config.yaml
  - distribution.yaml
  - skills/meta/
```