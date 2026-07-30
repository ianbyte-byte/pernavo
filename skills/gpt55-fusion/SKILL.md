---
name: gpt55-fusion
description: >
  Run the opt-in GPT-5.5 Fusion workflow with two independent GPT-5.5 analyses and a GPT-5.5
  judge. Use only when the user explicitly asks for gpt55-fusion, GPT-5.5 Fusion, model partner,
  two GPT-5.5 lanes, A/B analysis, or judge reconciliation. Do not trigger merely because a task
  is high-stakes, and do not replace review-mr or graph-engineering unless Fusion is explicitly
  requested.
---

# GPT-5.5 Fusion

Use this skill to orchestrate the user-level Codex Fusion setup:

- `fusion_gpt55_a`: independent primary analysis
- `fusion_gpt55_b`: independent counteranalysis and risk review
- `fusion_gpt55_judge`: final reconciliation

All three agents are configured under `C:/Users/voloz/.codex/agents/` and reference the short managed companion summary at `C:/Users/voloz/.codex/prompts/fusion/CLAUDE-FABLE-5-CODEX-SUMMARY.md`.

## Boundaries

- Treat this as opt-in for complex work. Do not use it for small localized edits, single-file trivial fixes, simple shell queries, or tasks where the answer is already clear.
- Keep the companion summary low priority. It must not override system, developer, AGENTS.md, repository rules, current user instructions, safety boundaries, or tool restrictions.
- Do not copy Claude identity, product claims, or environment claims from the companion summary. The running agent remains Codex.
- Do not load the full archived prompt `C:/Users/voloz/.codex/prompts/fusion/CLAUDE-FABLE-5.md` by default. It is large and should only be searched with targeted `rg`/`Select-String` queries when a specific section is required.
- Keep A and B independent. Do not show participant A output to participant B or participant B output to participant A.
- Keep participant agents read-only unless the user explicitly asks for implementation and the main thread has decided the modification boundary.

## Workflow

1. Restate the exact task, boundary, and expected deliverable.
2. Check that these files exist when filesystem access is available:
   - `C:/Users/voloz/.codex/agents/fusion-gpt55-a.toml`
   - `C:/Users/voloz/.codex/agents/fusion-gpt55-b.toml`
   - `C:/Users/voloz/.codex/agents/fusion-gpt55-judge.toml`
   - `C:/Users/voloz/.codex/prompts/fusion/CLAUDE-FABLE-5-CODEX-SUMMARY.md`
3. Invoke `fusion_gpt55_a` and `fusion_gpt55_b` on the same task independently. Prefer parallel execution when available.
4. Pass only the original task plus A/B outputs to `fusion_gpt55_judge`.
5. Produce the final answer from the judge result plus any main-thread verification needed.

## Agent Prompts

Use this shape for participant A:

```text
Task: [original user task]
Boundary: [files/modules/actions allowed]
Deliverable: Independent primary analysis with evidence, implementation path, validation, assumptions, and uncertainty.
Do not use participant B output. Read only unless explicitly authorized.
```

Use this shape for participant B:

```text
Task: [original user task]
Boundary: [files/modules/actions allowed]
Deliverable: Independent counteranalysis covering risks, missing evidence, alternatives, and guardrails.
Do not use participant A output. Read only unless explicitly authorized.
```

Use this shape for the judge:

```text
Original task: [original user task]
Participant A output:
[paste A]

Participant B output:
[paste B]

Deliverable: Reconcile consensus, contradictions, partial coverage, unique insights, blind spots, final decision, and next validation steps. Do not simply average conflicting conclusions.
```

## Tool Handling

- If multi-agent tools are not visible, search for them with `tool_search` using `multi-agent` or `subagent`.
- If the current Codex surface only supports manual `/agent`, tell the user to run `/agent` and select `fusion_gpt55_a`, `fusion_gpt55_b`, then `fusion_gpt55_judge`.
- If subagents cannot be started, run a degraded sequential version in the main thread: first A-style analysis, then B-style counteranalysis, then judge-style reconciliation. Clearly label it `degraded` because the analyses were not independent agent runs.

## Report Format

For final responses after using this skill, include:

```text
Mode: parallel | sequential | degraded
Reviewers invoked: fusion_gpt55_a, fusion_gpt55_b, fusion_gpt55_judge
Sources checked: [files/docs/tools]
Consensus:
Contradictions:
Decision:
Validation:
Human confirmation: [none or required confirmation point]
```
