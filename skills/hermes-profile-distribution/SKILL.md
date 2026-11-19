---
name: hermes-profile-distribution
description: "Package, ship, and update Hermes profile distributions."
version: 0.1.0
author: Amir Marmul (amirmarmul), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes-agent, profile, distribution, install, update]
    related_skills: [hermes-agent-skill-authoring]
---

# Hermes Profile Distribution

Package a Hermes profile (SOUL.md, skills, manifest) as a git repo that other machines install with `hermes profile install` and refresh with `hermes profile update`. Semantics below verified against `hermes_cli/profile_distribution.py` and `hermes_cli/profile_cmd.py`.

## When to Use
- Shipping a skill pack / agent profile to other users or machines
- Updating an installed distribution without clobbering recipient settings
- Diagnosing what install/update overwrites vs preserves

Don't use for: authoring SKILL.md content and frontmatter → `hermes-agent-skill-authoring`.

## Core Semantics
| Situation | Behavior |
|---|---|
| Fresh install | Shallow-clone DEFAULT branch to temp, copy owned payload to `~/.hermes/profiles/<name>`; names `default`/reserved refused |
| Profile already exists | Install refuses without `--force`; correct path is `hermes profile update <name>` |
| Update | Re-clones the recorded `source:`; overwrites owned entries; PRESERVES `config.yaml` unless `--force-config` |
| `--force` install | Overwrites owned + `config.yaml`; user data still preserved |
| `distribution_owned` | Explicit allowlist — only declared paths copied. OMITTING it makes the whole payload (minus excludes) owned; keep the list explicit |
| `config.yaml` | Owned by default but preserved on update; replaced only on fresh install / `--force` / `--force-config` |
| Owned dirs (`skills/<cat>/`) | Merged per authored root: shipped skills replaced wholesale, user-added skills kept, upstream-deleted skills NOT removed locally |
| `cron/jobs.json` | Merged by job id; new jobs arrive paused; local paused/enabled state survives |
| Non-owned paths | Never touched: `workspace/`, `memories/`, `sessions/`, `.env`, `auth.json`, etc. — hard-excluded even if shipped |
| `.env.template` | Lands as `.env.EXAMPLE`, never shadows a real `.env` |
| `env_requires` | Informational only: preview labels + `.env.EXAMPLE` generation; never blocks install |
| Version / git tags | Installer always clones the default branch; tags and manifest `version` are informational; only `hermes_requires` is enforced |
| Empty model sentinel | First interactive chat offers provider setup only when NO provider is configured; with credentials present it silently falls back to the provider's default model |

## Procedure — ship or update a distribution
1. Keep secrets and tenant data out of the payload: gitignore credential stores and workspace config holding live tokens; prove it with `terminal(command="git check-ignore -v <path>")` before pushing.
2. Declare `distribution_owned` explicitly (e.g. `SOUL.md`, `distribution.yaml`, `skills/<cat>/`). If recipients configure their own models, do not ship `config.yaml`: drop it from owned and from git tracking (`git rm --cached`, keep the local file); ship `config.yaml.example` as reference instead.
3. `env_requires`: list only variables the payload actually consumes — misleading entries make installers set values nothing reads.
4. Bump `version` in `distribution.yaml` (informational), commit, push to the DEFAULT branch — that push is the release; a tag is optional convention, not a distribution mechanism.
5. Recipient commands: fresh `hermes profile install github.com/<owner>/<repo> --name <name> --alias`; existing `hermes profile update <name>` (add `--force-config` only when intentionally resetting model settings).
6. Verify on a scratch target before announcing: install into a throwaway profile name and inspect exactly what landed. Stage the payload with `git archive HEAD | tar -x -C <staging-dir>` and install from the staging dir — installing from a live profile directory scans gitignored runtime dirs too and can refuse on stray symlinks (e.g. `lsp/bin/*`). After the test, `hermes profile delete <scratch-name> -y`.

## Pitfalls
- **Installing from a live profile directory** — the symlink scan covers the whole directory, including gitignored runtime artifacts; a stray symlink (LSP servers, node_modules) refuses the install even though the file would never be shipped. Stage via `git archive HEAD` instead.
- **Shipping your own `config.yaml` provider/key** — fresh installs inherit your model, and `--force` wipes recipient settings. Ship no `config.yaml` (or an empty-model sentinel without provider) when recipients own their models.
- **Omitting `distribution_owned`** — does NOT narrow ownership to defaults; code treats the entire payload as owned. Keep the allowlist explicit.
- **Pushing a tag as a release** — the installer reads the default branch only; tags change nothing for recipients.
- **User-local edits inside owned files** — `SOUL.md` and other owned entries are overwritten on every update; keep recipient customizations in non-owned paths.
- **Expecting upstream skill deletions to propagate** — update merges per authored root and never removes local skills; removals need explicit instructions to recipients.

## Verification
- `git check-ignore` confirms every secret/tenant path is excluded from the payload
- Fresh install into a scratch profile lands exactly the owned entries
- Update on a profile with custom `config.yaml` preserves model/provider settings
- `hermes profile info` shows the expected distribution name@version and source
