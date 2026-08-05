# Cost-Aware Multi-Agent Orchestration

**Access date:** 2026-08-05

This note records public primary-source evidence for a portable policy: use the cheapest reliable
capability for a bounded node, add agents only for independent work, retain one writer, and keep the
root accountable for synthesis and final validation. It contains no deployment recipe or provider
configuration.

## Evidence-backed facts

| Source | What it supports |
|--------|------------------|
| [OpenAI Agents SDK: orchestration](https://openai.github.io/openai-agents-python/multi_agent/) | Orchestration can be model-directed or code-directed. The documented manager pattern keeps one agent in control while specialists perform bounded work; code orchestration can chain, evaluate-and-repair, or parallelize independent tasks. |
| [OpenAI: A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | Model choice has quality, latency, and cost tradeoffs; establish an evaluation baseline, then replace capacity with smaller options where results remain acceptable. It recommends maximizing a single agent before introducing multi-agent complexity and overhead. |
| [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model) | Current guidance distinguishes capability/cost roles, recommends intentional reasoning effort, and says quality, completeness, evidence, tokens, latency, and cost should be compared on representative tasks. It also recommends lean prompts and relevant tools. |
| [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Start with the simplest solution and add agentic complexity only when the performance tradeoff justifies its latency and cost. Parallelization is appropriate for independent sectioned tasks or multiple perspectives that are aggregated. |
| [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents) | Subagents can use focused prompts, restricted tools, selectable models, isolated context, and continuation. The documentation also describes background-tool restrictions and a host-defined nesting limit, so a policy must verify host capabilities rather than assume them. |
| [Agent Skills specification](https://agentskills.io/specification) | A Skill is a directory centered on `SKILL.md`; optional `references/` support progressive disclosure, allowing detailed routing policy to stay out of the compact entry instruction. |

## Policy inferences

The following are project policy choices inferred from the evidence above, not claims made verbatim
by any source:

- Select `economy`, `standard`, or `deep` from the evidence and consequence required for a node;
  do not bind the policy to a vendor or a particular model name.
- Use one sequential owner for an economy task. For standard work, use cheap read-only discovery
  only when a deterministic preflight signal is present, then one writer and an independent verifier.
- Permit at most two parallel read-only investigations for deep work, only when their questions have
  independent inputs and a defined fan-in. Keep one writer per shared working tree.
- Set planned token, wall-time, and tool-call ceilings before dispatch; record host-observed spend
  separately. Stop or degrade sequentially when a host cannot provide the planned child topology.
- Send compact, redacted context packets; external advisers receive only public or safely redacted
  material after a privacy gate. The root inspects the resulting artifact and retains final synthesis.
- Repair only from a new, evidence-backed hypothesis. Do not repeatedly retry a deterministic
  environment, permission, or dependency failure.

## What these sources do not support

- They do not prove a particular local host can spawn, resume, constrain, or account for child
  agents; runtime capability must be observed in that host.
- They do not provide a universal token, time, tool-call, or cost budget, nor prove that a lower-cost
  capability will meet a particular acceptance bar. Local representative evaluation is required.
- They do not authorize destructive operations, new permissions, external writes, disclosure of
  sensitive information, releases, or production claims.
- They do not establish that a static Skill policy is executed by a model or that a read-only routing
  simulator is an executor. That requires separate runtime observation.

## Implementation boundary

The linked Skills encode a vendor-neutral routing policy only. They preserve task-specific ownership
of discovery, planning, implementation, verification, and review, and use a focused reference to
avoid duplicating those workflows.
