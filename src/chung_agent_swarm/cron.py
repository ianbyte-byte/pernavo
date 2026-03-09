from __future__ import annotations

import argparse
import subprocess
import sys
import re
import os
import shlex

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="lcc-claude-cron")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Create a recurring task.")
    create.add_argument("--prompt", required=True, help="The prompt to run.")
    create.add_argument("--cron", required=True, help="The cron schedule expression.")
    create.add_argument("--recurring", action="store_true", help="Whether the task is recurring.")

    subparsers.add_parser("list", help="List all recurring tasks.")

    delete = subparsers.add_parser("delete", help="Delete a task by pattern.")
    delete.add_argument("pattern", help="Regex pattern to match the prompt or command.")

    args = parser.parse_args(argv)

    try:
        if args.command == "create":
            return create_task(args.prompt, args.cron)
        elif args.command == "list":
            return list_tasks()
        elif args.command == "delete":
            return delete_task(args.pattern)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0

def get_crontab() -> list[str]:
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        if e.returncode == 1: # Usually means no crontab for user
            return []
        raise

def set_crontab(lines: list[str]):
    content = "\n".join(lines) + "\n"
    subprocess.run(["crontab", "-"], input=content, text=True, check=True)

def create_task(prompt: str, cron_expr: str) -> int:
    sanitized_prompt = prompt.replace("\n", " ").replace("\r", " ").strip()

    claude_bin = None
    for name in ["claude-code", "claude"]:
        path = subprocess.run(["which", name], capture_output=True, text=True).stdout.strip()
        if path:
            claude_bin = path
            break

    if not claude_bin:
        claude_bin = "claude"

    # We only preserve PATH and essential CLAUDE_ vars to avoid line length limits
    env_vars = []
    interesting_prefixes = ("CLAUDE_", "ANTHROPIC_", "PATH")
    for k, v in os.environ.items():
        if k.startswith(interesting_prefixes):
            env_vars.append(f"{k}={shlex.quote(v)}")

    env_str = " ".join(env_vars)
    quoted_prompt = shlex.quote(sanitized_prompt)
    full_cmd = f"{env_str} {claude_bin} -p {quoted_prompt}"

    lines = get_crontab()
    new_line = f"{cron_expr} {full_cmd} # LCC-CRON: {sanitized_prompt}"
    lines.append(new_line)

    set_crontab(lines)
    print(f"Task created: {sanitized_prompt} with schedule {cron_expr}")
    return 0

def list_tasks() -> int:
    lines = get_crontab()
    found = False
    for line in lines:
        if "# LCC-CRON:" in line:
            print(line)
            found = True

    if not found:
        print("No recurring tasks found.")
    return 0

def delete_task(pattern: str) -> int:
    lines = get_crontab()
    new_lines = []
    deleted_count = 0

    regex = re.compile(pattern)

    for line in lines:
        if "# LCC-CRON:" in line:
            if regex.search(line):
                deleted_count += 1
                continue
        new_lines.append(line)

    if deleted_count > 0:
        set_crontab(new_lines)
        print(f"Deleted {deleted_count} task(s) matching '{pattern}'.")
    else:
        print(f"No tasks found matching '{pattern}'.")

    return 0
