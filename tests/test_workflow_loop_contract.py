import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAUDE = ROOT / "CLAUDE.md"
CHANGE_REVIEW = ROOT / "skills" / "change-review" / "SKILL.md"
ENGINEERING = ROOT / "skills" / "engineering-workflow" / "SKILL.md"
TEST_ENGINEERING = ROOT / "skills" / "test-engineering" / "SKILL.md"
DATA_WORK = ROOT / "skills" / "data-work" / "SKILL.md"
PERFORMANCE = ROOT / "skills" / "performance-work" / "SKILL.md"
GOVERNANCE = ROOT / "skills" / "repository-governance" / "SKILL.md"
SLIMMING = ROOT / "skills" / "codebase-slimming" / "SKILL.md"
ENGINEERING_REPORT = ROOT / "skills" / "report-writer" / "references" / "engineering-review.md"
SKILLOPT_DIR = ROOT / "tests" / "skillopt"
DEFAULT_SKILLS = {
    "change-review",
    "codebase-slimming",
    "data-work",
    "engineering-workflow",
    "performance-work",
    "report-writer",
    "repository-governance",
    "test-engineering",
}
MACHINE_PATH = "/Users/chung/Developer/Code/loongclaude"


def folded(path):
    return " ".join(path.read_text(encoding="utf-8").split())


class WorkflowLoopContractTests(unittest.TestCase):
    def test_default_install_set_stays_eight_named_skills(self):
        names = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(DEFAULT_SKILLS, names)

    def test_claude_routes_review_to_change_review_without_self_review(self):
        contract = folded(CLAUDE)
        self.assertIn("invoke `change-review` (alias `/review-mr`)", contract)
        self.assertIn("engineering-workflow", contract)
        self.assertIn("test-engineering", contract)
        self.assertIn("different agent, model, or session", contract)
        self.assertIn("Do not implement", contract)
        self.assertIn("remaining P1 only", contract)
        self.assertIn("do not self-select P2 or P3", contract)
        self.assertIn("fresh context", contract)
        self.assertIn("invoke `/open-code-review`", contract)
        self.assertIn("do not implement suggested fixes", contract)
        self.assertIn(
            "do not invoke a review or cleanup workflow merely because the task involves code",
            contract,
        )

    def test_change_review_reports_findings_only_and_uses_default_policy(self):
        contract = folded(CHANGE_REVIEW)
        self.assertIn("do not silently edit", contract)
        self.assertIn("implement fixes", contract)
        self.assertIn("fresh context", contract)
        self.assertIn("remaining P1 only", contract)
        self.assertIn("do not self-select P2 or P3", contract)
        self.assertIn("different agent, model, or session", contract)
        self.assertIn("When no actionable finding exists, say so", contract)

    def test_engineering_workflow_does_not_self_review_or_self_select_nits(self):
        contract = folded(ENGINEERING)
        self.assertIn("one writer", contract)
        self.assertIn("does not review their own diff", contract)
        self.assertIn("Invoke `change-review` only when a diff review was requested", contract)
        self.assertIn("fresh context", contract)
        self.assertIn("remaining P1 only", contract)
        self.assertIn("do not self-select P2 or P3", contract)

    def test_test_engineering_does_not_reopen_review_or_edit(self):
        contract = folded(TEST_ENGINEERING)
        self.assertIn("does not re-open the review loop", contract)
        self.assertIn("does not authorize the verifier to edit the writer's tree", contract)
        self.assertIn("does not self-select P2 or P3", contract)

    def test_specialist_skills_do_not_implement_from_review(self):
        self.assertIn("Do not implement code or schema changes from a static review", folded(DATA_WORK))
        self.assertIn("do not silently edit", folded(PERFORMANCE))
        self.assertIn("This Skill reports findings; it is not the writer", folded(PERFORMANCE))
        self.assertIn("Do not implement from a `change-review` finding list", folded(GOVERNANCE))
        self.assertIn("writer does not implement from its own review notes", folded(SLIMMING))
        self.assertIn("Do not implement findings while formatting the report", folded(ENGINEERING_REPORT))
        self.assertIn("When called by `change-review` (alias `review-mr`)", folded(ENGINEERING_REPORT))

    def test_active_skillopt_fixtures_are_not_machine_specific(self):
        for path in sorted(SKILLOPT_DIR.glob("*.json")):
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn(MACHINE_PATH, text)
                payload = json.loads(text)
                self.assertEqual(".", payload["project"])
                for task in payload["tasks"]:
                    self.assertEqual(".", task["project"])


if __name__ == "__main__":
    unittest.main()
