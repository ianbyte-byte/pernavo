import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "codebase-slimming"
    / "scripts"
    / "quality_evidence.py"
)
SPEC = importlib.util.spec_from_file_location("quality_evidence", SCRIPT)
quality_evidence = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(quality_evidence)


class QualityEvidenceCase(unittest.TestCase):
    def run_cli(self, arguments):
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = quality_evidence.main(arguments)
        return exit_code, json.loads(output.getvalue())

    def make_executable(self, root, name, body):
        path = root / name
        path.write_text("#!/usr/bin/env python3\n" + body, encoding="utf-8")
        path.chmod(0o755)
        return path


class TestInventory(QualityEvidenceCase):
    def test_inventory_reports_signals_without_claiming_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "package.json").write_text("{}\n", encoding="utf-8")
            local_knip = target / "node_modules" / ".bin"
            local_knip.mkdir(parents=True)
            knip = self.make_executable(local_knip, "knip", "")
            with mock.patch.object(quality_evidence.shutil, "which", return_value=None):
                exit_code, result = self.run_cli(["inventory", "--target", str(target), "--json"])
        self.assertEqual(0, exit_code)
        self.assertTrue(result["signals"]["javascript_typescript"])
        tools = {item["name"]: item for item in result["tools"]}
        self.assertEqual(str(knip.resolve()), tools["knip"]["executable"])
        self.assertEqual("available", tools["knip"]["state"])
        self.assertIn("no analyzer was executed", result["proof_boundary"])

    def test_inventory_rejects_a_missing_target_with_stable_json(self):
        exit_code, result = self.run_cli(["inventory", "--target", "/definitely/absent/pernavo"])
        self.assertEqual(2, exit_code)
        self.assertFalse(result["valid"])
        self.assertEqual("invalid_target", result["error"]["code"])


class TestRun(QualityEvidenceCase):
    def test_dry_run_plans_commands_without_creating_evidence_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "main.py").write_text("print('ok')\n", encoding="utf-8")
            scc = self.make_executable(root, "scc", "")
            evidence = root / "evidence"
            with mock.patch.object(quality_evidence.shutil, "which", side_effect=lambda name: str(scc) if name == "scc" else None):
                exit_code, result = self.run_cli(
                    [
                        "run",
                        "--target",
                        str(target),
                        "--evidence-dir",
                        str(evidence),
                        "--tool",
                        "scc",
                        "--dry-run",
                    ]
                )
        self.assertEqual(0, exit_code)
        self.assertTrue(result["dry_run"])
        self.assertFalse(evidence.exists())

    def test_run_captures_hashes_and_normalized_scc_metrics(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "main.py").write_text("print('ok')\n", encoding="utf-8")
            body = "import json\nprint(json.dumps([{'Files': 2, 'Lines': 10, 'Code': 7, 'Comment': 1, 'Blank': 2, 'Complexity': 3}]))\n"
            scc = self.make_executable(root, "scc", body)
            evidence = root / "evidence"
            with mock.patch.object(quality_evidence.shutil, "which", side_effect=lambda name: str(scc) if name == "scc" else None):
                exit_code, result = self.run_cli(
                    ["run", "--target", str(target), "--evidence-dir", str(evidence), "--tool", "scc"]
                )
            manifest = json.loads((evidence / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(0, exit_code)
        self.assertEqual(7.0, result["tools"][0]["metrics"]["code"])
        self.assertEqual(3.0, manifest["tools"][0]["metrics"]["complexity"])
        self.assertEqual(64, len(result["tools"][0]["stdout"]["sha256"]))
        self.assertEqual([str(scc), "--version"], result["tools"][0]["version_probe"]["command"])

    def test_run_requires_explicit_sonarqube_side_effect_gates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "sonar-project.properties").write_text("sonar.projectKey=x\n", encoding="utf-8")
            scanner = self.make_executable(root, "sonar-scanner", "")
            with mock.patch.object(
                quality_evidence.shutil, "which", side_effect=lambda name: str(scanner) if name == "sonar-scanner" else None
            ):
                exit_code, result = self.run_cli(
                    ["run", "--target", str(target), "--evidence-dir", str(root / "evidence"), "--tool", "sonarqube"]
                )
        self.assertEqual(2, exit_code)
        self.assertEqual("network_gate", result["error"]["code"])

    def test_coverlet_uses_mtp_command_only_when_the_project_declares_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "Tests.csproj").write_text(
                '<Project Sdk="Microsoft.NET.Sdk"><ItemGroup><PackageReference Include="coverlet.MTP" /></ItemGroup></Project>\n',
                encoding="utf-8",
            )
            dotnet = self.make_executable(root, "dotnet", "import sys\nprint('10.0.100')\n")
            evidence = root / "evidence"
            with mock.patch.object(
                quality_evidence.shutil, "which", side_effect=lambda name: str(dotnet) if name == "dotnet" else None
            ):
                exit_code, result = self.run_cli(
                    [
                        "run",
                        "--target",
                        str(target),
                        "--evidence-dir",
                        str(evidence),
                        "--tool",
                        "coverlet",
                        "--allow-worktree-writes",
                        "--dry-run",
                    ]
                )
        self.assertEqual(0, exit_code)
        self.assertIn("--coverlet", result["tools"][0]["command"])
        self.assertNotIn("XPlat Code Coverage", result["tools"][0]["command"])

    def test_dotnet_and_roslyn_analyzer_dry_run_use_non_mutating_source_modes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "App.csproj").write_text('<Project Sdk="Microsoft.NET.Sdk" />\n', encoding="utf-8")
            dotnet = self.make_executable(root, "dotnet", "print('10.0.100')\n")
            with mock.patch.object(
                quality_evidence.shutil, "which", side_effect=lambda name: str(dotnet) if name == "dotnet" else None
            ):
                exit_code, result = self.run_cli(
                    [
                        "run",
                        "--target",
                        str(target),
                        "--evidence-dir",
                        str(root / "evidence"),
                        "--tool",
                        "dotnet-analyzers",
                        "--tool",
                        "roslyn-analyzers",
                        "--allow-worktree-writes",
                        "--dry-run",
                    ]
                )
        self.assertEqual(0, exit_code)
        commands = {item["name"]: item["command"] for item in result["tools"]}
        self.assertIn("-p:RunAnalyzers=true", commands["dotnet-analyzers"])
        self.assertIn("-p:EnableNETAnalyzers=true", commands["dotnet-analyzers"])
        self.assertIn("--verify-no-changes", commands["roslyn-analyzers"])
        self.assertIn("--no-restore", commands["roslyn-analyzers"])

    def test_dotnet_analyzer_run_normalizes_build_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "App.csproj").write_text('<Project Sdk="Microsoft.NET.Sdk" />\n', encoding="utf-8")
            body = "import sys\nprint('10.0.100' if '--version' in sys.argv else 'Program.cs(1,1): warning CA1822: Mark members as static')\n"
            dotnet = self.make_executable(root, "dotnet", body)
            with mock.patch.object(
                quality_evidence.shutil, "which", side_effect=lambda name: str(dotnet) if name == "dotnet" else None
            ):
                exit_code, result = self.run_cli(
                    [
                        "run",
                        "--target",
                        str(target),
                        "--evidence-dir",
                        str(root / "evidence"),
                        "--tool",
                        "dotnet-analyzers",
                        "--allow-worktree-writes",
                    ]
                )
        self.assertEqual(0, exit_code)
        self.assertEqual(1.0, result["tools"][0]["metrics"]["diagnostics_total"])
        self.assertEqual(1.0, result["tools"][0]["metrics"]["diagnostic_CA1822"])

    def test_roslyn_analyzer_run_hashes_report_and_normalizes_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "App.csproj").write_text('<Project Sdk="Microsoft.NET.Sdk" />\n', encoding="utf-8")
            body = (
                "import json, pathlib, sys\n"
                "if '--report' in sys.argv:\n"
                "    report = pathlib.Path(sys.argv[sys.argv.index('--report') + 1])\n"
                "    report.mkdir(parents=True)\n"
                "    (report / 'format-report.json').write_text(json.dumps([{'FilePath':'Program.cs','FileChanges':[{'DiagnosticId':'CA1822'}]}]))\n"
                "else:\n"
                "    print('10.0.100')\n"
            )
            dotnet = self.make_executable(root, "dotnet", body)
            with mock.patch.object(
                quality_evidence.shutil, "which", side_effect=lambda name: str(dotnet) if name == "dotnet" else None
            ):
                exit_code, result = self.run_cli(
                    [
                        "run",
                        "--target",
                        str(target),
                        "--evidence-dir",
                        str(root / "evidence"),
                        "--tool",
                        "roslyn-analyzers",
                        "--allow-worktree-writes",
                    ]
                )
        self.assertEqual(0, exit_code)
        tool = result["tools"][0]
        self.assertEqual(1.0, tool["metrics"]["diagnostic_CA1822"])
        self.assertEqual("roslyn-analyzers/format-report.json", tool["artifacts"][0]["relative_path"])
        self.assertEqual(64, len(tool["artifacts"][0]["sha256"]))

    def test_run_refuses_to_overwrite_existing_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "main.py").write_text("pass\n", encoding="utf-8")
            evidence = root / "evidence"
            evidence.mkdir()
            (evidence / "keep.txt").write_text("user evidence\n", encoding="utf-8")
            scc = self.make_executable(root, "scc", "")
            with mock.patch.object(quality_evidence.shutil, "which", side_effect=lambda name: str(scc) if name == "scc" else None):
                exit_code, result = self.run_cli(
                    ["run", "--target", str(target), "--evidence-dir", str(evidence), "--tool", "scc"]
                )
        self.assertEqual(2, exit_code)
        self.assertEqual("output_not_empty", result["error"]["code"])


class TestCompare(QualityEvidenceCase):
    def test_compare_reports_numeric_delta_without_interpreting_direction(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifests = []
            for name, code in (("before", 100), ("after", 70)):
                path = root / (name + ".json")
                path.write_text(
                    json.dumps(
                        {
                            "schema_version": 1,
                            "command": "run",
                            "target": str(root / "target"),
                            "tools": [{"name": "scc", "metrics": {"code": code}}],
                        }
                    ),
                    encoding="utf-8",
                )
                manifests.append(path)
            exit_code, result = self.run_cli(
                ["compare", "--before", str(manifests[0]), "--after", str(manifests[1]), "--json"]
            )
        self.assertEqual(0, exit_code)
        self.assertEqual(-30.0, result["tools"][0]["metrics"][0]["delta"])
        self.assertIn("engineering review", result["proof_boundary"])


if __name__ == "__main__":
    unittest.main()
