import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "change-review"
    / "scripts"
    / "sonarqube_local.py"
)
SPEC = importlib.util.spec_from_file_location("sonarqube_local", SCRIPT)
sonarqube_local = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(sonarqube_local)


class FakeResponse:
    def __init__(self, body, content_type="application/json"):
        self.status = 200
        self.body = body
        self.headers = {"Content-Type": content_type}

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self, _limit):
        return self.body


class SonarQubeLocalCase(unittest.TestCase):
    def run_cli(self, arguments):
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = sonarqube_local.main(arguments)
        return exit_code, json.loads(output.getvalue())


class TestMcpConfig(SonarQubeLocalCase):
    def test_codex_config_rewrites_localhost_mounts_read_only_and_never_persists_token(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            with mock.patch.dict(os.environ, {"SONARQUBE_TOKEN": "top-secret-token"}, clear=False):
                exit_code, result = self.run_cli(
                    [
                        "mcp-config",
                        "--client",
                        "codex",
                        "--workspace",
                        str(workspace),
                        "--project-key",
                        "sample-project",
                        "--image",
                        "sonarsource/sonarqube-mcp:1.23.0",
                    ]
                )
        serialized = json.dumps(result)
        self.assertEqual(0, exit_code)
        self.assertNotIn("top-secret-token", serialized)
        self.assertIn("host.docker.internal:9000", result["configuration"])
        self.assertIn(str(workspace.resolve()) + ":/app/mcp-workspace:ro", result["configuration"])
        self.assertIn('"SONARQUBE_READ_ONLY" = "true"', result["configuration"])
        self.assertTrue(result["authentication"]["present"])
        self.assertFalse(result["authentication"]["persisted_in_config"])

    def test_json_config_is_a_plan_and_reports_missing_runtime_and_unpinned_image(self):
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.object(sonarqube_local.shutil, "which", return_value=None):
                exit_code, result = self.run_cli(
                    ["mcp-config", "--client", "json", "--workspace", directory]
                )
        self.assertEqual(0, exit_code)
        self.assertIsNone(result["runtime"]["executable"])
        self.assertIn("container image is not version-pinned", result["warnings"])
        self.assertIn("not executed", result["proof_boundary"])

    def test_remote_server_requires_explicit_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            exit_code, result = self.run_cli(
                ["mcp-config", "--workspace", directory, "--url", "https://sonar.example.com"]
            )
        self.assertEqual(2, exit_code)
        self.assertEqual("remote_url_gate", result["error"]["code"])


class TestProbe(SonarQubeLocalCase):
    def test_probe_requires_network_gate(self):
        exit_code, result = self.run_cli(["probe"])
        self.assertEqual(2, exit_code)
        self.assertEqual("network_gate", result["error"]["code"])

    def test_probe_reports_status_without_exposing_token(self):
        responses = [
            FakeResponse(b'{"id":"server-1","status":"UP"}'),
            FakeResponse(b"2026.1", "text/plain"),
        ]

        def fake_open(request, timeout):
            self.assertEqual(5, timeout)
            self.assertTrue(request.get_header("Authorization").startswith("Basic "))
            return responses.pop(0)

        with mock.patch.dict(os.environ, {"SONARQUBE_TOKEN": "top-secret-token"}, clear=False):
            with mock.patch.object(sonarqube_local, "urlopen", side_effect=fake_open):
                exit_code, result = self.run_cli(["probe", "--allow-network", "--timeout", "5"])
        self.assertEqual(0, exit_code)
        self.assertEqual("UP", result["service"]["status"])
        self.assertEqual("2026.1", result["service"]["version"])
        self.assertNotIn("top-secret-token", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
