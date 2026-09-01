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
        self.assertIn("不得 `mkdir`", install)
        self.assertIn('test ! -e "$PERNAVO_GLOBAL_AGENTS"', install)
        self.assertIn("Exact rollback for created AGENTS.md", install)
        self.assertIn("不得覆盖", readme)
        self.assertNotIn("分发到用户全局", readme)
        self.assertNotIn("分发到用户全局", install)

    def test_default_install_is_llm_mediated_skills_agents_and_stop_hook(self):
        install = folded(AI_INSTALL)
        readme = folded(README)
        agents = folded(ROOT / "AGENTS-PERNAVO.md")
        self.assertIn("由本手册中的安装代理阅读现有文件后再写入", install)
        self.assertIn("禁止对默认宿主路径直接 `--apply`", install)
        self.assertIn("api_test_stop_hook.py", install)
        self.assertIn("不得整文件替换", install)
        self.assertIn("先读取", install)
        self.assertIn("API 测试 Stop 门禁", readme)
        self.assertIn("不得整文件替换", readme)
        self.assertIn("runtime-hook.py", install)
        self.assertIn("$HOME/.pernavo/logs/runtime.jsonl", install)
        self.assertIn("不得记录原文 prompt", install)
        self.assertIn("~/.pernavo", readme)
        self.assertIn("~/.pernavo/logs", agents)
        self.assertIn(".pernavo/api-test-matrix.json", agents)
        self.assertNotIn("test-engineering", agents)
        self.assertNotIn("skills add", agents)
