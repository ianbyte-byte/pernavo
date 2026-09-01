#!/usr/bin/env python3
"""Claude Code / Codex Stop adapter for the API test completion gate.

Blocks a stop or task-complete claim when the cwd has an API-test completion
story that the deterministic grader does not pass. Ordinary coding turns pass
through. Failure uses exit 2. Stdlib only.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from grade_api_jsonl import GradeError, format_reason, run


MATRIX_NAMES = (".pernavo/api-test-matrix.json", "api-test-matrix.json")
DONE = re.compile(
    r"(测试完成|测试已完成|已完成测试|测试全部通过|全部通过|可以上线|"
    r"业务功能\s*✅|测试结论|"
    r"tests?\s+(have\s+)?passed|testing complete|test(?:s|ing)?\s+(?:is|are)\s+complete|"
    r"ready to (?:ship|release|go live))",
    re.I,
)
API = re.compile(r"(jsonl|接口测试|业务测试|api test|/api/|http.?status|case matrix|用例矩阵)", re.I)
STOP_EVENTS = {"stop", "subagentstop", "taskcompleted", "task_completed"}


def _text(value: object) -> str:
    return value if isinstance(value, str) else ""


def payload_cwd(data: dict[str, Any]) -> Path:
    raw = _text(data.get("cwd") or data.get("working_directory") or data.get("workingDirectory"))
    if raw:
        return Path(raw)
    env = os.environ.get("PERNAVO_API_TEST_CWD")
    return Path(env) if env else Path.cwd()


def last_message(data: dict[str, Any]) -> str:
    for key in (
        "last_assistant_message",
        "lastAssistantMessage",
        "last_agent_message",
        "lastAgentMessage",
        "transcript",
        "message",
        "output",
        "response",
        "text",
    ):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value
        if isinstance(value, dict):
            nested = value.get("text") or value.get("content")
            if isinstance(nested, str) and nested.strip():
                return nested
    return ""


def hook_event(data: dict[str, Any]) -> str:
    return _text(data.get("hook_event_name") or data.get("hookEventName") or data.get("event")).lower()


def find_matrix(cwd: Path) -> Path | None:
    env = os.environ.get("PERNAVO_API_TEST_MATRIX")
    if env:
        path = Path(env).expanduser()
        return path if path.is_file() else None
    current = cwd.resolve()
    for directory in (current, *current.parents):
        for name in MATRIX_NAMES:
            candidate = directory / name
            if candidate.is_file():
                return candidate
        if directory.parent == directory:
            break
    return None


def claims_done(message: str) -> bool:
    return bool(DONE.search(message))


def api_context(message: str) -> bool:
    return bool(API.search(message))


def should_grade(data: dict[str, Any], matrix: Path | None, message: str) -> bool:
    event = hook_event(data)
    if event in {"taskcompleted", "task_completed"} and matrix is not None:
        return True
    if matrix is not None and claims_done(message):
        return True
    if matrix is None and claims_done(message) and api_context(message):
        return True
    return False


def allow() -> dict[str, Any]:
    return {"continue": True, "suppressOutput": True}


def block_payload(reason: str) -> dict[str, Any]:
    return {"decision": "block", "reason": reason}


def decide(data: dict[str, Any]) -> tuple[dict[str, Any], int]:
    cwd = payload_cwd(data)
    message = last_message(data)
    matrix = find_matrix(cwd)
    if not should_grade(data, matrix, message):
        return allow(), 0
    if matrix is None:
        return (
            block_payload(
                "api-test-gate incomplete: missing .pernavo/api-test-matrix.json; "
                "write the required_cases matrix before claiming API/business tests complete"
            ),
            2,
        )
    jsonl_env = os.environ.get("PERNAVO_API_TEST_JSONL")
    jsonl = Path(jsonl_env).expanduser() if jsonl_env else None
    try:
        report = run(matrix, jsonl, cwd)
    except GradeError as exc:
        return block_payload(f"api-test-gate incomplete: {exc}"), 2
    if report.get("pass"):
        return allow(), 0
    return block_payload(format_reason(report) if "reason" not in report else report["reason"]), 2


def main() -> int:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
        if not isinstance(data, dict):
            data = {}
    except json.JSONDecodeError:
        print(json.dumps(allow()))
        return 0
    try:
        payload, code = decide(data)
    except Exception as exc:
        message = last_message(data) if isinstance(data, dict) else ""
        if claims_done(message) or api_context(message):
            payload, code = block_payload(f"api-test-gate error: {exc}"), 2
        else:
            payload, code = allow(), 0
    text = json.dumps(payload, ensure_ascii=True)
    print(text)
    if code == 2:
        print(text, file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
