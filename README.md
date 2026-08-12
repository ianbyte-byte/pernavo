# Pernavo

Local-first skills, memory, and tool orchestration for AI agents.

Repository web page: [https://github.com/ianbyte-byte/pernavo](https://github.com/ianbyte-byte/pernavo)

Skill sources live under `skills/<name>/SKILL.md`.

For end-to-end workflow and trigger experiments, including the boundary between static,
installed, loaded, executed, and target-observed evidence, read
[End-to-End Skill Workflow and Trigger Experiments](docs/skill-workflow-and-trigger-experiments.md).

For a source-backed, vendor-neutral policy for bounded cost-aware multi-agent routing, read
[Cost-Aware Multi-Agent Orchestration](docs/reference/cost-aware-multi-agent-orchestration.md).

For the public-source methodology behind hidden performance-risk review, read
[Hidden Performance Public Research](docs/reference/hidden-performance-public-research.md).

## Install with an AI agent

Paste this prompt into Codex, Claude Code, Cursor, or another coding agent:

```text
请为我安装 Pernavo 的完整 Skills 系统。完整执行手册：
https://raw.githubusercontent.com/ianbyte-byte/pernavo/refs/heads/main/AI_INSTALL.md

默认参数：官方 GitHub 来源、当前用户、Codex、global、全部 25 个 Skills、从固定 SHA
checkout 执行 copy；远程 URL 只用于发现和 clone，不直接用于安装。
开始前必须读取全文、重新检查 skills CLI 的 version/help、确认授权、精确核对远程 --list
和 JSON 同名冲突；不要盲跑，不要使用 --all 或 remove --all。冲突默认按方案 A 处理：仅在旧
来源和固定 revision 可精确恢复时定向替换；否则停止。安装后完成固定 SHA 记录、JSON diff、
新会话代表性 smoke（正向/负向/碰撞）、报告和定向回滚记录。
若远程 --list 不是精确 25 项，停止并说明该版本尚未发布；未运行完整 75-case corpus 时，
不得声称全部 25 项的 runtime activation 已验证。
```

The installation prompt's 25 Skills and 75 cases refer to the complete documented installation set.
The six performance Skills are included in that set; the remote `--list`, fixed revision, and
trigger corpus must remain synchronized before installation is treated as complete.

The complete procedure is [AI_INSTALL.md](AI_INSTALL.md). An AI may fetch the published guide with:

```bash
curl -fsSL https://raw.githubusercontent.com/ianbyte-byte/pernavo/refs/heads/main/AI_INSTALL.md
```

This only prints Markdown; never pipe it into a shell. The remote URL is for discovery and cloning,
not direct installation or installed-revision proof. If its `--list` output is not the exact 25-name
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
python3 skills/codebase-slimming/scripts/sonarqube_local.py \
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

The performance suite separates static review from runtime proof:

- `performance-review` finds amplification signals and routes narrow-domain checks.
- `performance-measurement` defines reproducible workload, percentile, USE/RED, trace, and before/after evidence.
- `database-performance` checks SQL/ORM query shape, plans, round trips, cardinality, and locks.
- `runtime-performance` checks CPU, allocation, GC, blocking, queues, contention, I/O, and profiler evidence.
- `web-performance` checks LCP, INP, CLS, long tasks, resource loading, and field/lab data.
- `benchmark-performance` checks workload fidelity, setup separation, warmup, forks, variance, and result consumption.

The standard-library-only evidence helper is inventory/validation only; it does not run a workload,
profiler, database query, or network call:

```bash
python3 skills/performance-measurement/scripts/performance_evidence.py inventory --target . --json
python3 skills/performance-measurement/scripts/performance_evidence.py validate <manifest.json>
```

Performance findings must retain the workload, target, revision, time window, sample distribution,
resource signals, and proof boundary. A static smell or single average does not establish a bottleneck.

## Included skills

- `audit-agent-harness` — run reversible ablation audits on CLAUDE.md, AGENTS.md, Skills, Hooks, prompts, and other agent customizations without disabling safety controls
- `aviation-grade-engineering` — apply aviation-grade engineering rigor: risk-driven lifecycle, multi-layer test defense, SRE observability, resilience patterns, CI/CD quality gates, and blameless postmortems
- `codebase-slimming` — slim and decouple an existing codebase with a baseline, bounded pilot, and behavior-preserving batches
- `coding-task-controller` — govern risk-path selection and phase handoffs without owning delivery work
- `develop-production-code` — implement the smallest retained production change and hand off author evidence
- `engineering-work-system` — cross-domain workflow router and engineering-health assessor; focused tasks go directly to their specialist Skill
- `exa-search` — token-efficient Exa Search API workflows for neural web search, highlights, known-URL extraction, and structured enrichment
- `gpt55-fusion` — opt-in GPT-5.5 Fusion with two independent analyses and a judge when the user explicitly requests it
- `graph-engineering` — design auditable agent execution topologies with explicit routing, ownership, and verification
- `open-code-review` — run Alibaba's Open Code Review agent through the `ocr` CLI for line-level Git review and full-file scans
- `plan-code-change` — turn confirmed discovery into an executable, reviewable change plan
- `pplx-cli` — install, authenticate, or use Perplexity's `pplx` CLI for terminal web search and page fetch when the user asks for Perplexity
- `project-capability-engineering` — assess greenfield, existing, and legacy repository capabilities and select one evidence-based, reversible foundation increment
- `repository-knowledge-gardening` — inventory repository knowledge, detect documentation drift, and select one verifiable gardening increment without inferring unobserved behavior
- `report-writer` — turn supplied facts and evidence into a formal report and select Markdown, spreadsheet, PDF, HTML, Word, or slides from its intended use
- `review-mr` — produce findings on an existing diff with mandatory SonarQube evidence routing; separate from behavior verification
- `sonarqube-review` — mandatory read-only SonarQube quality-gate/measures/issues channel during code review through exposed MCP tools or a bundled API client; unavailable results stay labeled evidence
- `performance-review` — find hidden performance risks in code paths and route them to evidence-based measurement and domain overlays
- `performance-measurement` — design reproducible USE/RED, trace, percentile, resource, and before/after performance evidence
- `database-performance` — inspect SQL/ORM query shape, plans, round trips, cardinality, locks, and database runtime evidence
- `runtime-performance` — inspect CPU, allocations, GC, blocking, queues, contention, I/O, and matching profiler evidence
- `web-performance` — review LCP, INP, CLS, long tasks, resource loading, layout shifts, and field/lab evidence
- `benchmark-performance` — design reliable benchmarks with representative workloads, warmup, forks, variance, and setup separation
- `unknowns-field-guide` — discover pre-change facts, blindspots, assumptions, and evidence gaps
- `verify-change-evidence` — independently observe completed-change behavior and report proof boundaries

The current source checkout contains 25 Skills and the trigger corpus contains 75 positive, negative,
and collision cases. Run `./scripts/validate-skills.sh` to validate source layout, links, README
entries, trigger triplets, and the local Skills CLI listing.
