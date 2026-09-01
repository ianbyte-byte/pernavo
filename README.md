# Pernavo

Local-first skills, memory, and tool orchestration for AI agents.

Repository web page: [https://github.com/ianbyte-byte/pernavo](https://github.com/ianbyte-byte/pernavo)

Skill sources live under `skills/<name>/SKILL.md`. Repository instructions live in [AGENTS.md](AGENTS.md).
The separate [AGENTS-PERNAVO.md](AGENTS-PERNAVO.md) file is the distributable source for cross-project guidance and
contains no Skill inventory. Project routing for implement, review, and verify lives in [CLAUDE.md](CLAUDE.md);
review ownership is `change-review` (alias `/review-mr`).

For end-to-end workflow and trigger experiments, including the boundary between static,
installed, loaded, executed, and target-observed evidence, read
[End-to-End Skill Workflow and Trigger Experiments](docs/skill-workflow-and-trigger-experiments.md).

Codex and Claude Code hooks append privacy-preserving Skill usage evidence to the shared local
JSONL file `~/.codex/skill-usage/events.jsonl`. The logger records source, event kind, Skill name,
status, and session metadata, but never raw prompts, commands, tool responses, credentials, or data
rows. Analyze it with:

```bash
python3 scripts/skill-usage-report.py \
  --events ~/.codex/skill-usage/events.jsonl \
  --date 2026-08-28 --timezone Asia/Shanghai \
  --output docs/audit/skill-events.json
```

See [Cross-Agent Skill Usage Logging](docs/skill-usage-hook-integration.md) for the schema and Hook
configuration details.

For a source-backed, vendor-neutral policy for bounded cost-aware multi-agent routing, read
[Cost-Aware Multi-Agent Orchestration](docs/reference/cost-aware-multi-agent-orchestration.md).

For the public-source methodology behind hidden performance-risk review, read
[Hidden Performance Public Research](docs/reference/hidden-performance-public-research.md).

## Install with an AI agent

Paste this prompt into Codex, Claude Code, Cursor, or another coding agent:

```text
请为我安装 Pernavo 的完整 Skills 系统。完整执行手册：
https://raw.githubusercontent.com/ianbyte-byte/pernavo/refs/heads/main/AI_INSTALL.md

默认参数：官方 GitHub 来源、当前用户、所有支持 global 安装的 agents、全部 8 个 Skills、
从固定 SHA checkout 执行 copy；使用 `--agent '*'`，不要只安装 Codex。远程 URL 只用于发现和
clone，不直接用于安装。
开始前必须读取全文、重新检查 skills CLI 的 version/help、确认授权、精确核对远程 --list
和 JSON 同名冲突；不要盲跑，不要使用 --all 或 remove --all。冲突默认按方案 A 处理：仅在旧
来源和固定 revision 可精确恢复时定向替换；否则停止。安装后完成固定 SHA 记录、JSON diff、
新会话代表性 smoke（正向/负向/碰撞）、报告和定向回滚记录。
安装完成后，仅当全局 `$CODEX_HOME/AGENTS.md` 不存在时，将固定 checkout 中的
`AGENTS-PERNAVO.md` 创建为该文件；已存在则跳过或停止，不得覆盖。它只保存
学习笔记提炼出的通用规范，不保存 Skills 清单或安装流程。
若远程 --list 不是精确 8 项，停止并说明该版本尚未发布；未运行完整 24-case corpus 时，
不得声称全部 8 项的 runtime activation 已验证。
```

The installation prompt's 8 Skills and 24 cases refer to the consolidated documented installation
set. Retired fine-grained Skills remain recoverable under `skills-archive/` but are outside the
default discovery root. The remote `--list`, fixed revision, and trigger corpus must remain
synchronized before installation is treated as complete.

The complete procedure is [AI_INSTALL.md](AI_INSTALL.md). An AI may fetch the published guide with:

```bash
curl -fsSL https://raw.githubusercontent.com/ianbyte-byte/pernavo/refs/heads/main/AI_INSTALL.md
```

This only prints Markdown; never pipe it into a shell. The remote URL is for discovery and cloning,
not direct installation or installed-revision proof. If its `--list` output is not the exact 8-name
set in the guide, stop and report that the documented version is not published. Do not claim that
local uncommitted work is available remotely.

## Read-only local harness inspection

Phase 1 includes a Python 3.9, stdlib-only local inspector for canonical JSON configuration and JSONL memory:

```bash
python3 scripts/agentctl.py doctor --config harness/examples/agentctl.json --json
python3 scripts/agentctl.py explain --config harness/examples/agentctl.json --event harness/examples/event.json --json
python3 scripts/agentctl.py memory search --config harness/examples/agentctl.json --query canonical --json
```

Relative memory paths resolve from the configuration file, not the current directory. `doctor` validates only local static data and reports runtime capabilities, hooks, and authentication as `unknown`. `explain` is deterministic exact-field routing over JSON input; `memory search` reads JSONL without changing it. `--dry-run` is an accepted no-op because every Phase 1 command is already read-only.

This proves deterministic local routing simulation and data integrity only. It does not prove that any model or harness invoked a skill or tool. `MEMORY.md` is a future human-readable projection, not authoritative storage in Phase 1.

Do not copy a bare install command from this README. The guide requires authorization, current CLI
help, an exact remote list, a fixed-SHA checkout, before/after JSON snapshots, conflict
classification, and a new-session runtime check. It also explains the boundary between installing
workflow policy and proving host subagents, model routing, Hooks, MCP, permissions, or Harness.

Repository maintainers can validate the source without installing it:

```bash
./scripts/validate-skills.sh
```

## External quality evidence for cleanup agents

`codebase-slimming` includes a standard-library-only tool runner that lets an agent inventory and
invoke explicitly selected analyzers without installing anything or using a shell:

```bash
python3 skills/codebase-slimming/scripts/quality_evidence.py inventory --target . --json

python3 skills/codebase-slimming/scripts/quality_evidence.py run \
  --target . \
  --evidence-dir .codebase-slimming/evidence/baseline-001 \
  --tool scc \
  --dry-run \
  --json
```

Built-in adapters cover `scc`, `knip`, .NET package inventory, .NET SDK analyzers, Roslyn analyzers,
Coverlet collection, SonarScanner, and OWASP Dependency-Check. Real runs capture commands, analyzer version probes, exit status,
stdout/stderr hashes, normalized metrics where available, and an explicit proof boundary in
`manifest.json`. Networked or
worktree-writing adapters require opt-in gates. See the
[external evidence toolchain](skills/codebase-slimming/references/external-evidence-toolchain.md)
for execution examples, NDepend/ArchUnit integration guidance, and the evidence ladder required
before deleting a candidate.

For a local SonarQube Server, Skills can use SonarScanner through `quality_evidence.py` or generate a
secret-free, read-only MCP configuration proposal through `sonarqube_local.py`:

```bash
python3 skills/change-review/scripts/sonarqube_local.py \
  mcp-config \
  --client codex \
  --url http://localhost:9000 \
  --project-key my-project \
  --workspace /absolute/project \
  --image sonarsource/sonarqube-mcp:<pinned-version> \
  --json
```

The helper never writes host configuration, pulls or starts a container, or persists the required
`SONARQUBE_TOKEN`. Configuration, running-container, host tool discovery, and completed quality-query
evidence remain separate states.

## Hidden performance review

`performance-work` now owns static review, reproducible measurement, database/runtime/browser
overlays, and benchmark discipline. `data-work` supplies the database-specific static and test-target
checks; the split between hypothesis and runtime proof remains mandatory.

The standard-library-only evidence helper is inventory/validation only; it does not run a workload,
profiler, database query, or network call:

```bash
python3 skills/performance-work/scripts/performance_evidence.py inventory --target . --json
python3 skills/performance-work/scripts/performance_evidence.py validate <manifest.json>
```

Performance findings must retain the workload, target, revision, time window, sample distribution,
resource signals, and proof boundary. A static smell or single average does not establish a bottleneck.

## Included skills

- `engineering-workflow` — route intent and authority through discovery, planning, one-writer implementation, independent verification, and delivery boundaries
- `codebase-slimming` — slim and decouple an existing codebase with a baseline, bounded pilot, and behavior-preserving batches
- `data-work` — inspect SQL/ORM shape and run bounded, explicitly configured test-database checks
- `performance-work` — review and measure application, database, runtime, browser, and benchmark performance
- `change-review` — review Git diffs and MRs with separate correctness, performance, and environment evidence
- `report-writer` — turn supplied facts and evidence into a formal report and select Markdown, spreadsheet, PDF, HTML, Word, or slides from its intended use
- `repository-governance` — govern project/repository baselines, instructions, ownership, memory, agent configuration, and Skill-system hygiene from observed evidence
- `test-engineering` — route unit, integration, API, functional, regression, acceptance, and release-smoke tests across white-box, gray-box, and black-box evidence

The current source checkout contains 8 default Skills and the trigger corpus contains 24 positive,
negative, and collision cases. Retired source is preserved in
`skills-archive/20260826-pre-consolidation/`. Run `python3 scripts/skill-usage-report.py --db
<codex-history.sqlite> --output <report.json>` to refresh aggregate usage evidence, then run
`./scripts/validate-skills.sh` to validate source layout, links, README entries, trigger triplets,
and the local Skills CLI listing.
