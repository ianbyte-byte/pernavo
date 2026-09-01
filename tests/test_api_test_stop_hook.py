import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "skills" / "test-engineering" / "scripts" / "api_test_stop_hook.py"
EXAMPLES = ROOT / "skills" / "test-engineering" / "examples" / "api-test-gate"


def run_hook(payload, cwd, extra_env=None):
    env = {**os.environ, "PERNAVO_API_TEST_CWD": str(cwd)}
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(cwd),
        env=env,
        check=False,
    )


class ApiTestStopHookTests(unittest.TestCase):
    def test_ordinary_stop_without_api_claim_is_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_hook(
                {
                    "hook_event_name": "Stop",
                    "cwd": directory,
                    "last_assistant_message": "Renamed the helper file.",
                },
                directory,
            )
            self.assertEqual(0, result.returncode)
            self.assertEqual({"continue": True, "suppressOutput": True}, json.loads(result.stdout))

    def test_done_claim_with_jsonl_and_no_matrix_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_hook(
                {
                    "hook_event_name": "Stop",
                    "cwd": directory,
                    "last_assistant_message": "接口测试完成，jsonl 已写入。",
                },
                directory,
            )
            self.assertEqual(2, result.returncode)
            payload = json.loads(result.stdout)
            self.assertEqual("block", payload["decision"])
            self.assertIn("api-test-matrix.json", payload["reason"])

    def test_leftover_matrix_does_not_block_ordinary_stop(self):
        example = EXAMPLES / "czlhc-negative"
        result = run_hook(
            {
                "hook_event_name": "Stop",
                "cwd": str(example),
                "last_assistant_message": "Renamed the helper file.",
            },
            example,
        )
        self.assertEqual(0, result.returncode)

    def test_done_claim_with_failing_matrix_is_blocked(self):
        example = EXAMPLES / "czlhc-negative"
        result = run_hook(
            {
                "hook_event_name": "Stop",
                "cwd": str(example),
                "last_assistant_message": "测试完成，可以上线。",
            },
            example,
        )
        self.assertEqual(2, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("block", payload["decision"])
        self.assertIn("create-valid", payload["reason"])

    def test_passing_matrix_allows_stop(self):
        example = EXAMPLES / "setposition-pass"
        result = run_hook(
            {
                "hook_event_name": "Stop",
                "cwd": str(example),
                "last_assistant_message": "测试完成",
            },
            example,
        )
        self.assertEqual(0, result.returncode)


if __name__ == "__main__":
    unittest.main()
