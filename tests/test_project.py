from __future__ import annotations

from pathlib import Path

from chung_agent_swarm.project import check_project_layout


def test_check_project_layout_ok(tmp_path: Path) -> None:
    (tmp_path / "CLAUDE.md").write_text("x", encoding="utf-8")
    (tmp_path / ".claude" / "docs").mkdir(parents=True)
    (tmp_path / ".claude" / "docs" / "claud_platform_menu.md").write_text("x", encoding="utf-8")
    (tmp_path / ".claude" / "agents").mkdir(parents=True)
    (tmp_path / ".claude" / "skills").mkdir(parents=True)
    (tmp_path / ".claude" / "session_config.json").write_text("{}", encoding="utf-8")
    (tmp_path / ".claude" / "settings.json").write_text("{}", encoding="utf-8")
    (tmp_path / ".claude" / "hooks").mkdir(parents=True)
    (tmp_path / ".claude" / "hooks" / "lcc-quality-gate.sh").write_text("x", encoding="utf-8")

    result = check_project_layout(tmp_path)
    assert result.ok
