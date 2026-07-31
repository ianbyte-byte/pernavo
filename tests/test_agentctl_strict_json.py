import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_agentctl_cli import AgentctlCase, SCRIPTS


class TestAgentctlStrictJson(AgentctlCase):
    def test_duplicate_config_event_and_sensitive_memory_members_are_fatal(self):
        # Given: duplicate keys in config, event, and a sensitive memory record
        # When: the corresponding CLI commands decode them
        # Then: each is rejected before routing or default-search filtering
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self.write_config(root)
            duplicate_config = config.parent / "duplicate-config.json"
            duplicate_config.write_text('{"schema_version":1,"schema_version":1,"memory":{"path":"memory.jsonl","scopes":["project"]},"routes":[]}', encoding="utf-8")
            duplicate_event = config.parent / "duplicate-event.json"
            duplicate_event.write_text('{"kind":"note","kind":"memory.search"}', encoding="utf-8")
            (config.parent / "memory.jsonl").write_text('{"id":"record","text":"café","scope":"project","sensitivity":"sensitive","sensitivity":"normal"}\n', encoding="utf-8")
            cases = (
                ["doctor", "--config", str(duplicate_config), "--json"],
                ["explain", "--config", str(config), "--event", str(duplicate_event), "--json"],
                ["memory", "search", "--config", str(config), "--query", "café", "--json"],
            )
            for arguments in cases:
                exit_code, result = self.run_cli(arguments)
                self.assertEqual(1, exit_code)
                self.assertEqual("duplicate_json_key", result["error"]["code"])

    def test_non_finite_numbers_at_config_event_and_memory_boundaries_are_fatal(self):
        # Given: NaN, Infinity, and an overflowing exponent at canonical boundaries
        # When: commands decode each input
        # Then: non-finite numbers always cause the same data error
        for literal in ("NaN", "Infinity", "-Infinity", "1e400"):
            with self.subTest(literal=literal), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                config = self.write_config(root)
                bad_config = config.parent / "bad-config.json"
                bad_config.write_text('{"schema_version":' + literal + ',"memory":{"path":"memory.jsonl","scopes":["project"]},"routes":[]}', encoding="utf-8")
                event = config.parent / "event.json"
                event.write_text('{"kind":' + literal + '}', encoding="utf-8")
                (config.parent / "memory.jsonl").write_text('{"id":"record","text":"x","scope":"project","sensitivity":"normal","number":' + literal + '}\n', encoding="utf-8")
                cases = (
                    ["doctor", "--config", str(bad_config), "--json"],
                    ["explain", "--config", str(config), "--event", str(event), "--json"],
                    ["memory", "search", "--config", str(config), "--query", "x", "--json"],
                )
                for arguments in cases:
                    exit_code, result = self.run_cli(arguments)
                    self.assertEqual(1, exit_code)
                    self.assertEqual("non_finite_number", result["error"]["code"])

    def test_deep_config_when_run_as_real_process_returns_json_error(self):
        # Given: a config JSON document deeper than Python's decoder recursion limit
        # When: the executable CLI reads it in a child process
        # Then: it exits one with a stable JSON envelope and no traceback
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "deep.json"
            config.write_text("[" * 2000 + "]" * 2000, encoding="utf-8")
            process = subprocess.run(
                [sys.executable, str(SCRIPTS / "agentctl.py"), "doctor", "--config", str(config), "--json"],
                capture_output=True,
                check=False,
                encoding="utf-8",
            )
        self.assertEqual(1, process.returncode)
        self.assertEqual("", process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual("doctor", result["command"])
        self.assertFalse(result["valid"])
        self.assertEqual("json_recursion", result["error"]["code"])
