import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "pernavo-runtime-hook.py"
SPEC = importlib.util.spec_from_file_location("pernavo_runtime_hook", SCRIPT)
hook = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(hook)


class PernavoRuntimeHookTests(unittest.TestCase):
    def test_skill_read_omits_payload_secrets(self):
        event = hook.build_event(
            {
                "hook_event_name": "PostToolUse",
                "session_id": "s-1",
                "tool_name": "Read",
                "tool_input": {"file_path": "/Users/test/.agents/skills/test-engineering/SKILL.md"},
                "tool_response": "secret token=do-not-log",
            },
            "claude",
            "PostToolUse",
        )
        self.assertEqual("skill_file_read", event["kind"])
        self.assertEqual("test-engineering", event["skill_name"])
        self.assertNotIn("tool_response", event)
        self.assertNotIn("do-not-log", json.dumps(event))

    def test_stop_records_claim_flags_without_message_text(self):
        with tempfile.TemporaryDirectory() as directory:
            cwd = Path(directory)
            (cwd / "api-test-matrix.json").write_text("{}", encoding="utf-8")
            event = hook.build_event(
                {
                    "hook_event_name": "Stop",
                    "cwd": str(cwd),
                    "last_assistant_message": "测试完成，可以上线。token=abc123",
                },
                "claude",
                "Stop",
            )
        self.assertEqual("session_stop", event["kind"])
        self.assertTrue(event["claims_complete"])
        self.assertTrue(event["matrix_present"])
        self.assertNotIn("可以上线", json.dumps(event, ensure_ascii=True))
        self.assertNotIn("abc123", json.dumps(event))

    def test_cli_appends_under_pernavo_home_and_never_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / ".pernavo"
            result = subprocess.run(
                [sys.executable, str(SCRIPT)],
                input=json.dumps(
                    {
                        "hook_event_name": "PreToolUse",
                        "tool_name": "Skill",
                        "tool_input": {"skill": "data-work"},
                    }
                ),
                text=True,
                capture_output=True,
                env={
                    **os.environ,
                    "PERNAVO_HOME": str(home),
                    "PERNAVO_RUNTIME_SOURCE": "codex",
                },
                check=True,
            )
            self.assertEqual({"continue": True, "suppressOutput": True}, json.loads(result.stdout))
            log = home / "logs" / "runtime.jsonl"
            event = json.loads(log.read_text(encoding="utf-8"))
            self.assertEqual("pernavo.runtime_event.v1", event["schema_version"])
            self.assertEqual("skill_invoked", event["kind"])
            self.assertEqual("data-work", event["skill_name"])
            self.assertEqual("codex", event["source"])


if __name__ == "__main__":
    unittest.main()
