#!/usr/bin/env python3
"""Classify and verify the API test Stop hook; write only with --apply.

Live default install is AI_INSTALL.md: an installing agent reads the host JSON,
matches the existing hook-array shape, and merges by hand. This script's default
is --check (no write). --apply is for tests or an agent that already classified
the target. Never replace an existing hooks file.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from pathlib import Path


HOOK_MARKER = "api_test_stop_hook.py"
CLAUDE_EVENTS = ("Stop", "TaskCompleted")
CODEX_EVENTS = ("Stop", "SubagentStop")
OK_STATUSES = {"created", "merged", "skipped-identical", "blocked-parent"}


def default_script() -> Path:
    return Path(__file__).resolve().parent / HOOK_MARKER


def hook_entry(script: Path, timeout: int = 30) -> dict:
    command = f'{sys.executable} "{script}"'
    return {"type": "command", "command": command, "timeout": timeout}


def hook_group(entry: dict) -> dict:
    return {"hooks": [entry]}


def event_has_marker(hooks: dict, event: str, marker: str = HOOK_MARKER) -> bool:
    return marker in json.dumps(hooks.get(event) or [])


def uses_groups(items: list) -> bool:
    return bool(items) and all(
        isinstance(item, dict) and isinstance(item.get("hooks"), list) for item in items
    )


def append_event(hooks: dict, event: str, entry: dict) -> None:
    current = hooks.setdefault(event, [])
    if not isinstance(current, list):
        raise ValueError(f"hooks.{event} must be an array")
    payload = hook_group(entry) if (not current or uses_groups(current)) else entry
    current.append(payload)


def append_if_missing(hooks: dict, event: str, entry: dict) -> None:
    if event_has_marker(hooks, event):
        return
    append_event(hooks, event, entry)


def merge_events(config: dict, script: Path, events: tuple[str, ...]) -> dict:
    hooks = config.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("hooks must be an object")
    entry = hook_entry(script)
    for event in events:
        append_if_missing(hooks, event, entry)
    return config


def dump(data: dict) -> str:
    return json.dumps(data, ensure_ascii=True, indent=2) + "\n"


def classify_target(path: Path) -> str:
    if path.is_symlink():
        return "blocked-symlink"
    if path.exists() and not path.is_file():
        return "blocked-not-file"
    parent = path.parent
    if not path.exists() and (not parent.is_dir() or parent.is_symlink()):
        return "blocked-parent"
    return "ready"


def load_or_empty(path: Path) -> dict:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def write_json(path: Path, data: dict, created: bool) -> None:
    path.write_text(dump(data), encoding="utf-8")
    if created:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


def events_ready(hooks: dict, events: tuple[str, ...]) -> bool:
    return all(event_has_marker(hooks, event) for event in events)


def apply_host(
    path: Path,
    events: tuple[str, ...],
    script: Path,
    *,
    mode: str,
) -> dict:
    status = classify_target(path)
    report = {"path": str(path), "status": status, "events": list(events), "mode": mode}
    if status != "ready":
        return report
    existed = path.is_file()
    try:
        original = load_or_empty(path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        report["status"] = "blocked-invalid"
        report["error"] = str(exc)
        return report
    updated = json.loads(dump(original))
    hooks = updated.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        report["status"] = "blocked-invalid"
        report["error"] = "hooks must be an object"
        return report
    if mode == "check":
        report["status"] = "skipped-identical" if events_ready(hooks, events) else "missing"
        return report
    if mode in {"uninstall", "uninstall-dry-run"}:
        changed = False
        for event in list(hooks):
            items = hooks.get(event)
            if not isinstance(items, list):
                continue
            kept = [item for item in items if HOOK_MARKER not in json.dumps(item)]
            if kept != items:
                changed = True
                if kept:
                    hooks[event] = kept
                else:
                    del hooks[event]
        if not changed:
            report["status"] = "skipped-identical"
            return report
        report["status"] = "removed"
        if mode == "uninstall":
            write_json(path, updated, created=False)
        return report
    before = events_ready(hooks, events)
    merge_events(updated, script, events)
    after_hooks = updated.get("hooks") if isinstance(updated.get("hooks"), dict) else {}
    if before and events_ready(after_hooks, events) and dump(original) == dump(updated):
        report["status"] = "skipped-identical"
        return report
    report["status"] = "merged" if existed else "created"
    if mode == "apply":
        write_json(path, updated, created=not existed)
    return report


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify or apply the API test Stop hook. Default is --check (no write)."
    )
    parser.add_argument("--script", type=Path, default=default_script())
    parser.add_argument("--claude-settings", type=Path, default=Path.home() / ".claude" / "settings.json")
    parser.add_argument("--codex-hooks", type=Path, default=Path.home() / ".codex" / "hooks.json")
    parser.add_argument("--cursor-hooks", type=Path, default=None)
    parser.add_argument("--grok-hooks", type=Path, default=None)
    parser.add_argument("--check", action="store_true", help="read-only verify (default)")
    parser.add_argument("--dry-run", action="store_true", help="classify a merge without writing")
    parser.add_argument("--apply", action="store_true", help="write; not the live default install path")
    parser.add_argument("--skip-claude", action="store_true")
    parser.add_argument("--skip-codex", action="store_true")
    parser.add_argument("--uninstall", action="store_true", help="remove this marker only; requires --apply")
    parser.add_argument("--json", action="store_true", help="print the host status object (always on)")
    return parser.parse_args(argv)


def resolve_mode(args: argparse.Namespace) -> str:
    if args.uninstall and args.apply:
        return "uninstall"
    if args.uninstall and args.dry_run:
        return "uninstall-dry-run"
    if args.uninstall:
        raise SystemExit("uninstall requires --apply (or --dry-run); default is read-only")
    if args.apply:
        return "apply"
    if args.dry_run:
        return "dry-run"
    return "check"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    mode = resolve_mode(args)
    script = args.script.expanduser().resolve()
    report: dict = {"script": str(script), "mode": mode, "hosts": {}}
    if mode not in {"uninstall", "uninstall-dry-run"} and not script.is_file():
        print(f"missing hook script: {script}", file=sys.stderr)
        report["error"] = f"missing hook script: {script}"
        print(json.dumps(report, ensure_ascii=True, indent=2))
        return 1
    if not args.skip_claude:
        report["hosts"]["claude"] = apply_host(
            args.claude_settings.expanduser(),
            CLAUDE_EVENTS,
            script,
            mode=mode,
        )
    if not args.skip_codex:
        report["hosts"]["codex"] = apply_host(
            args.codex_hooks.expanduser(),
            CODEX_EVENTS,
            script,
            mode=mode,
        )
    if args.cursor_hooks is not None:
        report["hosts"]["cursor"] = apply_host(
            args.cursor_hooks.expanduser(),
            ("stop", "subagentStop"),
            script,
            mode=mode,
        )
    if args.grok_hooks is not None:
        report["hosts"]["grok"] = apply_host(
            args.grok_hooks.expanduser(),
            CODEX_EVENTS,
            script,
            mode=mode,
        )
    print(json.dumps(report, ensure_ascii=True, indent=2))
    statuses = [host["status"] for host in report["hosts"].values()]
    if not statuses:
        return 1
    if mode == "check":
        return 0 if all(status in {"skipped-identical", "blocked-parent"} for status in statuses) else 1
    if mode in {"uninstall", "uninstall-dry-run"}:
        return 0 if all(status in {"removed", "skipped-identical", "blocked-parent"} for status in statuses) else 1
    return 0 if all(status in OK_STATUSES for status in statuses) else 1


if __name__ == "__main__":
    raise SystemExit(main())
