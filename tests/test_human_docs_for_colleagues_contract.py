import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "human-docs-for-colleagues" / "SKILL.md"
CLAUDE = ROOT / "CLAUDE.md"
REPORT = ROOT / "skills" / "report-writer" / "SKILL.md"
GOVERNANCE = ROOT / "skills" / "repository-governance" / "SKILL.md"


class HumanDocsForColleaguesContractTests(unittest.TestCase):
    def test_triggers_and_boundaries(self):
        contract = SKILL.read_text(encoding="utf-8")

        self.assertIn("给同事看", contract)
        self.assertIn("对接文档", contract)
        self.assertIn("不要太啰嗦", contract)
        self.assertIn("`report-writer`", contract)
        self.assertIn("`engineering-workflow`", contract)
        self.assertIn("Do not use for agent skills", contract)

    def test_keep_cut_and_scan_budget(self):
        contract = SKILL.read_text(encoding="utf-8")

        self.assertIn("Scan time is the budget", contract)
        self.assertIn("result == 1", contract)
        self.assertIn("data-dictionary constants", contract)
        self.assertIn("full JSON walkthroughs", contract)
        self.assertIn("各场景只记差异", contract)
        self.assertIn("under half the page", contract)

    def test_claude_and_sibling_skills_route_here(self):
        claude = CLAUDE.read_text(encoding="utf-8")
        report = REPORT.read_text(encoding="utf-8")
        governance = GOVERNANCE.read_text(encoding="utf-8")

        self.assertIn("human-docs-for-colleagues", claude)
        self.assertIn("给同事看", claude)
        self.assertIn("`human-docs-for-colleagues`", report)
        self.assertIn("`human-docs-for-colleagues`", governance)


if __name__ == "__main__":
    unittest.main()
