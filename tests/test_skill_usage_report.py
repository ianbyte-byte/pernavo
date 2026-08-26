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


if __name__ == "__main__":
    unittest.main()
