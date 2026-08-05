#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shlex
from pathlib import Path
from typing import Iterable


SKILL_PATH_PATTERN = re.compile(
    r"(?P<path>(?:/|\.{0,2}/)?[^\s\"'<>]*?(?:(?:\.agents/)?skills)/"
    r"(?P<name>[a-z0-9-]+)/SKILL\.md)"
)
REDIRECTION_OPERATORS = {">", ">>", ">&", "&>", "&>>"}


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


def command_segments(command: str) -> list[list[str]]:
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars="|;&>")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return []

    segments: list[list[str]] = []
    segment: list[str] = []
    for token in tokens:
        if token in {";", "&&", "||", "|"}:
            if segment:
                segments.append(without_redirections(segment))
                segment = []
        else:
            segment.append(token)
    if segment:
        segments.append(without_redirections(segment))
    return segments


def without_redirections(arguments: list[str]) -> list[str]:
    retained = []
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument in REDIRECTION_OPERATORS:
            index += 2
            continue
        if (
            argument.isdigit()
            and index + 1 < len(arguments)
            and arguments[index + 1] in REDIRECTION_OPERATORS
        ):
            index += 3
            continue
        retained.append(argument)
        index += 1
    return retained


def positional_inputs(arguments: list[str], value_options: set[str]) -> list[str]:
    inputs = []
    iterator = iter(arguments)
    for argument in iterator:
        if argument == "--":
            inputs.extend(iterator)
            break
        if argument in value_options:
            next(iterator, None)
            continue
        if argument.startswith("--") and "=" in argument:
            continue
        if argument.startswith("-"):
            continue
        inputs.append(argument)
    return inputs


def script_reader_inputs(arguments: list[str], value_options: set[str]) -> list[str]:
    """Return input files after a sed/awk program, excluding option-supplied program files."""
    inputs = []
    program_seen = False
    iterator = iter(arguments)
    for argument in iterator:
        if argument == "--":
            remaining = list(iterator)
            if not program_seen and remaining:
                remaining.pop(0)
                program_seen = True
            inputs.extend(remaining)
            break
        if argument in value_options:
            next(iterator, None)
            program_seen = True
            continue
        if argument.startswith("--") and "=" in argument:
            program_seen = True
            continue
        if argument.startswith("-"):
            continue
        if program_seen:
            inputs.append(argument)
        else:
            program_seen = True
    return inputs


def target_reader_segments(command: str, path: str) -> list[list[str]]:
    targets = []
    for segment in command_segments(command):
        if segment and segment[0] == "command":
            segment = segment[1:]
        if not segment:
            continue
        reader, arguments = segment[0], segment[1:]
        if reader == "cat":
            inputs = positional_inputs(arguments, set())
        elif reader in {"head", "tail"}:
            inputs = positional_inputs(arguments, {"-n", "-c", "--lines", "--bytes"})
        elif reader == "sed":
            inputs = script_reader_inputs(arguments, {"-e", "-f", "--expression", "--file"})
        elif reader == "awk":
            inputs = script_reader_inputs(arguments, {"-f", "-v", "--file", "--assign"})
        else:
            continue
        if path in inputs:
            targets.append(segment)
    return targets


def reader_reads_target(command: str, path: str) -> bool:
    return bool(target_reader_segments(command, path))


def command_proves_read(item: dict, name: str, path: str) -> bool:
    """Accept evidence only when the same reader invocation names the target input file."""
    command = item.get("command", "")
    segments = command_segments(command)
    reader_segments = target_reader_segments(command, path)
    if len(segments) != 1 or len(reader_segments) != 1:
        return False
    output = item.get("aggregated_output", "")
    frontmatter_name = re.compile(rf"(?m)^name:\s*{re.escape(name)}\s*\r?$")
    if frontmatter_name.search(output):
        return True
    return item.get("exit_code") == 0


def is_project_read(path: str, project_skill_root: Path) -> bool:
    normalized = path[2:] if path.startswith("./") else path
    if normalized.startswith(".agents/skills/"):
        return True
    candidate = Path(path)
    if not candidate.is_absolute():
        return normalized.startswith("skills/")
    try:
        candidate.resolve().relative_to(project_skill_root.resolve())
    except ValueError:
        return False
    return True


def observation(events: Iterable[dict]) -> str:
    event_list = list(events)
    if any(event.get("type") in {"turn.timeout", "turn.timed_out"} for event in event_list):
        return "timeout"
    for event in event_list:
        item = event.get("item", {})
        if item.get("exit_code") == 124:
            return "timeout"
        if "timeout" in str(event.get("error", "")).lower():
            return "timeout"
    if any(event.get("type") == "turn.completed" for event in event_list):
        return "completed"
    return "unobserved"


def summarize(corpus_path: Path, results_path: Path, project_skill_root: Path) -> list[dict]:
    with corpus_path.open(encoding="utf-8", newline="") as handle:
        corpus = {row["id"]: row for row in csv.DictReader(handle, delimiter="\t")}

    summary = []
    for result_path in sorted(results_path.glob("*.jsonl")):
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
                if not command_proves_read(item, name, path):
                    continue
                proved.append(name)
                if is_project_read(path, project_skill_root):
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
        sample_observation = observation(events)
        completed = sample_observation == "completed"
        missing = sorted(expected - loaded)
        forbidden_hits = sorted(forbidden & loaded)
        target_observed = not missing and not forbidden_hits
        summary.append(
            {
                "id": case_id,
                "subject": case["subject"],
                "issued": True,
                "observation": sample_observation,
                "completed": completed,
                "execution_observed": completed,
                "target_observed": target_observed,
                "project_reads": sorted(project_reads),
                "global_reads": sorted(global_reads),
                "missing": missing,
                "forbidden_hits": forbidden_hits,
                "pass": completed and target_observed and not forbidden_hits,
                "targeted_commands": commands,
            }
        )
    return sorted(summary, key=lambda item: item["id"])


def main() -> int:
    args = parse_args()
    summary = summarize(args.corpus, args.results, args.project_skill_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
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
