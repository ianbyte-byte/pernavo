import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError


SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "sonarqube-review" / "scripts" / "sonarqube_review.py"
SPEC = importlib.util.spec_from_file_location("sonarqube_review", SCRIPT)
sonarqube_review = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(sonarqube_review)


class FakeResponse:
    def __init__(self, body):
        self.body = json.dumps(body).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self, _limit):
        return self.body


class SonarQubeReviewCase(unittest.TestCase):
    def run_cli(self, arguments):
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = sonarqube_review.main(arguments)
        return exit_code, json.loads(output.getvalue())


class TestPrerequisites(SonarQubeReviewCase):
    def test_missing_token_stops_before_network(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch.object(sonarqube_review, "urlopen") as mocked_open:
                exit_code, result = self.run_cli(["preflight", "--project-key", "sample", "--allow-network"])
        self.assertEqual(2, exit_code)
        self.assertEqual("missing_secret", result["error"]["code"])
        mocked_open.assert_not_called()

    def test_remote_url_requires_explicit_gate(self):
        with mock.patch.dict(os.environ, {"SONARQUBE_TOKEN": "secret"}, clear=True):
            exit_code, result = self.run_cli(
                ["preflight", "--url", "https://sonar.example.com", "--project-key", "sample", "--allow-network"]
            )
        self.assertEqual(2, exit_code)
        self.assertEqual("remote_url_gate", result["error"]["code"])


class TestReview(SonarQubeReviewCase):
    def test_project_key_is_read_from_properties_and_token_is_not_emitted(self):
        responses = [
            {"status": "UP"},
            {"component": {"key": "sample", "name": "Sample"}},
            {"projectStatus": {"status": "OK"}},
            {"component": {"key": "sample", "measures": [{"metric": "bugs", "value": "1"}]}},
            {"paging": {"total": 1}, "issues": [{"severity": "MAJOR", "message": "Fix this"}]},
            {"analyses": [{"revision": "abc123", "date": "2026-08-07T00:00:00+0000"}]},
        ]

        def fake_open(request, timeout):
            self.assertEqual(10, timeout)
            self.assertTrue(request.get_header("Authorization").startswith("Basic "))
            return FakeResponse(responses.pop(0))

        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "sonar-project.properties").write_text("sonar.projectKey=sample\n", encoding="utf-8")
            with mock.patch.dict(os.environ, {"SONARQUBE_TOKEN": "top-secret-token"}, clear=True):
                with mock.patch.object(sonarqube_review, "urlopen", side_effect=fake_open):
                    exit_code, result = self.run_cli(["review", "--workspace", directory, "--allow-network"])
        self.assertEqual(0, exit_code)
        self.assertEqual("sample", result["target"]["project_key"])
        self.assertEqual("OK", result["quality_gate"]["status"])
        self.assertEqual(1, result["issues"]["counts"]["major"])
        self.assertEqual("abc123", result["analysis"][0]["revision"])
        self.assertFalse(result["partial"])
        self.assertNotIn("top-secret-token", json.dumps(result))

    def test_missing_key_uses_one_bounded_exact_name_search(self):
        responses = [
            {"status": "UP"},
            {"components": [{"key": "sample-key", "name": "sample"}]},
        ]

        def fake_open(request, timeout):
            self.assertEqual(10, timeout)
            if len(responses) == 1:
                self.assertIn("/api/components/search?", request.full_url)
                self.assertIn("q=sample", request.full_url)
            return FakeResponse(responses.pop(0))

        with tempfile.TemporaryDirectory() as parent:
            workspace = Path(parent, "sample")
            workspace.mkdir()
            with mock.patch.dict(os.environ, {"SONARQUBE_TOKEN": "secret"}, clear=True):
                with mock.patch.object(sonarqube_review, "urlopen", side_effect=fake_open):
                    exit_code, result = self.run_cli(["preflight", "--workspace", str(workspace), "--allow-network"])
        self.assertEqual(0, exit_code)
        self.assertEqual("sample-key", result["target"]["project_key"])
        self.assertEqual("project-resolved", result["evidence_state"])

    def test_endpoint_failure_preserves_other_review_evidence(self):
        responses = {
            "/api/system/status": {"status": "UP"},
            "/api/components/show": {"component": {"key": "sample", "name": "Sample"}},
            "/api/qualitygates/project_status": {"projectStatus": {"status": "ERROR"}},
            "/api/issues/search": {"paging": {"total": 0}, "issues": []},
            "/api/project_analyses/search": {"analyses": []},
        }

        def fake_open(request, timeout):
            self.assertEqual(10, timeout)
            if "/api/measures/component" in request.full_url:
                raise HTTPError(request.full_url, 500, "Server Error", None, None)
            endpoint = next(key for key in responses if key in request.full_url)
            return FakeResponse(responses[endpoint])

        with mock.patch.dict(os.environ, {"SONARQUBE_TOKEN": "secret"}, clear=True):
            with mock.patch.object(sonarqube_review, "urlopen", side_effect=fake_open):
                exit_code, result = self.run_cli(
                    ["review", "--project-key", "sample", "--allow-network"]
                )
        self.assertEqual(0, exit_code)
        self.assertTrue(result["partial"])
        self.assertEqual("ERROR", result["quality_gate"]["status"])
        self.assertIsNone(result["measures"])
        self.assertEqual("/api/measures/component", result["errors"][0]["endpoint"])


if __name__ == "__main__":
    unittest.main()
