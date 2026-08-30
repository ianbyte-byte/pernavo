import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAUDE = ROOT / "CLAUDE.md"
CHANGE_REVIEW = ROOT / "skills" / "change-review" / "SKILL.md"
ENGINEERING = ROOT / "skills" / "engineering-workflow" / "SKILL.md"
TEST_ENGINEERING = ROOT / "skills" / "test-engineering" / "SKILL.md"
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
        self.assertIn("no remaining P1", contract)
        self.assertIn("findings list is empty", contract)
        self.assertIn("fresh context", contract)
        self.assertIn("invoke `/open-code-review`", contract)
        self.assertIn(
            "do not invoke a review or cleanup workflow merely because the task involves code",
            contract,
        )

    def test_change_review_reports_findings_only_and_stops_on_severity(self):
        contract = folded(CHANGE_REVIEW)
        self.assertIn("do not silently edit", contract)
        self.assertIn("implement fixes", contract)
        self.assertIn("fresh context", contract)
        self.assertIn("findings list is empty", contract)
        self.assertIn("no remaining P1", contract)
        self.assertIn("different agent, model, or session", contract)
        self.assertIn("When no actionable finding exists, say so", contract)

    def test_engineering_workflow_does_not_self_review_or_auto_loop(self):
        contract = folded(ENGINEERING)
        self.assertIn("one writer", contract)
        self.assertIn("does not review their own diff", contract)
        self.assertIn("Invoke `change-review` only when a diff review was requested", contract)
        self.assertIn("findings list is empty", contract)
        self.assertIn("fresh context", contract)
        self.assertIn("no remaining P1", contract)

    def test_test_engineering_does_not_reopen_review_or_edit(self):
        contract = folded(TEST_ENGINEERING)
        self.assertIn("does not re-open the review loop", contract)
        self.assertIn("does not authorize the verifier to edit the writer's tree", contract)


if __name__ == "__main__":
    unittest.main()
