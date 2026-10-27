#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

SKIP_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        "node_modules",
        "vendor",
        "dist",
        "build",
        "out",
        "coverage",
        "target",
        ".venv",
        "venv",
        "__pycache__",
        ".pernavo",
        "third_party",
        "external",
        "testdata",
        "fixtures",
        "mocks",
        "__tests__",
    }
)

SUFFIXES = frozenset(
    {
        ".c",
        ".cc",
        ".clj",
        ".cpp",
        ".cs",
        ".cshtml",
        ".dart",
        ".ex",
        ".exs",
        ".go",
        ".gql",
        ".graphql",
        ".h",
        ".hpp",
        ".java",
        ".js",
        ".jsx",
        ".kt",
        ".mjs",
        ".php",
        ".prisma",
        ".proto",
        ".py",
        ".pyi",
        ".razor",
        ".rb",
        ".rs",
        ".scala",
        ".sql",
        ".swift",
        ".ts",
        ".tsx",
        ".vue",
    }
)


def inventory(root: Path) -> list[str]:
    found: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if keep_dir(name)]
        for name in filenames:
            path = Path(dirpath) / name
            if path.suffix.lower() not in SUFFIXES:
                continue
            relative = path.relative_to(root).as_posix()
            if is_test(relative) or is_generated(relative):
                continue
            found.append(relative)
    found.sort()
    return found


def keep_dir(name: str) -> bool:
    return name not in SKIP_DIRS and not name.startswith(".")


def is_test(relative: str) -> bool:
    path = Path(relative)
    name = path.name
    if name.endswith("_test.go") or name.endswith("_test.py"):
        return True
    if name.startswith("test_") and name.endswith(".py"):
        return True
    if ".test." in name or ".spec." in name:
        return True
    return bool(set(path.parts) & {"test", "tests", "__tests__"})


def is_generated(relative: str) -> bool:
    name = Path(relative).name
    markers = (
        ".pb.go",
        ".pb.cc",
        "_generated.go",
        ".generated.ts",
        ".min.js",
    )
    return name.endswith(markers)


def cited(text: str, path: str) -> bool:
    start = 0
    while True:
        index = text.find(path, start)
        if index < 0:
            return False
        if not extends_path(text, index - 1) and not extends_path(text, index + len(path)):
            return True
        start = index + 1


def extends_path(text: str, index: int) -> bool:
    if index < 0 or index >= len(text):
        return False
    char = text[index]
    if char.isalnum() or char in {"_", "-", "/"}:
        return True
    if char != ".":
        return False
    next_index = index + 1
    if next_index >= len(text):
        return False
    next_char = text[next_index]
    return next_char.isalnum() or next_char == "_"


def list_command(root: Path) -> int:
    for path in inventory(root):
        print(path)
    return 0


def check_command(root: Path, document: Path) -> int:
    if not document.is_file():
        print("ERROR: document is not a file")
        return 1
    try:
        text = document.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: {exc}")
        return 1
    except UnicodeError as exc:
        print(f"ERROR: {exc}")
        return 1
    paths = inventory(root)
    missing = [path for path in paths if not cited(text, path)]
    total = len(paths)
    if missing:
        print(f"FAIL: missing {len(missing)} of {total}")
        for path in missing:
            print(path)
        return 2
    print(f"PASS: cited {total} of {total}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="coverage.py")
    commands = parser.add_subparsers(dest="command", required=True)
    list_parser = commands.add_parser("list")
    list_parser.add_argument("repository")
    check_parser = commands.add_parser("check")
    check_parser.add_argument("repository")
    check_parser.add_argument("document")
    args = parser.parse_args(argv)
    root = Path(args.repository)
    if not root.is_dir():
        print("ERROR: repository is not a directory")
        return 1
    if args.command == "list":
        return list_command(root)
    return check_command(root, Path(args.document))


if __name__ == "__main__":
    sys.exit(main())
