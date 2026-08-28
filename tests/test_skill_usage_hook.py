import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "skill-usage-hook.py"
SPEC = importlib.util.spec_from_file_location("skill_usage_hook", SCRIPT)
skill_usage_hook = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(skill_usage_hook)


class SkillUsageHookCase(unittest.TestCase):
    def test_skill_read_event_contains_evidence_without_payload(self):
        event = skill_usage_hook.build_event(
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

    def test_prompt_is_hashed_and_not_recorded(self):
        event = skill_usage_hook.build_event(
            {"hook_event_name": "UserPromptSubmit", "prompt": "use token=abc123 to test skills"},
            "codex",
            "UserPromptSubmit",
        )
        self.assertEqual("prompt_submitted", event["kind"])
        self.assertEqual(len("use token=abc123 to test skills"), event["prompt_length"])
        self.assertNotIn("abc123", json.dumps(event))
        self.assertRegex(event["prompt_sha256"], r"^[0-9a-f]{64}$")

    def test_cli_appends_jsonl_and_never_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "events.jsonl"
            result = subprocess.run(
                [sys.executable, str(SCRIPT)],
                input=json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Skill", "tool_input": {"skill": "data-work"}}),
                text=True,
                capture_output=True,
                env={**os.environ, "SKILL_USAGE_SOURCE": "codex", "SKILL_USAGE_LOG": str(log)},
                check=True,
            )
            self.assertEqual({"continue": True, "suppressOutput": True}, json.loads(result.stdout))
            event = json.loads(log.read_text(encoding="utf-8"))
            self.assertEqual("skill_invoked", event["kind"])
            self.assertEqual("data-work", event["skill_name"])


if __name__ == "__main__":
    unittest.main()
