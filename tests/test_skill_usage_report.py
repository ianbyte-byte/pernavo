import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "skill-usage-report.py"
SPEC = importlib.util.spec_from_file_location("skill_usage_report", SCRIPT)
skill_usage_report = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(skill_usage_report)


class SkillUsageReportCase(unittest.TestCase):
    def test_reads_only_user_message_text(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "history.sqlite"
            with sqlite3.connect(database) as connection:
                connection.execute(
                    "CREATE TABLE thread_items (created_at_ms INTEGER, item_json TEXT, item_type TEXT)"
                )
                connection.executemany(
                    "INSERT INTO thread_items VALUES (?, ?, ?)",
                    [
                        (1, json.dumps({"content": [{"text": "review-mr 审查 SQL 性能"}]}), "userMessage"),
                        (2, json.dumps({"content": [{"text": "ignored secret"}]}), "agentMessage"),
                    ],
                )
            messages, first_ms, last_ms = skill_usage_report.read_user_messages(database)
        self.assertEqual(["review-mr 审查 SQL 性能"], messages)
        self.assertEqual(1, first_ms)
        self.assertEqual(1, last_ms)

    def test_groups_continuations_and_requires_reader_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "rollout-a.jsonl"
            continuation = root / "rollout-a_child.jsonl"
            meta = {
                "timestamp": "2026-08-28T01:00:00Z",
                "type": "session_meta",
                "payload": {"session_id": "session-a", "thread_source": "user"},
            }
            user = {
                "timestamp": "2026-08-28T01:00:01Z",
                "type": "event_msg",
                "payload": {
                    "type": "item_completed",
                    "item": {"type": "UserMessage", "content": [{"text": "修复接口并补充回归测试"}]},
                },
            }
            loaded = {
                "timestamp": "2026-08-28T01:00:02Z",
                "type": "response_item",
                "payload": {
                    "type": "custom_tool_call",
                    "name": "exec",
                    "input": "tools.exec_command({cmd: \"sed -n '1,80p' .agents/skills/test-engineering/SKILL.md\"})",
                },
            }
            completion = {"timestamp": "2026-08-28T01:00:03Z", "type": "event_msg", "payload": {"type": "task_complete"}}
            first.write_text("\n".join(json.dumps(item) for item in (meta, user)), encoding="utf-8")
            continuation.write_text("\n".join(json.dumps(item) for item in (meta, loaded, completion)), encoding="utf-8")

            report = skill_usage_report.build_session_usage_report(root, "2026-08-28", "Asia/Shanghai")

        self.assertEqual(1, report["task_count"])
        self.assertEqual(["test-engineering"], report["tasks"][0]["loaded_skills"])
        self.assertEqual(["engineering-workflow"], report["tasks"][0]["missed_opportunity"])
        self.assertEqual(1, report["summary"]["loaded"]["test-engineering"])

    def test_generated_evaluator_prompts_are_excluded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            events = [
                {
                    "timestamp": "2026-08-28T01:00:00Z",
                    "type": "session_meta",
                    "payload": {"session_id": "synthetic", "thread_source": "user"},
                },
                {
                    "timestamp": "2026-08-28T01:00:01Z",
                    "type": "event_msg",
                    "payload": {
                        "type": "item_completed",
                        "item": {
                            "type": "UserMessage",
                            "content": [{"text": "Complete the following task for the user. Score how well the response satisfies the rubric"}],
                        },
                    },
                },
            ]
            (root / "rollout.jsonl").write_text("\n".join(json.dumps(item) for item in events), encoding="utf-8")
            report = skill_usage_report.build_session_usage_report(root, "2026-08-28", "Asia/Shanghai")

        self.assertEqual(0, report["task_count"])

    def test_request_summary_redacts_credentials(self):
        self.assertEqual("call bearer [REDACTED]", skill_usage_report.redact_text("call bearer abc.def"))
        self.assertEqual("token=[REDACTED]", skill_usage_report.redact_text("token=abc123"))


if __name__ == "__main__":
    unittest.main()
