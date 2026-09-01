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
        self.assertIn("replaced-empty", install)
        self.assertIn("不得 `mkdir`", install)
        self.assertIn('test ! -e "$PERNAVO_GLOBAL_AGENTS"', install)
        self.assertIn('test ! -s "$PERNAVO_GLOBAL_AGENTS"', install)
        self.assertIn("Exact rollback for created AGENTS.md", install)
        self.assertIn("Exact rollback for replaced-empty AGENTS.md", install)
        self.assertIn("--single-branch", install)
        self.assertIn("--depth 1", install)
        self.assertNotIn("fetch --all --tags", install)
        self.assertNotIn("skills ls --global --agent '*'", install)
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

    def test_default_install_covers_local_agent_harnesses_and_readonly_agentctl(self):
        install = folded(AI_INSTALL)
        readme = folded(README)
        self.assertIn("$HOME/.claude/rules/pernavo.md", install)
        self.assertIn("$HOME/.cursor/rules/pernavo.mdc", install)
        self.assertIn("$HOME/.grok/rules/pernavo.md", install)
        self.assertIn("$HOME/.cursor/hooks.json", install)
        self.assertIn("$HOME/.grok/hooks/pernavo.json", install)
        self.assertIn("不得覆盖 Claude 的 `~/.claude/AGENTS.md`", readme)
        self.assertIn("alwaysApply: true", install)
        self.assertIn("不得改写项目 `AGENTS.md`", install)
        self.assertNotIn("User Rules", install)
        self.assertIn("本机所有支持 global 安装的 agent harness", install)
        self.assertIn("--agent '*'", install)
        self.assertIn("python3 scripts/agentctl.py doctor", install)
        self.assertNotIn("Harness 检查（可选、独立授权）", install)
        self.assertIn("本机所有支持 global 安装的 agent harness", readme)
        self.assertIn("agentctl", readme)
