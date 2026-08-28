#!/usr/bin/env python3
"""Best-effort cross-agent Skill usage event logger.

The hook deliberately records evidence metadata, not prompts, commands, or tool payloads.
It must never block the host agent when logging is unavailable.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows hosts simply lose cross-process locking.
    fcntl = None


DEFAULT_LOG = Path.home() / ".codex" / "skill-usage" / "events.jsonl"
SKILL_PATH = re.compile(r"(?:\.agents/skills|skills)/([a-z0-9][a-z0-9-]*)/SKILL\.md", re.I)
SKILL_PREFIX = re.compile(r"^(?:oh-my-claudecode:|claude:|codex:|\$)+", re.I)
SENSITIVE = re.compile(r"(?i)(bearer\s+|password\s*[:=]\s*|token\s*[:=]\s*)[^\s,;]+")


def _text(value: object) -> str:
    return value if isinstance(value, str) else ""


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", "replace")).hexdigest()


def _skill_name(value: object) -> str | None:
    raw = _text(value).strip()
    if not raw:
        return None
    match = SKILL_PATH.search(raw)
    if match:
        return match.group(1).lower()
    raw = SKILL_PREFIX.sub("", raw).strip().split()[0]
    if re.fullmatch(r"[a-z0-9][a-z0-9-]*", raw, re.I):
        return raw.lower()
    return None


def _tool_input(data: dict) -> dict:
    value = data.get("tool_input", data.get("toolInput", {}))
    return value if isinstance(value, dict) else {}


def _find_skill(data: dict, tool_input: dict) -> str | None:
    for key in ("skill", "skill_name", "skillName", "command"):
        skill = _skill_name(tool_input.get(key))
        if skill:
            return skill
    for value in (tool_input.get("path"), tool_input.get("file_path"), tool_input.get("filePath")):
        skill = _skill_name(value)
        if skill:
            return skill
    return _skill_name(data.get("skill_name", data.get("skillName")))


def _event_kind(hook_event: str, tool_name: str, skill: str | None, tool_input: dict) -> str:
    if hook_event.lower() in {"userpromptsubmit", "user_prompt_submit", "prompt"}:
        return "prompt_submitted"
    if skill and tool_name.lower() == "skill":
        return "skill_invoked"
    if skill:
        path = _text(tool_input.get("path") or tool_input.get("file_path") or tool_input.get("filePath"))
        command = _text(tool_input.get("command"))
        if SKILL_PATH.search(path) or (SKILL_PATH.search(command) and re.search(r"\b(cat|sed|head|tail)\b", command)):
            return "skill_file_read"
    return "hook_observed"


def build_event(data: dict, source: str, hook_event: str) -> dict:
    tool_input = _tool_input(data)
    tool_name = _text(data.get("tool_name", data.get("toolName")))
    skill = _find_skill(data, tool_input)
    prompt = _text(
        data.get(
            "prompt",
            data.get("user_prompt", data.get("userPrompt", data.get("message", data.get("content", "")))),
        )
    )
    raw_status = data.get("success", data.get("ok"))
    if raw_status is True:
        status = "success"
    elif raw_status is False:
        status = "failure"
    elif hook_event.lower() in {"posttooluse", "post_tool_use"}:
        status = "observed"
    else:
        status = "started"
    event = {
        "schema_version": "pernavo.skill_usage_event.v1",
        "event_id": _text(data.get("event_id", data.get("eventId"))) or _hash(
            "|".join((source, hook_event, _text(data.get("session_id", data.get("sessionId"))), tool_name, skill or "", os.urandom(8).hex()))
        ),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "hook_event": hook_event or "unknown",
        "kind": _event_kind(hook_event, tool_name, skill, tool_input),
        "status": status,
        "session_id": _text(data.get("session_id", data.get("sessionId")))[:256] or None,
        "cwd": _text(data.get("cwd", data.get("working_directory", data.get("workingDirectory"))))[:1024] or None,
        "tool_name": tool_name[:128] or None,
        "skill_name": skill,
    }
    if prompt:
        event["prompt_length"] = len(prompt)
        event["prompt_sha256"] = _hash(SENSITIVE.sub("[REDACTED]", prompt))
    return event


def append_event(event: dict, destination: Path = DEFAULT_LOG) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(destination.parent, 0o700)
    with destination.open("a", encoding="utf-8") as handle:
        try:
            os.chmod(destination, 0o600)
        except FileNotFoundError:
            pass
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.write(json.dumps(event, ensure_ascii=True, separators=(",", ":")) + "\n")
        handle.flush()
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        if not isinstance(data, dict):
            data = {}
        source = os.environ.get("SKILL_USAGE_SOURCE", "unknown").lower()
        hook_event = _text(data.get("hook_event_name", data.get("hookEventName", data.get("event"))))
        hook_event = hook_event or os.environ.get("SKILL_USAGE_HOOK_EVENT", "")
        destination = Path(os.environ.get("SKILL_USAGE_LOG", str(DEFAULT_LOG))).expanduser()
        append_event(build_event(data, source, hook_event), destination)
    except Exception:
        pass
    # Valid JSON is accepted by both Claude Code and Codex hook runners.
    print(json.dumps({"continue": True, "suppressOutput": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
