#!/usr/bin/env python3
"""Create an aggregate, secret-free Skill usage report from Codex history."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sqlite3
from zoneinfo import ZoneInfo
from collections import Counter
from pathlib import Path


CANONICAL = (
    "engineering-workflow",
    "codebase-slimming",
    "data-work",
    "performance-work",
    "change-review",
    "report-writer",
    "repository-governance",
    "test-engineering",
)
LEGACY = (
    "audit-agent-harness", "aviation-grade-engineering", "benchmark-performance",
    "coding-task-controller", "database-performance", "database-testing", "develop-production-code",
    "engineering-work-system", "exa-search", "gpt55-fusion", "graph-engineering", "open-code-review",
    "performance-measurement", "performance-review", "plan-code-change", "pplx-cli",
    "project-capability-engineering", "repository-knowledge-gardening", "review-mr", "runtime-performance",
    "sonarqube-review", "unknowns-field-guide", "verify-change-evidence", "web-performance",
)
ROUTES = {
    "performance": re.compile(r"性能|超时|延迟|内存|CPU|GC|并发|锁|redis|缓存|slow|latency|timeout", re.I),
    "data": re.compile(r"数据库|测试库|SQL|sqlcmd|视图|表|字段|存储过程|报表|query|N\+1|ORM", re.I),
    "review": re.compile(r"审查|代码审查|提交前自查|review|diff|MR|PR|pull request", re.I),
    "delivery": re.compile(r"部署|上线|发布|启动|IIS|Windows Server|docker|主分支|提交|commit|工作树", re.I),
    "implementation": re.compile(r"修复|实现|增加|移除|修改|编写|创建.*脚本|改为", re.I),
    "governance": re.compile(r"skills?|skillopt|subagents|记忆|文档|职位|风俗|朝代|投稿", re.I),
    "testing": re.compile(
        r"测试|单元|集成|接口|回归|验收|冒烟|黑盒|白盒|灰盒|覆盖率|test|testing|coverage|UAT|smoke",
        re.I,
    ),
}
ROUTE_SKILLS = {
    "performance": {"performance-work"},
    "data": {"data-work"},
    "review": {"change-review"},
    "delivery": {"engineering-workflow"},
    "implementation": {"engineering-workflow"},
    "governance": {"repository-governance"},
    "testing": {"test-engineering"},
}
SKILL_PATH_PATTERN = re.compile(
    r"(?:(?:/|\.{0,2}/)?[^\s\"'<>]*?(?:(?:\.agents/)?skills)/)"
    r"(?P<name>[a-z0-9-]+)/SKILL\.md",
    re.I,
)
READER_PATTERN = re.compile(r"\b(?:cat|sed|head|tail)\b[^\n;|&]*SKILL\.md", re.I)
GENERATED_USER_MARKERS = (
    "Complete the following task for the user",
    "Score how well the response satisfies the rubric",
    "You are SkillOpt's optimizer",
    "Reply with exactly",
)
REDACTION_PATTERNS = (
    (re.compile(r"(?i)(\bbearer\s+)[A-Za-z0-9._~+/=-]+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(\b(?:password|passwd|pwd|token|secret)\s*[:=]\s*)[^\s,;]+"), r"\1[REDACTED]"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True, help="Codex thread_history SQLite database")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sessions-root", type=Path, help="Codex JSONL session directory")
    parser.add_argument("--date", help="Local calendar date to include, YYYY-MM-DD")
    parser.add_argument("--timezone", default="Asia/Shanghai")
    return parser.parse_args()


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def redact_text(value: str) -> str:
    for pattern, replacement in REDACTION_PATTERNS:
        value = pattern.sub(replacement, value)
    return value


def event_timestamp(event: dict) -> dt.datetime | None:
    value = event.get("timestamp")
    if not isinstance(value, str):
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def is_generated_user_message(text: str) -> bool:
    return text.startswith("<recommended_plugins>") or any(
        marker in text for marker in GENERATED_USER_MARKERS
    )


def session_events(path: Path) -> list[dict]:
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def session_groups(sessions_root: Path, target_date: str | None, timezone: str) -> list[dict]:
    """Group continuation files by session id and retain only user-origin sessions."""
    local_zone = ZoneInfo(timezone)
    grouped: dict[str, list[dict]] = {}
    for path in sorted(sessions_root.rglob("*.jsonl")):
        events = session_events(path)
        if not events:
            continue
        meta = next((event.get("payload", {}) for event in events if event.get("type") == "session_meta"), {})
        session_id = meta.get("session_id")
        if not session_id or meta.get("thread_source") != "user":
            continue
        if target_date:
            timestamps = [event_timestamp(event) for event in events]
            if not any(timestamp and timestamp.astimezone(local_zone).date().isoformat() == target_date for timestamp in timestamps):
                continue
        grouped.setdefault(session_id, []).extend(events)
    return [{"session_id": session_id, "events": events} for session_id, events in grouped.items()]


def user_messages(events: list[dict]) -> list[str]:
    messages = []
    for event in events:
        if event.get("type") != "event_msg" or event.get("payload", {}).get("type") != "item_completed":
            continue
        item = event.get("payload", {}).get("item", {})
        if item.get("type") != "UserMessage":
            continue
        for part in item.get("content", []):
            text = normalize_text(part.get("text", "")) if isinstance(part, dict) else ""
            if text and not is_generated_user_message(text):
                messages.append(redact_text(text))
    return list(dict.fromkeys(messages))


def loaded_skills(events: list[dict], allowed: set[str] | None = None) -> set[str]:
    """Infer a load only from a reader command naming a SKILL.md path."""
    names: set[str] = set()
    for event in events:
        payload = event.get("payload", {})
        if payload.get("type") != "custom_tool_call" or payload.get("name") != "exec":
            continue
        source = payload.get("input", "")
        if not READER_PATTERN.search(source):
            continue
        for match in SKILL_PATH_PATTERN.finditer(source):
            name = match.group("name").lower()
            if allowed is None or name in allowed:
                names.add(name)
    return names


def task_completion(events: list[dict]) -> tuple[str, bool]:
    kinds = [event.get("payload", {}).get("type") for event in events if event.get("type") == "event_msg"]
    if "turn_aborted" in kinds:
        return "aborted", False
    if "task_complete" in kinds or any(event.get("type") == "turn.completed" for event in events):
        return "completed", True
    return "unobserved", False


def session_report(group: dict) -> dict:
    messages = user_messages(group["events"])
    text = " ".join(messages)
    applicable_routes = sorted(route for route, pattern in ROUTES.items() if pattern.search(text))
    applicable = sorted({skill for route in applicable_routes for skill in ROUTE_SKILLS[route]})
    loaded = sorted(loaded_skills(group["events"], set(CANONICAL)))
    explicit = sorted(
        name for name in CANONICAL
        if re.search(rf"(?<![a-z0-9-])(?:\$)?{re.escape(name)}(?![a-z0-9-])", text, re.I)
    )
    observation, completed = task_completion(group["events"])
    return {
        "session_id": group["session_id"],
        "request": text[:500],
        "applicable_routes": applicable_routes,
        "applicable_skills": applicable,
        "loaded_skills": loaded,
        "explicit_mentions": explicit,
        "missed_opportunity": sorted(set(applicable) - set(loaded)),
        "observation": observation,
        "completed": completed,
    }


def build_session_usage_report(sessions_root: Path, target_date: str | None, timezone: str) -> dict:
    tasks = [
        session_report(group)
        for group in session_groups(sessions_root, target_date, timezone)
        if user_messages(group["events"])
    ]
    applicable = Counter(skill for task in tasks for skill in task["applicable_skills"])
    loaded = Counter(skill for task in tasks for skill in task["loaded_skills"])
    missed = Counter(skill for task in tasks for skill in task["missed_opportunity"])
    explicit_only = Counter(
        skill for task in tasks for skill in task["loaded_skills"]
        if skill in task["explicit_mentions"] and skill not in task["applicable_skills"]
    )
    return {
        "format": "pernavo.skill_usage.v2",
        "source": str(sessions_root.resolve()),
        "date": target_date,
        "timezone": timezone,
        "task_count": len(tasks),
        "tasks": sorted(tasks, key=lambda task: task["session_id"]),
        "summary": {
            "applicable": dict(sorted(applicable.items())),
            "loaded": dict(sorted(loaded.items())),
            "missed_opportunity": dict(sorted(missed.items())),
            "explicit_only": dict(sorted(explicit_only.items())),
        },
        "method": "Top-level user sessions grouped by session_id; generated evaluator prompts excluded; loaded requires a reader command naming SKILL.md and is not inferred from mentions or available-skill listings.",
    }


def read_user_messages(db: Path) -> tuple[list[str], int, int]:
    uri = f"file:{db.resolve()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as connection:
        rows = connection.execute(
            "SELECT created_at_ms, item_json FROM thread_items WHERE item_type='userMessage' "
            "ORDER BY created_at_ms"
        ).fetchall()
    messages: list[str] = []
    timestamps = []
    for timestamp, raw in rows:
        try:
            item = json.loads(raw)
            text = " ".join(
                part.get("text", "") for part in item.get("content", []) if isinstance(part, dict)
            ).strip()
        except (TypeError, json.JSONDecodeError):
            continue
        if text:
            messages.append(text)
            timestamps.append(int(timestamp))
    return messages, (min(timestamps) if timestamps else 0), (max(timestamps) if timestamps else 0)


def main() -> int:
    args = parse_args()
    if args.sessions_root:
        report = build_session_usage_report(args.sessions_root, args.date, args.timezone)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"task_count": report["task_count"], "summary": report["summary"]}, ensure_ascii=False))
        return 0
    messages, first_ms, last_ms = read_user_messages(args.db)
    unique_messages = list(dict.fromkeys(re.sub(r"\s+", " ", message).strip() for message in messages))
    all_names = CANONICAL + LEGACY
    explicit = Counter()
    for message in messages:
        for name in all_names:
            if re.search(rf"(?<![a-z0-9-])(?:\$)?{re.escape(name)}(?![a-z0-9-])", message, re.I):
                explicit[name] += 1
    route_counts = Counter(
        route for message in unique_messages for route, pattern in ROUTES.items() if pattern.search(message)
    )
    report = {
        "format": "pernavo.skill_usage.v1",
        "source": str(args.db.resolve()),
        "message_count": len(messages),
        "unique_message_count": len(unique_messages),
        "first_created_at_ms": first_ms,
        "last_created_at_ms": last_ms,
        "explicit_skill_mentions": dict(sorted(explicit.items(), key=lambda pair: (-pair[1], pair[0]))),
        "canonical_route_counts": dict(route_counts),
        "legacy_names_not_in_default_root": sorted(name for name in LEGACY if explicit[name]),
        "method": "Counts userMessage text only; assistant/system prompt echoes are excluded.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("message_count", "unique_message_count", "canonical_route_counts")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
