# Pernavo

Local-first skills, memory, and tool orchestration for AI agents.

Repository web page: [https://github.com/tuloong/pernavo](https://github.com/tuloong/pernavo)

Skill sources live under `skills/<name>/SKILL.md`.

## For Humans

**Strongly recommended: let an AI agent install this for you.** The agent should read the complete
guide before changing any Skill, Harness, or memory configuration.

Paste this prompt into Codex, Claude Code, Cursor, or another coding agent:

```text
Install and configure Pernavo by following the complete instructions here:
https://raw.githubusercontent.com/tuloong/pernavo/refs/heads/main/AI_INSTALL.md

Read the entire guide before acting. If the URL is unavailable or the repository does not expose
the 14 Skills declared by the guide, stop and report that the requested version is not published.
Do not fall back to older README installation commands.
```

## For LLM Agents

Fetch the complete guide and follow it step by step:

```bash
curl -fsSL https://raw.githubusercontent.com/tuloong/pernavo/refs/heads/main/AI_INSTALL.md
```

This command only prints the guide; never pipe it into a shell. A non-zero exit or empty response is
a stop condition. The guide owns authorization, conflict detection, verification, and rollback.

Local checkout readers may open [AI_INSTALL.md](AI_INSTALL.md) directly.

## Read-only local harness inspection

Phase 1 includes a Python 3.9, stdlib-only local inspector for canonical JSON configuration and JSONL memory:

```bash
python3 scripts/agentctl.py doctor --config harness/examples/agentctl.json --json
python3 scripts/agentctl.py explain --config harness/examples/agentctl.json --event harness/examples/event.json --json
python3 scripts/agentctl.py memory search --config harness/examples/agentctl.json --query canonical --json
```

Relative memory paths resolve from the configuration file, not the current directory. `doctor` validates only local static data and reports runtime capabilities, hooks, and authentication as `unknown`. `explain` is deterministic exact-field routing over JSON input; `memory search` reads JSONL without changing it. `--dry-run` is an accepted no-op because every Phase 1 command is already read-only.

This proves deterministic local routing simulation and data integrity only. It does not prove that any model or harness invoked a skill or tool. `MEMORY.md` is a future human-readable projection, not authoritative storage in Phase 1.

## List skills

```bash
npx skills add https://github.com/tuloong/pernavo --list
```

## Install all skills for the current user's Codex

```bash
npx skills add https://github.com/tuloong/pernavo \
  --global --agent codex --skill '*' --yes --copy
```

Installing to every supported agent requires separate, explicit authorization; see
[AI_INSTALL.md](AI_INSTALL.md).

Do not project-install this package into its own checkout: that creates tracked or local
`.agents/skills` copies which can become stale and compete with the source under `skills/`.
Use the regression command below while developing. After validation and the conflict/snapshot gates
in [AI_INSTALL.md](AI_INSTALL.md), deliberately refresh a user-level Codex installation from the
current checkout when runtime testing needs it:

```bash
./scripts/validate-skills.sh
npx skills add . --global --agent codex --skill '*' --yes --copy
```

## Included skills

- `audit-agent-harness` — run reversible ablation audits on CLAUDE.md, AGENTS.md, Skills, Hooks, prompts, and other agent customizations without disabling safety controls
- `aviation-grade-engineering` — apply aviation-grade engineering rigor: risk-driven lifecycle, multi-layer test defense, SRE observability, resilience patterns, CI/CD quality gates, and blameless postmortems
- `codebase-slimming`
- `coding-task-controller` — govern risk-path selection and phase handoffs without owning delivery work
- `develop-production-code` — implement the smallest retained production change and hand off author evidence
- `engineering-work-system` — cross-domain workflow router and engineering-health assessor; focused tasks go directly to their specialist Skill
- `exa-search`
- `gpt55-fusion`
- `graph-engineering` — design auditable agent execution topologies with explicit routing, ownership, and verification
- `plan-code-change` — turn confirmed discovery into an executable, reviewable change plan
- `pplx-cli`
- `review-mr` — produce findings on an existing diff; separate from behavior verification
- `unknowns-field-guide` — discover pre-change facts, blindspots, assumptions, and evidence gaps
- `verify-change-evidence` — independently observe completed-change behavior and report proof boundaries
