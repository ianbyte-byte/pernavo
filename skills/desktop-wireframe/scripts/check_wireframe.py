#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_COLUMNS = frozenset({"layout", "buttons", "components"})
REQUIRED_KIT_PARTS = frozenset(
    {
        "window",
        "status-bar",
        "button-primary",
        "button-secondary",
        "checkbox",
        "radio",
        "tag",
        "field",
        "toggle",
        "icon-button",
        "menu",
        "card",
        "search",
        "media",
        "transport",
        "tabs",
        "tree",
        "toolbar",
    }
)
EXTERNAL_ATTR = re.compile(
    r"""(?:href|src)\s*=\s*['"]\s*((?:https?:)?//[^'"]+)['"]""",
    re.IGNORECASE,
)
EXTERNAL_CSS = re.compile(r"""url\(\s*['"]?(?:https?:)?//""", re.IGNORECASE)


class SheetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str | None] = []
        self.boards: set[str] = set()
        self.columns: set[str] = set()
        self.kit_parts: set[str] = set()
        self.screen_parts: set[str] = set()
        self.screens = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        parent = next((board for board in reversed(self.stack) if board), None)
        board = attr.get("data-board") or parent
        self.stack.append(board)
        if attr.get("data-board"):
            self.boards.add(attr["data-board"])
        column = attr.get("data-column")
        if board == "kit" and column:
            self.columns.add(column)
        part = attr.get("data-part")
        if board == "kit" and part:
            self.kit_parts.add(part)
        if board == "screens" and part:
            self.screen_parts.add(part)
        if board == "screens" and attr.get("data-screen"):
            self.screens += 1

    def handle_endtag(self, tag: str) -> None:
        if self.stack:
            self.stack.pop()


def check(text: str) -> list[str]:
    parser = SheetParser()
    parser.feed(text)
    parser.close()
    problems: list[str] = []
    if "kit" not in parser.boards:
        problems.append('missing data-board="kit"')
    if "screens" not in parser.boards:
        problems.append('missing data-board="screens"')
    for column in sorted(REQUIRED_COLUMNS - parser.columns):
        problems.append(f'missing data-column="{column}"')
    for part in sorted(REQUIRED_KIT_PARTS - parser.kit_parts):
        problems.append(f'missing kit data-part="{part}"')
    for part in sorted(parser.screen_parts - parser.kit_parts):
        problems.append(f'screen uses data-part="{part}" that is not in the kit')
    if parser.screens < 1:
        problems.append("screens board has no data-screen")
    for match in EXTERNAL_ATTR.finditer(text):
        problems.append(f"external ref {match.group(1)}")
    if EXTERNAL_CSS.search(text):
        problems.append("external css url")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_wireframe.py <file.html>", file=sys.stderr)
        return 1
    path = Path(argv[1])
    if not path.is_file():
        print(f"missing file: {path}", file=sys.stderr)
        return 1
    problems = check(path.read_text(encoding="utf-8"))
    if problems:
        for item in problems:
            print(f"FAIL: {item}")
        return 2
    print("PASS: kit and screens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
