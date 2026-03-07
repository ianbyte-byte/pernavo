from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectCheck:
    root: Path
    required_paths: tuple[Path, ...]
    missing: tuple[Path, ...]

    @property
    def ok(self) -> bool:
        return len(self.missing) == 0


def check_project_layout(root: Path) -> ProjectCheck:
    root = root.resolve()
    required = (
        root / "CLAUDE.md",
        root / ".claude" / "docs" / "claud_platform_menu.md",
        root / ".claude" / "session_config.json",
        root / ".claude" / "settings.json",
        root / ".claude" / "hooks" / "lcc-quality-gate.sh",
        root / ".claude" / "agents",
        root / ".claude" / "skills",
    )
    missing = tuple(p for p in required if not p.exists())
    return ProjectCheck(root=root, required_paths=required, missing=missing)
