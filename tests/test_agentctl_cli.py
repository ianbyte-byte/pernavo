import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import agentctl  # noqa: E402


class AgentctlCase(unittest.TestCase):
    def write_json(self, path, data):
        path.write_text(json.dumps(data), encoding="utf-8")

    def write_config(self, root, config=None, memory=None):
        config_dir = root / "config"
        config_dir.mkdir(parents=True)
        self.write_json(
            config_dir / "agentctl.json",
            config
            or {
                "schema_version": 1,
                "memory": {"path": "memory.jsonl", "scopes": ["project", "team"]},
                "routes": [
                    {
                        "id": "route.memory",
                        "priority": 20,
                        "when": {"kind": "memory.search"},
                        "requires": ["memory.read"],
                    },
                    {
                        "id": "route.note",
                        "priority": 10,
                        "when": {"kind": "note", "scope": "project"},
                        "requires": ["files.read"],
                    },
                ],
            },
        )
        lines = memory or [
            {"id": "alpha", "text": "Caf\u00e9 architecture", "scope": "project", "sensitivity": "normal"},
            {"id": "beta", "text": "CAF\u00c9 routing", "scope": "team", "sensitivity": "normal"},
            {"id": "secret", "text": "caf\u00e9 internal", "scope": "project", "sensitivity": "sensitive"},
        ]
        (config_dir / "memory.jsonl").write_text(
            "".join(json.dumps(line, ensure_ascii=False) + "\n" for line in lines), encoding="utf-8"
        )
        return config_dir / "agentctl.json"

    def run_cli(self, arguments):
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = agentctl.main(arguments)
        return exit_code, json.loads(output.getvalue()) if output.getvalue() else None

    def snapshot(self, root):
        paths = tuple(sorted(str(path.relative_to(root)) for path in root.rglob("*")))
        contents = {str(path.relative_to(root)): path.read_bytes() for path in root.rglob("*") if path.is_file()}
        return paths, contents


class TestAgentctlCli(AgentctlCase):
    def test_help_and_usage_exit_codes(self):
        # Given: the root command's parser
        # When: help and an invalid invocation are evaluated
        # Then: help succeeds and usage failures retain argparse's exit code
        with self.assertRaises(SystemExit) as help_raised:
            agentctl.main(["--help"])
        self.assertEqual(0, help_raised.exception.code)
        with self.assertRaises(SystemExit) as usage_raised:
            agentctl.main(["doctor"])
        self.assertEqual(2, usage_raised.exception.code)

    def test_doctor_when_valid_config_is_static_and_honest(self):
        # Given: a canonical config and memory relative to its own directory
        # When: doctor is run from another directory
        # Then: it validates data but marks runtime state unknown
        with tempfile.TemporaryDirectory() as directory:
            config = self.write_config(Path(directory))
            exit_code, result = self.run_cli(["doctor", "--config", str(config), "--json", "--dry-run"])
        self.assertEqual(0, exit_code)
        self.assertEqual({"schema_version": 1, "command": "doctor"}, {key: result[key] for key in ("schema_version", "command")})
        self.assertTrue(result["valid"])
        self.assertEqual("unknown", result["runtime"]["capabilities"])
        self.assertEqual("unknown", result["runtime"]["hooks"])
        self.assertEqual("unknown", result["runtime"]["auth"])
        self.assertEqual(3, result["memory"]["entries"])
        self.assertEqual(str((config.parent / "memory.jsonl").resolve()), result["memory"]["path"])

    def test_doctor_when_config_is_missing_invalid_unsupported_or_unknown_field_fails(self):
        # Given: malformed configurations at the CLI boundary
        # When: doctor evaluates each file
        # Then: each is a data failure with a stable JSON error envelope
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            missing = root / "absent.json"
            for config in (
                missing,
                self.write_config(root / "invalid", config={"schema_version": 1}),
                self.write_config(root / "unsupported", config={"schema_version": 9, "memory": {"path": "memory.jsonl", "scopes": ["project"]}, "routes": []}),
                self.write_config(root / "unknown", config={"schema_version": 1, "memory": {"path": "memory.jsonl", "scopes": ["project"]}, "routes": [], "extra": True}),
            ):
                exit_code, result = self.run_cli(["doctor", "--config", str(config), "--json"])
                self.assertEqual(1, exit_code)
                self.assertEqual("doctor", result["command"])
                self.assertFalse(result["valid"])

    def test_explain_when_matching_is_deterministic_and_capabilities_are_unknown(self):
        # Given: an event which exactly matches one route
        # When: explain is run twice
        # Then: matching, skipping, and unknown requirements are deterministic
        with tempfile.TemporaryDirectory() as directory:
            config = self.write_config(Path(directory))
            event = config.parent / "event.json"
            self.write_json(event, {"kind": "note", "scope": "project"})
            first = self.run_cli(["explain", "--config", str(config), "--event", str(event), "--json"])
            second = self.run_cli(["explain", "--config", str(config), "--event", str(event), "--json"])
        self.assertEqual(first, second)
        self.assertEqual(0, first[0])
        self.assertEqual(["route.note"], [item["id"] for item in first[1]["matched"]])
        self.assertEqual(["route.memory"], [item["id"] for item in first[1]["skipped"]])
        self.assertEqual([{"name": "files.read", "state": "unknown"}], first[1]["required_capabilities"])

    def test_explain_when_routes_collide_reports_conflict(self):
        # Given: two equally preferred routes matching an event
        # When: explain evaluates the event
        # Then: the collision is reported rather than silently hidden
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self.write_config(root, config={
                "schema_version": 1,
                "memory": {"path": "memory.jsonl", "scopes": ["project"]},
                "routes": [
                    {"id": "a", "priority": 1, "when": {"kind": "go"}, "requires": []},
                    {"id": "b", "priority": 1, "when": {"kind": "go"}, "requires": []},
                ],
            })
            event = config.parent / "event.json"
            self.write_json(event, {"kind": "go"})
            exit_code, result = self.run_cli(["explain", "--config", str(config), "--event", str(event), "--json"])
        self.assertEqual(0, exit_code)
        self.assertEqual([["a", "b"]], [conflict["route_ids"] for conflict in result["conflicts"]])

    def test_memory_search_when_unicode_scope_sensitivity_and_ties_apply(self):
        # Given: Unicode-equivalent memories across scope and sensitivity boundaries
        # When: searches apply explicit filters
        # Then: normal entries rank by score then id, and sensitive data needs opt-in
        with tempfile.TemporaryDirectory() as directory:
            config = self.write_config(Path(directory))
            basic = self.run_cli(["memory", "search", "--config", str(config), "--query", "cafe\u0301", "--json"])
            project = self.run_cli(["memory", "search", "--config", str(config), "--query", "CAF\u00c9", "--scope", "project", "--json"])
            sensitive = self.run_cli(["memory", "search", "--config", str(config), "--query", "caf\u00e9", "--include-sensitive", "--json"])
        self.assertEqual(0, basic[0])
        self.assertEqual(["alpha", "beta"], [entry["id"] for entry in basic[1]["results"]])
        self.assertEqual(["alpha"], [entry["id"] for entry in project[1]["results"]])
        self.assertEqual(["alpha", "beta", "secret"], [entry["id"] for entry in sensitive[1]["results"]])
        self.assertEqual("memory.jsonl", Path(basic[1]["results"][0]["provenance"]["path"]).name)

    def test_memory_and_doctor_when_jsonl_is_malformed_duplicate_or_cyclic_fail(self):
        # Given: canonical memory files with invalid JSONL or graph integrity
        # When: doctor and memory search read them
        # Then: malformed, duplicate, and cyclic records are fatal
        bad_memories = (
            "{bad}\n",
            '{"id":"a","text":"x","scope":"project","sensitivity":"normal"}\n{"id":"a","text":"y","scope":"project","sensitivity":"normal"}\n',
            '{"id":"a","text":"x","scope":"project","sensitivity":"normal","supersedes":"b"}\n{"id":"b","text":"y","scope":"project","sensitivity":"normal","supersedes":"a"}\n',
        )
        for memory in bad_memories:
            with self.subTest(memory=memory), tempfile.TemporaryDirectory() as directory:
                config = self.write_config(Path(directory), memory=[])
                (config.parent / "memory.jsonl").write_text(memory, encoding="utf-8")
                for arguments in (
                    ["doctor", "--config", str(config), "--json"],
                    ["memory", "search", "--config", str(config), "--query", "x", "--json"],
                ):
                    exit_code, result = self.run_cli(arguments)
                    self.assertEqual(1, exit_code)
                    self.assertFalse(result["valid"])

    def test_doctor_when_jsonl_is_not_utf8_fails(self):
        # Given: a canonical memory path whose bytes are not UTF-8
        # When: doctor reads the JSONL boundary
        # Then: encoding corruption is a fatal data error
        with tempfile.TemporaryDirectory() as directory:
            config = self.write_config(Path(directory), memory=[])
            (config.parent / "memory.jsonl").write_bytes(b"\xff\n")
            exit_code, result = self.run_cli(["doctor", "--config", str(config), "--json"])
        self.assertEqual(1, exit_code)
        self.assertEqual("invalid_jsonl", result["error"]["code"])

    def test_doctor_when_memory_symlink_escapes_physical_config_directory_fails(self):
        # Given: a config-relative memory symlink to a sibling outside its physical directory
        # When: doctor loads the config before opening memory
        # Then: physical path confinement rejects the escape
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self.write_config(root, config={
                "schema_version": 1,
                "memory": {"path": "escape.jsonl", "scopes": ["project"]},
                "routes": [],
            })
            outside = root / "outside.jsonl"
            outside.write_text('{"id":"outside","text":"x","scope":"project","sensitivity":"normal"}\n', encoding="utf-8")
            (config.parent / "escape.jsonl").symlink_to(outside)
            exit_code, result = self.run_cli(["doctor", "--config", str(config), "--json"])
        self.assertEqual(1, exit_code)
        self.assertEqual("unsafe_path", result["error"]["code"])

    def test_memory_search_when_entry_is_superseded_excludes_the_obsolete_entry(self):
        # Given: a memory entry that supersedes an earlier matching entry
        # When: default search runs
        # Then: only the active entry appears
        memories = [
            {"id": "old", "text": "canonical routing", "scope": "project", "sensitivity": "normal"},
            {"id": "new", "text": "canonical routing", "scope": "project", "sensitivity": "normal", "supersedes": "old"},
        ]
        with tempfile.TemporaryDirectory() as directory:
            config = self.write_config(Path(directory), memory=memories)
            exit_code, result = self.run_cli(["memory", "search", "--config", str(config), "--query", "canonical", "--json"])
        self.assertEqual(0, exit_code)
        self.assertEqual(["new"], [entry["id"] for entry in result["results"]])

    def test_memory_when_final_line_is_truncated_or_overlong_fails(self):
        # Given: JSONL without a final newline and JSONL exceeding the byte bound
        # When: doctor reads canonical memory
        # Then: both conditions are fatal
        cases = ((b'{"id":"a","text":"x","scope":"project","sensitivity":"normal"}', "truncated_jsonl"), (b"x" * 65537 + b"\n", "jsonl_limit"))
        for memory, expected_code in cases:
            with self.subTest(expected_code=expected_code), tempfile.TemporaryDirectory() as directory:
                config = self.write_config(Path(directory), memory=[])
                (config.parent / "memory.jsonl").write_bytes(memory)
                exit_code, result = self.run_cli(["doctor", "--config", str(config), "--json"])
                self.assertEqual(1, exit_code)
                self.assertEqual(expected_code, result["error"]["code"])

    def test_commands_when_run_against_input_directory_do_not_mutate_it(self):
        # Given: canonical config, event, and memory in a temporary input directory
        # When: all three read-only commands run
        # Then: the input directory path set and file contents are unchanged
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self.write_config(root)
            event = config.parent / "event.json"
            self.write_json(event, {"kind": "note", "scope": "project"})
            before = self.snapshot(root)
            self.run_cli(["doctor", "--config", str(config), "--json"])
            self.run_cli(["explain", "--config", str(config), "--event", str(event), "--json"])
            self.run_cli(["memory", "search", "--config", str(config), "--query", "café", "--json"])
            self.assertEqual(before, self.snapshot(root))
