# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
import argparse
import json
import sys
from typing import Optional, Sequence

from agentctl_commands import doctor, error_result, explain, load_event, memory_search
from agentctl_data import load_config, load_memory
from agentctl_types import DataError, JsonValue


def add_dry_run(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--dry-run", action="store_true", help="accepted compatibility no-op")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="agentctl", description="Read-only local agent harness inspector")
    add_dry_run(root)
    commands = root.add_subparsers(dest="command", required=True)
    doctor_parser = commands.add_parser("doctor", help="validate canonical local data")
    doctor_parser.add_argument("--config", required=True)
    doctor_parser.add_argument("--json", action="store_true")
    add_dry_run(doctor_parser)
    explain_parser = commands.add_parser("explain", help="resolve canonical event routes")
    explain_parser.add_argument("--config", required=True)
    explain_parser.add_argument("--event", required=True)
    explain_parser.add_argument("--json", action="store_true")
    add_dry_run(explain_parser)
    memory_parser = commands.add_parser("memory", help="inspect canonical memory")
    add_dry_run(memory_parser)
    memory_commands = memory_parser.add_subparsers(dest="memory_command", required=True)
    search_parser = memory_commands.add_parser("search", help="search canonical JSONL memory")
    search_parser.add_argument("--config", required=True)
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--scope", action="append", default=[])
    search_parser.add_argument("--include-sensitive", action="store_true")
    search_parser.add_argument("--json", action="store_true")
    add_dry_run(search_parser)
    return root


def emit(result: JsonValue) -> None:
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def main(arguments: Optional[Sequence[str]] = None) -> int:
    arguments_parser = parser()
    arguments_value = arguments_parser.parse_args(arguments)
    try:
        config = load_config(arguments_value.config)
        if arguments_value.command == "doctor":  # noqa: IF_VARIANT_OK - Python 3.9 has no match/case syntax
            emit(doctor(config, load_memory(config)))
        elif arguments_value.command == "explain":
            emit(explain(config, load_event(arguments_value.event)))
        else:
            emit(
                memory_search(
                    config,
                    load_memory(config),
                    arguments_value.query,
                    arguments_value.scope,
                    arguments_value.include_sensitive,
                )
            )
        return 0
    except DataError as error:
        command = "memory search" if arguments_value.command == "memory" else arguments_value.command
        emit(error_result(command, error))
        return 1


if __name__ == "__main__":
    sys.exit(main())
