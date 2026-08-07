# Harness-Informed Knowledge Principles

Primary source: OpenAI, [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/), published February 11, 2026.

Use the source as an experience report and design input, not a universal benchmark or proof that the
same repository structure, merge policy, or autonomy level is correct elsewhere.

## Principles used by this Skill

1. **Map before manual.** A small stable entry point should direct an agent to relevant deeper
   sources. Loading every rule for every task wastes context and hides priority.
2. **Repository knowledge as execution context.** Knowledge required for coding-agent work should be
   repository-local and versioned when ownership, confidentiality, and the true authoritative source
   allow it.
3. **Progressive disclosure.** Index design, product, plans, generated references, quality,
   reliability, and security material so a task loads only the context it needs.
4. **Plans and debt are knowledge.** Preserve active/completed plans, decision logs, and known debt as
   distinct versioned artifacts rather than relying on conversation history.
5. **Mechanical verification.** Prefer deterministic checks for structure, links, freshness, and
   generated artifacts. Give remediation guidance when a check fails.
6. **Recurring small gardening.** Detect drift frequently and propose targeted corrections that are
   cheap to inspect and reverse. A scheduler and pull-request runtime are separate capabilities from
   this assessment Skill.
7. **Promote repeated prose into controls.** When documentation repeatedly fails to preserve a
   critical invariant, encode it in a lint, test, schema, permission, or tool where feasible.

## Adaptation limits

- Do not impose the source article's example directory tree on a repository with a working knowledge
  system.
- Do not treat roughly 100 lines as a universal `AGENTS.md` limit; evaluate navigation depth, signal,
  duplication, and verification instead.
- Do not infer that agent-generated documentation is correct without an independent oracle.
- Do not weaken merge, security, data, or release gates merely because corrections may be cheap in a
  different environment.
- Do not copy external knowledge into the repository when the external system is authoritative,
  sensitive, licensed, or governed by a separate retention policy; store a discoverable reference.
