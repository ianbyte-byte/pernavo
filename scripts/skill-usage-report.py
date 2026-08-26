#!/usr/bin/env python3
"""Create an aggregate, secret-free Skill usage report from Codex history."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
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
    "review": re.compile(r"审查|review|diff|MR|PR|核对|检查|验证", re.I),
    "delivery": re.compile(r"部署|上线|发布|启动|IIS|Windows Server|docker|主分支|提交|commit|工作树", re.I),
    "implementation": re.compile(r"修复|实现|增加|移除|修改|编写|创建.*脚本|改为", re.I),
    "governance": re.compile(r"skills?|skillopt|subagents|记忆|文档|职位|风俗|朝代|投稿", re.I),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True, help="Codex thread_history SQLite database")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


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
