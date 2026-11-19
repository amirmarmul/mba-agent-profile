#!/usr/bin/env python3
"""Read-only MBA health probe.

Probes config, eligibility, settings, knowledge counts, allowlist, and saved
test/eval history, then computes ONE recommended next action (the priority
ladder). Never mutates anything: GET requests and local file reads only.

Output: JSON report on stdout. Exit 0 when config loaded, 1 when config is
missing/incomplete (run the mba-get-started wizard).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mba_common import (
    ConfigError,
    MetaConfig,
    _profile_workspace_config_path,
    request_json,
)


def _items(resp: Any) -> list:
    """Normalize a list-endpoint response to a list of objects."""
    if isinstance(resp, list):
        return resp
    if isinstance(resp, dict):
        for key in ("data", "items", "results"):
            if isinstance(resp.get(key), list):
                return resp[key]
        if "id" in resp:
            return [resp]
    return []


def _probe(fn) -> dict:
    try:
        return {"ok": True, "data": fn()}
    except Exception as exc:  # report errors verbatim; never invent causes
        return {"ok": False, "error": str(exc)}


def _knowledge(config: MetaConfig) -> dict:
    out: dict = {"ok": True, "faq_count": 0, "website_count": 0,
                 "website_completed": 0, "website_stuck": 0,
                 "website_no_data": 0, "file_count": 0,
                 "errors": {}}
    for name, path in (("faq", "agent_config/faq"),
                       ("websites", "agent_config/websites"),
                       ("files", "agent_config/files")):
        p = _probe(lambda path=path: request_json(config, "GET", path))
        if not p["ok"]:
            out["ok"] = False
            out["errors"][name] = p["error"]
            continue
        items = _items(p["data"])
        if name == "faq":
            out["faq_count"] = len(items)
        elif name == "files":
            out["file_count"] = len(items)
        else:
            out["website_count"] = len(items)
            for w in items:
                status = str(w.get("crawl_status", "")).lower()
                pages = w.get("pages_crawled") or 0
                if status == "completed" and pages > 0:
                    out["website_completed"] += 1
                elif status == "in_progress" and pages == 0:
                    out["website_stuck"] += 1
                elif status.startswith("completed") and pages == 0:
                    # e.g. completed_no_data: crawl finished but yielded nothing
                    out["website_no_data"] += 1
    return out


def _latest_file(directory: Path) -> Path | None:
    if not directory.is_dir():
        return None
    files = sorted(directory.glob("*.json"))
    return files[-1] if files else None


def _history(entity_id: str) -> dict:
    root = _profile_workspace_config_path().parent / entity_id / "runtime"
    out: dict = {"latest_test": None, "test_success": False,
                 "eval_summary_saved": False, "latest_eval_file": None}

    test_file = _latest_file(root / "tests")
    if test_file:
        info: dict = {"file": test_file.name,
                      "saved_at": datetime.fromtimestamp(
                          test_file.stat().st_mtime, tz=timezone.utc
                      ).strftime("%Y-%m-%dT%H:%M:%SZ")}
        try:
            payload = json.loads(test_file.read_text(encoding="utf-8"))
            body = payload.get("data") if isinstance(payload.get("data"), dict) else payload
            answer = body.get("agent_response") or ""
            no_response = body.get("no_response_reason") or ""
            info["eligibility_error"] = "ELIGIBILITY_CHECK_FAILED" in json.dumps(payload)
            info["has_answer"] = bool(answer.strip())
            out["test_success"] = info["has_answer"] and not info["eligibility_error"] and not no_response
        except (json.JSONDecodeError, OSError, AttributeError) as exc:
            info["parse_error"] = str(exc)
        out["latest_test"] = info

    eval_dir = root / "eval"
    if eval_dir.is_dir():
        summaries = sorted(eval_dir.glob("*-summary.json"))
        out["eval_summary_saved"] = bool(summaries)
        latest = _latest_file(eval_dir)
        if latest:
            out["latest_eval_file"] = latest.name
    return out


def _next_action(checks: dict) -> dict:
    """Priority ladder: hard blockers first, then brain, then proof, then launch."""
    elig = checks["eligibility"]
    if not elig["ok"]:
        err = elig.get("error", "")
        if any(code in err for code in ("HTTP 401", "HTTP 403", "HTTP 404")):
            return {"step": "repair-credentials", "skill": "mba-get-started",
                    "reason": f"Eligibility call rejected the credentials: {err}"}
        return {"step": "retry-connection", "skill": "mba-get-started",
                "reason": f"Eligibility call failed (non-auth): {err}"}
    if elig.get("eligible") is False:
        return {"step": "eligibility-blocked", "skill": "mba-onboard",
                "reason": "Meta reports this number is not eligible yet — a business-side "
                          "blocker, not a setup failure. Contact IT/Meta; details via mba-onboard."}

    know = checks["knowledge"]
    if not know["ok"]:
        return {"step": "inspect-knowledge", "skill": "mba-knowledge",
                "reason": f"Knowledge probes failed: {know['errors']}"}
    if know["faq_count"] + know["website_completed"] + know["file_count"] == 0:
        return {"step": "first-knowledge", "skill": "mba-knowledge",
                "reason": "The agent has no usable knowledge yet. Add the first FAQ "
                          "(or a processed file / completed website source)."}

    allow = checks["allowlist"]
    if not allow["ok"]:
        return {"step": "inspect-allowlist", "skill": "mba-onboard",
                "reason": f"Allowlist probe failed: {allow.get('error')}"}
    if allow["count"] == 0:
        return {"step": "add-tester", "skill": "mba-onboard",
                "reason": "Knowledge exists but no tester number is allowlisted. "
                          "Add a tester before the first test message."}

    hist = checks["history"]
    if not hist["test_success"]:
        return {"step": "first-test", "skill": "mba-runtime",
                "reason": "No successful saved test yet. Send the first test message "
                          "(allowlist propagation takes ~30s after adding a tester)."}
    if not hist["eval_summary_saved"]:
        return {"step": "run-eval", "skill": "mba-runtime",
                "reason": "A test passed but no eval summary is saved. Run an eval job "
                          "and retrieve its summary."}

    settings = checks["settings"]
    if not settings["ok"]:
        return {"step": "inspect-settings", "skill": "mba-onboard",
                "reason": f"Settings probe failed: {settings.get('error')}"}
    if settings.get("ai_audience") == "EVERYONE" and settings.get("rollout_enabled"):
        return {"step": "monitor", "skill": "mba-get-started",
                "reason": "Agent is live for everyone. Keep monitoring: re-run this health "
                          "check regularly and inspect connector logs on any tool-failure symptom."}
    return {"step": "launch-gate", "skill": "mba-onboard",
            "reason": "Tests and eval are in place. Review eval results and verify the "
                      "allowlist rollout before opening ai_audience to EVERYONE — "
                      "launch is a gated decision, not a wizard step."}


def main() -> int:
    report: dict = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "entity_id": None,
        "checks": {},
        "next_action": None,
    }
    try:
        config = MetaConfig.from_env()
    except ConfigError as exc:
        report["checks"]["config"] = {"ok": False, "error": str(exc)}
        report["next_action"] = {
            "step": "setup", "skill": "mba-get-started",
            "reason": "Config missing or incomplete. Run the get-started wizard "
                      "(token + entity ID from the IT package).",
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1

    report["entity_id"] = config.entity_id
    report["checks"]["config"] = {
        "ok": True,
        "entity_id": config.entity_id,
        "token_prefix": config.access_token[:4] + "...",
        "api_version": config.api_version,
        "base_url": config.base_url,
    }

    elig = _probe(lambda: request_json(config, "GET", "agent_eligibility"))
    if elig["ok"]:
        data = elig["data"]
        eligible = None
        if isinstance(data, dict):
            # Live API returns {"is_eligible": ...}; older docs show {"eligible": ...}
            eligible = data.get("eligible", data.get("is_eligible"))
        report["checks"]["eligibility"] = {
            "ok": True,
            "eligible": bool(eligible) if eligible is not None else None,
            "raw": data,
        }
    else:
        report["checks"]["eligibility"] = elig

    sett = _probe(lambda: request_json(config, "GET", "agent_config/settings"))
    if sett["ok"]:
        data = sett["data"]
        if isinstance(data, list):  # live API returns an array of agent configs
            data = next((d for d in data if isinstance(d, dict)), {})
        if not isinstance(data, dict):
            data = {}
        handoff = data.get("handoff") or {}
        report["checks"]["settings"] = {
            "ok": True,
            "rollout_enabled": bool((data.get("rollout") or {}).get("enabled")),
            "ai_audience": data.get("ai_audience"),
            "handoff_enabled": handoff.get("enabled"),  # None when absent
            "followup_enabled": bool((data.get("followup") or {}).get("enabled")),
        }
    else:
        report["checks"]["settings"] = sett

    report["checks"]["knowledge"] = _knowledge(config)

    allow = _probe(lambda: request_json(config, "GET", "agent_config/allowlist"))
    if allow["ok"]:
        report["checks"]["allowlist"] = {"ok": True, "count": len(_items(allow["data"]))}
    else:
        report["checks"]["allowlist"] = allow

    report["checks"]["history"] = _history(config.entity_id)
    report["next_action"] = _next_action(report["checks"])

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Aborted.", file=sys.stderr)
        sys.exit(1)
