from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .handoff import (
    HandoffParseError,
    HandoffValidationError,
    format_handoff,
    parse_handoff_dict,
    parse_handoff_from_text,
)
from .project import check_project_layout
from .session_config import (
    load_session_config,
    validate_session_config,
    write_session_config_template,
)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        return _dispatch(args)
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return 130


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="chung-swarm")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="Check that Claude Code workflow files exist.")
    check.add_argument("--root", type=Path, default=Path.cwd())

    handoff = subparsers.add_parser("handoff", help="Parse/validate or generate a handoff envelope.")
    handoff_sub = handoff.add_subparsers(dest="handoff_cmd", required=True)

    handoff_validate = handoff_sub.add_parser("validate", help="Validate a handoff from stdin or file.")
    handoff_validate.add_argument("--file", type=Path, default=None)

    handoff_new = handoff_sub.add_parser("new", help="Generate a handoff JSON envelope.")
    handoff_new.add_argument("--next-role", required=True)
    handoff_new.add_argument("--next-instructions", required=True)
    handoff_new.add_argument(
        "--summary", help="Summary string or general summary if other summary fields are provided."
    )
    handoff_new.add_argument("--progress", help="Summary: What was accomplished")
    handoff_new.add_argument("--remaining", help="Summary: Outstanding tasks")
    handoff_new.add_argument("--risks", help="Summary: Potential blockers")
    handoff_new.add_argument("--changes", help="Summary: Key file modifications")
    handoff_new.add_argument(
        "--acceptance-criteria", nargs="+", help="List of verifiable conditions for completion"
    )
    handoff_new.add_argument("--context", help="Context as a JSON string")

    sess = subparsers.add_parser("session-config", help="Validate or initialize session_config.json.")
    sess_sub = sess.add_subparsers(dest="session_cmd", required=True)

    sess_validate = sess_sub.add_parser("validate", help="Validate a session_config.json file.")
    sess_validate.add_argument("--file", type=Path, default=Path(".claude/session_config.json"))

    sess_init = sess_sub.add_parser("init", help="Write a session_config.json template if missing.")
    sess_init.add_argument("--file", type=Path, default=Path(".claude/session_config.json"))
    sess_init.add_argument("--force", action="store_true")

    return parser


def _dispatch(args: argparse.Namespace) -> int:
    if args.command == "check":
        check = check_project_layout(args.root)
        if check.ok:
            print(f"OK: Claude Code workflow files present under {check.root}")
            return 0

        print(f"Missing required files under {check.root}:", file=sys.stderr)
        for p in check.missing:
            print(f"- {p.relative_to(check.root)}", file=sys.stderr)
        return 1

    if args.command == "handoff":
        if args.handoff_cmd == "validate":
            text = _read_text_from_cli(file_path=args.file)
            try:
                envelope = parse_handoff_from_text(text)
            except (HandoffParseError, HandoffValidationError) as e:
                print(f"Invalid handoff: {e}", file=sys.stderr)
                return 1
            print(format_handoff(envelope))
            return 0

        if args.handoff_cmd == "new":
            summary_obj = {}
            if args.progress:
                summary_obj["progress"] = args.progress
            if args.remaining:
                summary_obj["remaining"] = args.remaining
            if args.risks:
                summary_obj["risks"] = args.risks
            if args.changes:
                summary_obj["changes"] = args.changes

            final_summary = args.summary
            if summary_obj:
                if args.summary and "progress" not in summary_obj:
                    summary_obj["progress"] = args.summary
                final_summary = summary_obj

            if not final_summary:
                print(
                    "Error: --summary or at least one of (--progress, --remaining, --risks, --changes) is required.",
                    file=sys.stderr,
                )
                return 1

            handoff_dict: dict[str, Any] = {
                "type": "handoff",
                "next_role": args.next_role,
                "summary": final_summary,
                "next_instructions": args.next_instructions,
            }
            if args.acceptance_criteria:
                handoff_dict["acceptance_criteria"] = args.acceptance_criteria
            if args.context:
                try:
                    handoff_dict["context"] = json.loads(args.context)
                except json.JSONDecodeError as e:
                    print(f"Invalid JSON for --context: {e}", file=sys.stderr)
                    return 1

            try:
                envelope = parse_handoff_dict(handoff_dict)
                print(format_handoff(envelope))
                return 0
            except HandoffValidationError as e:
                print(f"Invalid handoff: {e}", file=sys.stderr)
                return 1

    if args.command == "session-config":
        if args.session_cmd == "validate":
            if not args.file.exists():
                print(f"Missing session config: {args.file}", file=sys.stderr)
                return 1
            data = load_session_config(args.file)
            result = validate_session_config(data)
            if result.ok:
                print(f"OK: {args.file}")
                return 0
            print(f"Invalid session config: {args.file}", file=sys.stderr)
            for err in result.errors:
                print(f"- {err}", file=sys.stderr)
            return 1

        if args.session_cmd == "init":
            if args.file.exists() and not args.force:
                print(f"Refusing to overwrite existing file: {args.file}", file=sys.stderr)
                return 1
            write_session_config_template(args.file)
            print(f"Wrote: {args.file}")
            return 0

    raise RuntimeError(f"Unhandled command: {args.command}")


def _read_text_from_cli(file_path: Path | None) -> str:
    if file_path is None:
        return sys.stdin.read()
    return file_path.read_text(encoding="utf-8")
