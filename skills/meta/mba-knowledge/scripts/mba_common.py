#!/usr/bin/env python3
"""Common helpers for Meta Business Agent scripts."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_BASE_URL = "https://api.facebook.com"
DEFAULT_API_VERSION = "2.0.0"

# Profile workspace config path (Hermes profile root + workspace/mba/config.json)
def _profile_workspace_config_path() -> Path:
    """Return <profile>/workspace/mba/config.json.
    Resolution order: HERMES_PROFILE_DIR env > script location (skills/meta/<skill>/scripts/) > cwd."""
    env = os.getenv("HERMES_PROFILE_DIR")
    if env:
        return Path(env) / "workspace" / "mba" / "config.json"
    here = Path(__file__).resolve()
    for parent in here.parents:
        if parent.name == "meta" and parent.parent.name == "skills":
            return parent.parent.parent / "workspace" / "mba" / "config.json"
    return Path(os.getcwd()) / "workspace" / "mba" / "config.json"


class ConfigError(RuntimeError):
    """Raised when required environment is missing."""


@dataclass(frozen=True)
class MetaConfig:
    access_token: str
    entity_id: str
    api_version: str = DEFAULT_API_VERSION
    base_url: str = DEFAULT_BASE_URL

    @classmethod
    def from_env(cls) -> "MetaConfig":
        # 1) Try profile workspace config first
        workspace_config = _profile_workspace_config_path()
        if workspace_config.exists():
            try:
                data = json.loads(workspace_config.read_text(encoding="utf-8"))
                access_token = data.get("access_token", "").strip()
                entity_id = data.get("entity_id", "").strip()
                api_version = data.get("api_version", DEFAULT_API_VERSION).strip() or DEFAULT_API_VERSION
                base_url = data.get("base_url", DEFAULT_BASE_URL).strip() or DEFAULT_BASE_URL

                missing: list[str] = []
                if not access_token:
                    missing.append("access_token (in workspace config)")
                if not entity_id:
                    missing.append("entity_id (in workspace config)")
                if not missing:
                    return cls(
                        access_token=access_token,
                        entity_id=entity_id,
                        api_version=api_version,
                        base_url=base_url.rstrip("/"),
                    )
            except (json.JSONDecodeError, OSError):
                pass  # fall through to .env

        # 2) No workspace config: fail fast. Env vars are never used as
        # credentials (tenant isolation); mba-get-started is the single gate.
        raise ConfigError(
            f"MBA config missing or incomplete at {workspace_config}. "
            "Run the 'mba-get-started' skill: it asks the user for META_ACCESS_TOKEN "
            "and META_ENTITY_ID, then writes the config."
        )

    def url(self, path: str, query: dict[str, Any] | None = None) -> str:
        clean_path = path.lstrip("/")
        url = f"{self.base_url}/{self.entity_id}/{clean_path}"
        if query:
            filtered = {k: v for k, v in query.items() if v is not None and v != ""}
            if filtered:
                url = url + "?" + urllib.parse.urlencode(filtered, doseq=True)
        return url

    def headers(self, include_json_content_type: bool = True) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-API-Version": self.api_version,
            "Accept": "application/json",
            "User-Agent": "curl/7.68.0",
        }
        if include_json_content_type:
            headers["Content-Type"] = "application/json"
        return headers

    def auth_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "X-API-Version": self.api_version,
            "Accept": "application/json",
            "User-Agent": "curl/7.68.0",
        }


def request_multipart(
    config: MetaConfig,
    method: str,
    path: str,
    *,
    fields: dict[str, str],
    file_fields: dict[str, tuple[str, bytes]],
) -> Any:
    boundary = uuid.uuid4().hex
    parts: list[bytes] = []

    for name, value in fields.items():
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode("utf-8"))

    for name, (filename, content) in file_fields.items():
        mime = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{filename}\"\r\nContent-Type: {mime}\r\n\r\n".encode("utf-8"))
        parts.append(content)
        parts.append(b"\r\n")

    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    data = b"".join(parts)

    headers = config.auth_headers()
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"

    req = urllib.request.Request(
        config.url(path),
        data=data,
        headers=headers,
        method=method.upper(),
    )
    return _send_req(req)


def _send_req(req: urllib.request.Request) -> Any:
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            if not raw:
                return {"status": resp.status}
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {exc.reason}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc


def request_json(
    config: MetaConfig,
    method: str,
    path: str,
    *,
    query: dict[str, Any] | None = None,
    body: dict[str, Any] | list[Any] | None = None,
) -> Any:
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    headers = config.headers(include_json_content_type=body is not None)
    req = urllib.request.Request(
        config.url(path, query=query),
        data=data,
        headers=headers,
        method=method.upper(),
    )
    return _send_req(req)


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def _workspace_output_root(entity_id: str) -> Path:
    """Return workspace/mba/<ENTITY_ID>/ under the profile workspace."""
    return _profile_workspace_config_path().parent / entity_id


def write_run_output(kind: str, payload: Any, prefix: str = "run", skill: str = "knowledge") -> Path:
    config = MetaConfig.from_env()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_prefix = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in prefix).strip("-") or "run"
    out_dir = _workspace_output_root(config.entity_id) / skill / kind
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{timestamp}-{safe_prefix}.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return out_path


def add_save_arg(parser: argparse.ArgumentParser, default: bool = False) -> None:
    action = "store_true" if not default else "store_false"
    flag = "--save" if not default else "--no-save"
    parser.add_argument(flag, action=action, dest="save", default=default, help="Save response JSON under workspace/mba/<ENTITY_ID>/<skill>/")


def add_yes_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--yes", action="store_true", help="Confirm destructive operation")


def require_yes(args: argparse.Namespace, action: str) -> None:
    if not getattr(args, "yes", False):
        raise ConfigError(f"Refusing to {action} without --yes")


def load_json_file(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--agent-id",
        default="",
        help="Optional Meta Business Agent settings/configuration ID.",
    )


def main_error(exc: BaseException) -> int:
    print(f"ERROR: {exc}", file=sys.stderr)
    return 1