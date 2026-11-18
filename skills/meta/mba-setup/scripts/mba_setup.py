#!/usr/bin/env python3
"""One-time setup: create workspace/mba/config.json from interactive prompts."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def _profile_workspace_config_path() -> Path:
    """Return the profile workspace config path: <HERMES_PROFILE_DIR>/workspace/mba/config.json"""
    profile_dir = os.getenv("HERMES_PROFILE_DIR") or os.getcwd()
    return Path(profile_dir) / "workspace" / "mba" / "config.json"


def main() -> int:
    config_path = _profile_workspace_config_path()

    print("=== MBA Setup ===")
    print(f"Config will be written to: {config_path}")
    print()

    # Check if config already exists
    if config_path.exists():
        overwrite = input("Config already exists. Overwrite? [y/N]: ").strip().lower()
        if overwrite != "y":
            print("Aborted.")
            return 0

    # Prompt for credentials
    print("Enter your Meta Business Agent credentials:")
    print("(Get these from your Meta Business Portfolio System User)")

    access_token = input("META_ACCESS_TOKEN: ").strip()
    while not access_token:
        print("Access token cannot be empty.")
        access_token = input("META_ACCESS_TOKEN: ").strip()

    entity_id = input("META_ENTITY_ID (WhatsApp Business Phone Number ID): ").strip()
    while not entity_id:
        print("Entity ID cannot be empty.")
        entity_id = input("META_ENTITY_ID: ").strip()

    # Optional: api_version and base_url
    api_version = input("META_API_VERSION [2.0.0]: ").strip() or "2.0.0"
    base_url = input("META_BASE_URL [https://api.facebook.com]: ").strip() or "https://api.facebook.com"

    # Validate entity_id is numeric
    if not entity_id.isdigit():
        print("WARNING: META_ENTITY_ID should be a numeric Phone Number ID (not WABA ID).")

    # Write config
    config_data = {
        "access_token": access_token,
        "entity_id": entity_id,
        "api_version": api_version,
        "base_url": base_url.rstrip("/"),
    }

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config_data, indent=2) + "\n", encoding="utf-8")

    print()
    print(f"✓ Config written to {config_path}")
    print()
    print("You can now run MBA scripts from any directory — they will auto-detect the config.")
    print("Example:")
    print("  python3 scripts/mba_eligibility.py")
    print("  python3 scripts/mba_settings.py get")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)