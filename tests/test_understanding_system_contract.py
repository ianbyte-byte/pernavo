import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "understanding-system" / "SKILL.md"
CLAUDE = ROOT / "CLAUDE.md"
DATA = ROOT / "skills" / "data-work" / "SKILL.md"
HANDOFF = ROOT / "skills" / "human-docs-for-colleagues" / "SKILL.md"
GOVERNANCE = ROOT / "skills" / "repository-governance" / "SKILL.md"
REFERENCES = (
    "structure.md",
    "repetition.md",
    "choice.md",
    "alignment.md",
    "table.md",
    "er.md",
    "flow.md",
    "state.md",
)


class UnderstandingSystemContractTests(unittest.TestCase):
    def test_one_page_per_question_and_paper_routes(self):
        contract = SKILL.read_text(encoding="utf-8")

        self.assertIn("/understanding-system", contract)
        self.assertIn(".pernavo/system-design.md", contract)
        self.assertIn("表设计", contract)
        self.assertIn("方案", contract)
        self.assertIn("mermaid", contract.lower())
        self.assertNotIn("read only", contract)
        self.assertNotIn("excalidraw", contract.lower())
        self.assertIn("搞清楚一个系统的设计", contract)
        self.assertIn("references/structure.md", contract)
        self.assertIn("references/er.md", contract)
        self.assertIn("references/flow.md", contract)
        self.assertIn("references/state.md", contract)
        self.assertIn("`engineering-workflow`", contract)
        self.assertIn("`data-work`", contract)
        self.assertIn("`human-docs-for-colleagues`", contract)
        for name in REFERENCES:
            self.assertTrue((SKILL.parent / "references" / name).is_file(), name)

    def test_siblings_route_design_explanation_here(self):
        self.assertIn("understanding-system", CLAUDE.read_text(encoding="utf-8"))
        self.assertIn("搞清楚一个系统的设计", CLAUDE.read_text(encoding="utf-8"))
        self.assertIn("`understanding-system`", DATA.read_text(encoding="utf-8"))
        self.assertIn("`understanding-system`", HANDOFF.read_text(encoding="utf-8"))
        self.assertIn("`understanding-system`", GOVERNANCE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
