# loongclaude skills

Personal Codex/agent workflow skills packaged for the `skills` CLI.

Skill sources live under `skills/<name>/SKILL.md`.

## List skills

```bash
npx skills add https://github.com/tuloong/loongclaude --list
```

## Install all skills

```bash
npx skills add https://github.com/tuloong/loongclaude --all
```

Do not project-install this package into its own checkout: that creates tracked or local
`.agents/skills` copies which can become stale and compete with the source under `skills/`.
Use the regression command below while developing. After validation, deliberately refresh a
user-level Codex installation from the current checkout when runtime testing needs it:

```bash
./scripts/validate-skills.sh
npx skills add . --global --agent codex --skill '*' --yes --copy
```

## Included skills

- `review-mr`
- `codebase-slimming`
- `audit-agent-harness` — run reversible ablation audits on CLAUDE.md, AGENTS.md, Skills, Hooks, prompts, and other agent customizations without disabling safety controls
- `gpt55-fusion`
- `unknowns-field-guide`
- `coding-task-controller`
- `develop-production-code` — implement AI-assisted production changes with risk-tiered code reading, independent evidence, runtime QA, and explicit proof boundaries
- `graph-engineering` — design auditable agent execution topologies with explicit routing, ownership, and verification
- `pplx-cli`
- `exa-search`
- `aviation-grade-engineering` — apply aviation-grade engineering rigor: risk-driven lifecycle, multi-layer test defense, SRE observability, resilience patterns, CI/CD quality gates, and blameless postmortems
- `engineering-work-system` — cross-domain workflow router and engineering-health assessor; focused tasks go directly to their specialist Skill
