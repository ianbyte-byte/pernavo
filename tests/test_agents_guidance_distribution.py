import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AI_INSTALL = ROOT / "AI_INSTALL.md"
README = ROOT / "README.md"


def folded(path):
    return " ".join(path.read_text(encoding="utf-8").split())


class AgentsGuidanceDistributionTests(unittest.TestCase):
    def test_install_guide_creates_global_agents_only_when_absent(self):
        install = folded(AI_INSTALL)
        readme = folded(README)
        self.assertNotIn("PERNAVO_GLOBAL_AGENTS_BACKUP", install)
        self.assertIn("不得覆盖已有文件", install)
        self.assertIn("粘贴提示不构成覆盖授权", install)
        self.assertIn("blocked-symlink", install)
        self.assertIn("skipped-identical", install)
        self.assertIn("blocked-existing", install)
        self.assertIn("不得 mkdir", install)
        self.assertIn('test ! -e "$PERNAVO_GLOBAL_AGENTS"', install)
        self.assertIn("Exact rollback for created AGENTS.md", install)
        self.assertIn("不得覆盖", readme)
        self.assertNotIn("分发到用户全局", readme)
        self.assertNotIn("分发到用户全局", install)
