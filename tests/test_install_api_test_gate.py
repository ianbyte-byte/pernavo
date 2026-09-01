import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "skills" / "test-engineering" / "scripts" / "install_api_test_gate.py"
HOOK = ROOT / "skills" / "test-engineering" / "scripts" / "api_test_stop_hook.py"


def run_installer(args):
    return subprocess.run(
        [sys.executable, str(INSTALLER), *args],
        text=True,
        capture_output=True,
        check=False,
    )


class InstallApiTestGateTests(unittest.TestCase):
    def test_default_is_check_and_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            claude = root / "claude" / "settings.json"
            claude.parent.mkdir()
            original = {
                "env": {"KEEP": "1"},
                "hooks": {
                    "Stop": [
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": "python3 /tmp/mem0-on-stop.sh",
                                    "timeout": 10,
                                }
                            ]
                        }
                    ]
                },
            }
            claude.write_text(json.dumps(original), encoding="utf-8")
            before = claude.read_text(encoding="utf-8")
            result = run_installer(
                [
                    "--script",
                    str(HOOK),
                    "--claude-settings",
                    str(claude),
                    "--codex-hooks",
                    str(root / "missing-parent" / "hooks.json"),
                ]
            )
            report = json.loads(result.stdout)
            self.assertEqual("check", report["mode"])
            self.assertEqual("missing", report["hosts"]["claude"]["status"])
            self.assertEqual("blocked-parent", report["hosts"]["codex"]["status"])
            self.assertEqual(before, claude.read_text(encoding="utf-8"))
            self.assertFalse((root / "missing-parent").exists())
            self.assertNotEqual(0, result.returncode)

    def test_apply_merges_without_dropping_existing_hooks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            claude = root / "claude" / "settings.json"
            codex = root / "codex" / "hooks.json"
            claude.parent.mkdir()
            codex.parent.mkdir()
            claude.write_text(
                json.dumps(
                    {
                        "includeCoAuthoredBy": False,
                        "hooks": {
                            "Stop": [
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": "python3 /tmp/skill-usage-hook.py",
                                            "timeout": 10,
                                        }
                                    ]
                                }
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            first = run_installer(
                [
                    "--apply",
                    "--script",
                    str(HOOK),
                    "--claude-settings",
                    str(claude),
                    "--codex-hooks",
                    str(codex),
                ]
            )
            self.assertEqual(0, first.returncode, first.stderr)
            claude_data = json.loads(claude.read_text(encoding="utf-8"))
            self.assertFalse(claude_data["includeCoAuthoredBy"])
            stop = claude_data["hooks"]["Stop"]
            self.assertEqual(2, len(stop))
            self.assertIn("skill-usage-hook.py", json.dumps(stop[0]))
            self.assertIn("api_test_stop_hook.py", json.dumps(stop[1]))
            self.assertIn("TaskCompleted", claude_data["hooks"])
            second = run_installer(
                [
                    "--apply",
                    "--script",
                    str(HOOK),
                    "--claude-settings",
                    str(claude),
                    "--codex-hooks",
                    str(codex),
                ]
            )
            self.assertEqual("skipped-identical", json.loads(second.stdout)["hosts"]["claude"]["status"])
            self.assertEqual(2, len(json.loads(claude.read_text(encoding="utf-8"))["hooks"]["Stop"]))
            mode = stat.S_IMODE(os.stat(codex).st_mode)
            self.assertEqual(0o600, mode)


if __name__ == "__main__":
    unittest.main()
