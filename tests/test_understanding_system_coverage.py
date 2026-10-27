import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COVERAGE = ROOT / "skills" / "understanding-system" / "scripts" / "coverage.py"
SKILL = ROOT / "skills" / "understanding-system" / "SKILL.md"
FLOW = ROOT / "skills" / "understanding-system" / "references" / "flow.md"
STRUCTURE = ROOT / "skills" / "understanding-system" / "references" / "structure.md"
TABLE = ROOT / "skills" / "understanding-system" / "references" / "table.md"
ER = ROOT / "skills" / "understanding-system" / "references" / "er.md"
STATE = ROOT / "skills" / "understanding-system" / "references" / "state.md"


def run_coverage(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(COVERAGE), *args],
        check=False,
        capture_output=True,
        text=True,
    )


class CoverageScriptTests(unittest.TestCase):
    def test_missing_path_exits_2_and_complete_document_exits_0(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            kept = root / "internal" / "services" / "files.go"
            kept.parent.mkdir(parents=True)
            kept.write_text("package services\n", encoding="utf-8")
            other = root / "pkg" / "files.go"
            other.parent.mkdir()
            other.write_text("package pkg\n", encoding="utf-8")
            driver = root / "internal" / "test_driver.go"
            driver.write_text("package internal\n", encoding="utf-8")
            (root / "internal" / "test_helper.py").write_text("x\n", encoding="utf-8")
            (root / "node_modules" / "left-out").mkdir(parents=True)
            (root / "node_modules" / "left-out" / "index.js").write_text("x", encoding="utf-8")
            (root / "internal" / "services" / "files_test.go").write_text("package services\n", encoding="utf-8")
            (root / "internal" / "services" / "api.pb.go").write_text("package services\n", encoding="utf-8")

            listed = run_coverage("list", str(root))
            self.assertEqual(listed.returncode, 0, listed.stderr)
            self.assertEqual(
                listed.stdout.splitlines(),
                ["internal/services/files.go", "internal/test_driver.go", "pkg/files.go"],
            )

            document = root / "design.md"
            document.write_text("见 `internal/services/files.go`。\n", encoding="utf-8")
            missing_name = other.relative_to(root).as_posix()
            driver_name = driver.relative_to(root).as_posix()
            failed = run_coverage("check", str(root), str(document))
            self.assertEqual(failed.returncode, 2, failed.stdout)
            self.assertEqual(failed.stdout.splitlines()[0], "FAIL: missing 2 of 3")
            self.assertIn(missing_name, failed.stdout.splitlines())
            self.assertIn(driver_name, failed.stdout.splitlines())
            self.assertNotIn("internal/services/files.go", failed.stdout.splitlines()[1:])

            document.write_text(
                "见 `internal/services/files.go`。见 `internal/test_driver.go`。见 `pkg/files.go`。\n",
                encoding="utf-8",
            )
            passed = run_coverage("check", str(root), str(document))
            self.assertEqual(passed.returncode, 0, passed.stdout)
            self.assertEqual(passed.stdout.strip(), "PASS: cited 3 of 3")

    def test_sentence_period_cites_and_longer_suffix_does_not(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "cmd" / "main.go"
            source.parent.mkdir()
            source.write_text("package main\n", encoding="utf-8")
            document = root / "design.md"
            document.write_text("入口是 cmd/main.go.bak。\n", encoding="utf-8")
            failed = run_coverage("check", str(root), str(document))
            self.assertEqual(failed.returncode, 2, failed.stdout)
            document.write_text("入口是 cmd/main.go。\n", encoding="utf-8")
            passed = run_coverage("check", str(root), str(document))
            self.assertEqual(passed.returncode, 0, passed.stdout)
            self.assertEqual(passed.stdout.strip(), "PASS: cited 1 of 1")
            document.write_text("The entry is cmd/main.go.\n", encoding="utf-8")
            ascii_period = run_coverage("check", str(root), str(document))
            self.assertEqual(ascii_period.returncode, 0, ascii_period.stdout)

    def test_tool_error_exits_1(self):
        missing = run_coverage("list", "/no/such/understanding-system-repo")
        self.assertEqual(missing.returncode, 1)
        self.assertTrue(missing.stdout.startswith("ERROR:"))


class CoverageContractTests(unittest.TestCase):
    def test_skill_requires_the_checker_and_drops_the_unread_directory_stop(self):
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("scripts/coverage.py", skill)
        self.assertIn("PASS: cited", skill)
        self.assertIn("FAIL: missing", skill)
        self.assertNotIn("unread directory", skill)
        self.assertNotIn("directory that was not read", FLOW.read_text(encoding="utf-8"))
        self.assertNotIn("Do not write a code note for every directory", STRUCTURE.read_text(encoding="utf-8"))
        self.assertNotIn("Do not list tables the question did not name", TABLE.read_text(encoding="utf-8"))
        self.assertNotIn("only for another relationship the question names", ER.read_text(encoding="utf-8"))
        self.assertNotIn("Walk one normal path", STATE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
