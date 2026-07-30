#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


SKILL_PATH_PATTERN = re.compile(
    r"(?P<path>(?:/|\.{0,2}/)?[^\s\"'<>]*\.agents/skills/"
    r"(?P<name>[a-z0-9-]+)/SKILL\.md)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--project-skill-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def split_names(value: str) -> set[str]:
    return set() if value == "-" else set(value.split(","))


def read_events(path: Path) -> list[dict]:
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def command_proves_read(item: dict, name: str) -> bool:
    if item.get("exit_code") == 0:
        return True
    output = item.get("aggregated_output", "")
    frontmatter_name = re.compile(rf"(?m)^name:\s*{re.escape(name)}\s*\r?$")
    return frontmatter_name.search(output) is not None


def infer_status(events: list[dict]) -> int:
    if any(event.get("type") == "turn.completed" for event in events):
        return 0
    return 124


def main() -> int:
    args = parse_args()
    project_skill_root = str(args.project_skill_root.resolve())
    with args.corpus.open(encoding="utf-8", newline="") as handle:
        corpus = {row["id"]: row for row in csv.DictReader(handle, delimiter="\t")}

    summary = []
    for result_path in sorted(args.results.glob("*.jsonl")):
        case_id = result_path.stem
        if case_id not in corpus:
            continue
        case = corpus[case_id]
        events = read_events(result_path)
        project_reads: set[str] = set()
        global_reads: set[str] = set()
        commands = []

        for event in events:
            item = event.get("item", {})
            if event.get("type") != "item.completed" or item.get("type") != "command_execution":
                continue
            command = item.get("command", "")
            proved = []
            for match in SKILL_PATH_PATTERN.finditer(command):
                path = match.group("path")
                name = match.group("name")
                if not command_proves_read(item, name):
                    continue
                proved.append(name)
                if (
                    project_skill_root in path
                    or path.startswith(".agents/skills/")
                    or path.startswith("./.agents/skills/")
                ):
                    project_reads.add(name)
                else:
                    global_reads.add(name)
            if proved:
                commands.append(
                    {
                        "command": command,
                        "exit_code": item.get("exit_code"),
                        "proved_reads": sorted(set(proved)),
                    }
                )

        loaded = project_reads | global_reads
        expected = split_names(case["expected"])
        forbidden = split_names(case["forbidden"])
        missing = sorted(expected - loaded)
        forbidden_hits = sorted(forbidden & loaded)
        status = infer_status(events)
        summary.append(
            {
                "id": case_id,
                "subject": case["subject"],
                "status": status,
                "project_reads": sorted(project_reads),
                "global_reads": sorted(global_reads),
                "missing": missing,
                "forbidden_hits": forbidden_hits,
                "pass": status == 0 and not missing and not forbidden_hits,
                "targeted_commands": commands,
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(sorted(summary, key=lambda item: item["id"]), ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    failed = [item["id"] for item in summary if not item["pass"]]
    print(
        json.dumps(
            {
                "passed": len(summary) - len(failed),
                "total": len(summary),
                "failed_ids": sorted(failed),
                "output": str(args.output),
            },
            ensure_ascii=False,
        )
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
