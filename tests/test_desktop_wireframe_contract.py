import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "desktop-wireframe" / "SKILL.md"
SHELL = ROOT / "skills" / "desktop-wireframe" / "assets" / "shell.html"
CHECK = ROOT / "skills" / "desktop-wireframe" / "scripts" / "check_wireframe.py"
CLAUDE = ROOT / "CLAUDE.md"


def run_check(html: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "sheet.html"
        path.write_text(html, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(CHECK), str(path)],
            capture_output=True,
            text=True,
            check=False,
        )


class DesktopWireframeContractTests(unittest.TestCase):
    def test_triggers_and_boundaries(self):
        contract = SKILL.read_text(encoding="utf-8")
        claude = CLAUDE.read_text(encoding="utf-8")

        self.assertIn("桌面端线框原型", contract)
        self.assertIn("窗口布局", contract)
        self.assertIn("常用组件", contract)
        self.assertIn("`frontend-wireframe`", contract)
        self.assertIn("`engineering-workflow`", contract)
        self.assertIn("[assets/shell.html](assets/shell.html)", contract)
        self.assertIn("[scripts/check_wireframe.py](scripts/check_wireframe.py)", contract)
        self.assertIn("invoke `desktop-wireframe`", claude)

    def test_shell_passes(self):
        result = run_check(SHELL.read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: kit and screens", result.stdout)
        self.assertNotIn("http://", SHELL.read_text(encoding="utf-8"))
        self.assertNotIn("https://", SHELL.read_text(encoding="utf-8"))

    def test_missing_kit_part_fails(self):
        html = SHELL.read_text(encoding="utf-8").replace('data-part="media"', 'data-part="removed"', 1)
        result = run_check(html)

        self.assertEqual(result.returncode, 2)
        self.assertIn('FAIL: missing kit data-part="media"', result.stdout)

    def test_screen_part_outside_the_kit_fails(self):
        html = SHELL.read_text(encoding="utf-8").replace(
            'data-screen="orders"',
            'data-screen="orders" data-part="sparkline"',
            1,
        )
        result = run_check(html)

        self.assertEqual(result.returncode, 2)
        self.assertIn('FAIL: screen uses data-part="sparkline" that is not in the kit', result.stdout)

    def test_external_ref_fails(self):
        html = SHELL.read_text(encoding="utf-8").replace(
            "<title>",
            '<link rel="stylesheet" href="https://example.com/kit.css"><title>',
            1,
        )
        result = run_check(html)

        self.assertEqual(result.returncode, 2)
        self.assertIn("FAIL: external ref https://example.com/kit.css", result.stdout)
