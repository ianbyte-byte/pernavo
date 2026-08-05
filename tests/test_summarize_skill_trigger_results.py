import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "summarize-skill-trigger-results.py"
SPEC = importlib.util.spec_from_file_location("skill_trigger_summary", SCRIPT_PATH)
SUMMARY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(SUMMARY)


def command_event(command, exit_code=0, output=""):
    return {
        "type": "item.completed",
        "item": {
            "type": "command_execution",
            "command": command,
            "exit_code": exit_code,
            "aggregated_output": output,
        },
    }


class SummarizeSkillTriggerResultsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.corpus = self.root / "corpus.tsv"
        self.results = self.root / "results"
        self.results.mkdir()
        self.project_skill_root = self.root / "workspace" / ".agents" / "skills"
        self.corpus.write_text(
            "id\tsubject\texpected\tforbidden\tprompt\n"
            "case\talpha\talpha\tbeta\tabstract request\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_result(self, *events):
        (self.results / "case.jsonl").write_text(
            "\n".join(json.dumps(event) for event in events) + "\n",
            encoding="utf-8",
        )
        return SUMMARY.summarize(self.corpus, self.results, self.project_skill_root)[0]

    def test_path_text_without_a_reader_is_not_loaded(self):
        result = self.write_result(
            command_event("echo .agents/skills/alpha/SKILL.md"),
            {"type": "turn.completed"},
        )

        self.assertTrue(result["completed"])
        self.assertFalse(result["target_observed"])
        self.assertFalse(result["pass"])

    def test_successful_reader_for_target_is_loaded(self):
        result = self.write_result(
            command_event("sed -n '1,20p' .agents/skills/alpha/SKILL.md"),
            {"type": "turn.completed"},
        )

        self.assertEqual(["alpha"], result["project_reads"])
        self.assertTrue(result["target_observed"])
        self.assertTrue(result["pass"])

    def test_single_cat_with_zero_exit_proves_read(self):
        result = self.write_result(
            command_event("cat .agents/skills/alpha/SKILL.md"),
            {"type": "turn.completed"},
        )

        self.assertEqual(["alpha"], result["project_reads"])
        self.assertTrue(result["pass"])

    def test_compound_zero_exit_does_not_prove_earlier_read_without_frontmatter(self):
        result = self.write_result(
            command_event("cat .agents/skills/alpha/SKILL.md; true"),
            {"type": "turn.completed"},
        )

        self.assertEqual([], result["project_reads"])
        self.assertFalse(result["pass"])

    def test_compound_read_with_matching_frontmatter_does_not_prove_read(self):
        result = self.write_result(
            command_event(
                "cat .agents/skills/alpha/SKILL.md; true",
                output="---\nname: alpha\n---\n",
            ),
            {"type": "turn.completed"},
        )

        self.assertEqual([], result["project_reads"])
        self.assertFalse(result["pass"])

    def test_reader_for_another_target_does_not_prove_the_path(self):
        result = self.write_result(
            command_event("cat notes.txt; echo .agents/skills/alpha/SKILL.md"),
            {"type": "turn.completed"},
        )

        self.assertEqual([], result["project_reads"])
        self.assertFalse(result["pass"])

    def test_pattern_search_for_target_path_does_not_prove_a_read(self):
        result = self.write_result(
            command_event("rg -n '.agents/skills/alpha/SKILL.md' notes.txt"),
            {"type": "turn.completed"},
        )

        self.assertEqual([], result["project_reads"])
        self.assertFalse(result["target_observed"])

    def test_redirection_targets_are_not_reader_inputs(self):
        for redirect in (
            "> .agents/skills/alpha/SKILL.md",
            "2>.agents/skills/alpha/SKILL.md",
            "&>.agents/skills/alpha/SKILL.md",
        ):
            with self.subTest(redirect=redirect):
                result = self.write_result(
                    command_event(f"cat README.md {redirect}"),
                    {"type": "turn.completed"},
                )

                self.assertEqual([], result["project_reads"])
                self.assertFalse(result["target_observed"])

    def test_frontmatter_requires_the_same_reader_to_read_the_target(self):
        result = self.write_result(
            command_event(
                "cat notes.txt; echo .agents/skills/alpha/SKILL.md",
                output="---\nname: alpha\n---\n",
            ),
            {"type": "turn.completed"},
        )

        self.assertEqual([], result["project_reads"])
        self.assertFalse(result["pass"])

    def test_compound_reader_then_failure_does_not_prove_read(self):
        result = self.write_result(
            command_event(
                "cat .agents/skills/alpha/SKILL.md && false",
                exit_code=1,
                output="---\nname: alpha\n---\n",
            ),
            {"type": "turn.completed"},
        )

        self.assertEqual([], result["project_reads"])
        self.assertFalse(result["pass"])

    def test_echoed_frontmatter_before_a_compound_reader_does_not_prove_read(self):
        result = self.write_result(
            command_event(
                "echo 'name: alpha'; cat .agents/skills/alpha/SKILL.md; true",
                output="name: alpha\n",
            ),
            {"type": "turn.completed"},
        )

        self.assertEqual([], result["project_reads"])
        self.assertFalse(result["pass"])

    def test_timeout_and_unobserved_are_not_completed_or_passed(self):
        timed_out = self.write_result(command_event("true", exit_code=124))
        self.assertEqual("timeout", timed_out["observation"])
        self.assertFalse(timed_out["completed"])
        self.assertFalse(timed_out["pass"])

        (self.results / "case.jsonl").write_text("", encoding="utf-8")
        unobserved = SUMMARY.summarize(self.corpus, self.results, self.project_skill_root)[0]
        self.assertEqual("unobserved", unobserved["observation"])
        self.assertTrue(unobserved["issued"])
        self.assertFalse(unobserved["completed"])

    def test_timeout_overrides_a_completed_turn(self):
        result = self.write_result(
            command_event("true", exit_code=124),
            {"type": "turn.completed"},
        )

        self.assertEqual("timeout", result["observation"])
        self.assertFalse(result["completed"])
        self.assertFalse(result["pass"])

    def test_forbidden_read_prevents_target_observation(self):
        result = self.write_result(
            command_event("cat .agents/skills/alpha/SKILL.md"),
            command_event("cat .agents/skills/beta/SKILL.md"),
            {"type": "turn.completed"},
        )

        self.assertEqual(["beta"], result["forbidden_hits"])
        self.assertFalse(result["target_observed"])
        self.assertFalse(result["pass"])


if __name__ == "__main__":
    unittest.main()
