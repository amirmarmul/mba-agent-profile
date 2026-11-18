#!/usr/bin/env python3
"""One-time setup: create workspace/mba/config.json from args, env, or interactive prompts."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _profile_workspace_config_path() -> Path:
    """Return the profile workspace config path: <HERMES_PROFILE_DIR>/workspace/mba/config.json"""
    profile_dir = os.getenv("HERMES_PROFILE_DIR") or os.getcwd()
    return Path(profile_dir) / "workspace" / "mba" / "config.json"


def _prompt_if_tty(prompt: str, default: str = "") -> str:
    """Prompt for input only if stdin is a TTY, otherwise use default."""
    if sys.stdin.isatty():
        if default:
            return input(f"{prompt} [{default}]: ").strip() or default
        return input(f"{prompt}: ").strip()
    return default


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize Meta Business Agent workspace configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/mba_setup.py --access-token TOKEN --entity-id 123456789
  python3 scripts/mba_setup.py  # interactive mode (requires TTY)

Environment variables:
  META_ACCESS_TOKEN   Meta access token
  META_ENTITY_ID      WhatsApp Business Phone Number ID
  META_API_VERSION    API version (default: 2.0.0)
  META_BASE_URL       Base URL (default: https://api.facebook.com)
        """
    )
    parser.add_argument(
        "--access-token", "-t",
        help="META_ACCESS_TOKEN from Meta Business Portfolio System User",
    )
    parser.add_argument(
        "--entity-id", "-e",
        help="META_ENTITY_ID (WhatsApp Business Phone Number ID, numeric)",
    )
    parser.add_argument(
        "--api-version", "-v",
        default="2.0.0",
        help="META_API_VERSION (default: 2.0.0)",
    )
    parser.add_argument(
        "--base-url", "-u",
        default="https://api.facebook.com",
        help="META_BASE_URL (default: https://api.facebook.com)",
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite existing config without prompting",
    )
    parser.add_argument(
        "--print-config-path",
        action="store_true",
        help="Print config path and exit",
    )

    args = parser.parse_args()

    config_path = _profile_workspace_config_path()

    if args.print_config_path:
        print(config_path)
        return 0

    print("=== MBA Setup ===")
    print(f"Config will be written to: {config_path}")
    print()

    # Check if config already exists
    if config_path.exists() and not args.force:
        if sys.stdin.isatty():
            overwrite = input("Config already exists. Overwrite? [y/N]: ").strip().lower()
            if overwrite != "y":
                print("Aborted.")
                return 0
        else:
            print("Config already exists. Use --force to overwrite.")
            return 1

    # Gather credentials: CLI args > env vars > interactive prompts
    access_token = (
        args.access_token
        or os.getenv("META_ACCESS_TOKEN", "").strip()
        or _prompt_if_tty("META_ACCESS_TOKEN")
    )
    while not access_token:
        print("Access token cannot be empty.", file=sys.stderr)
        access_token = _prompt_if_tty("META_ACCESS_TOKEN")

    entity_id = (
        args.entity_id
        or os.getenv("META_ENTITY_ID", "").strip()
        or _prompt_if_tty("META_ENTITY_ID (WhatsApp Business Phone Number ID)")
    )
    while not entity_id:
        print("Entity ID cannot be empty.", file=sys.stderr)
        entity_id = _prompt_if_tty("META_ENTITY_ID")

    api_version = args.api_version or os.getenv("META_API_VERSION", "2.0.0").strip() or "2.0.0"
    base_url = (args.base_url or os.getenv("META_BASE_URL", "https://api.facebook.com").strip() or "https://api.facebook.com").rstrip("/")

    # Validate entity_id is numeric
    if not entity_id.isdigit():
        print("WARNING: META_ENTITY_ID should be a numeric Phone Number ID (not WABA ID).", file=sys.stderr)

    # Write config
    config_data = {
        "access_token": access_token,
        "entity_id": entity_id,
        "api_version": api_version,
        "base_url": base_url,
    }

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config_data, indent=2) + "\n", encoding="utf-8")

    print()
    print(f"✓ Config written to {config_path}")
    print()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)