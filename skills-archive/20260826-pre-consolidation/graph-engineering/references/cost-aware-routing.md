# Cost-Aware Routing

Use this reference when an engineering workflow may delegate work. It is a portable runtime policy,
not a vendor configuration or an execution guarantee. It does not change a read-only simulator into
an executor, grant tools or permissions, or prove that a host supports child agents.

## Choose the cheapest reliable capability tier

Select by the node's required evidence, permissions, and consequence—not by a provider, model, or
marketing label. Record the selected tier and the reason code in the root packet.

| Tier | Use when | Default topology | Planning ceiling when no stricter host limit exists |
|------|----------|------------------|-----------------------------------------------------|
| `economy` | A localized, reversible task has clear inputs and an objective check | one sequential owner; no child agent | 8k tokens, 15 minutes, 12 tool calls |
| `standard` | A normal retained change needs one bounded fact pass or independent behavior evidence | optional one cheap read-only discovery → one writer → one independent verifier | 32k tokens, 45 minutes, 40 tool calls |
| `deep` | Existing deep-risk triggers or decision-changing uncertainty apply | at most two partitioned read-only investigations → one writer → one independent verifier; add exactly one required review surface | 64k tokens, 90 minutes, 80 tool calls |

These are **planned ceilings**, not observed spend, quality guarantees, permission grants, or billing
estimates. Use host-reported token, elapsed-time, and tool-call counters when available; otherwise
write `observed: unavailable` rather than estimating. Stop or degrade before exceeding a ceiling.
The root may raise a ceiling only with a recorded reason, and must still obey host limits.

## Preflight and topology selection

Use deterministic, additive reason codes. `fast-local` needs no graph. `default-standard` may add
only the preflight codes that are actually observed:

- `unknown-repository-or-api`
- `multi-file-or-dependency`
- `failing-tests`
- `security-data-schema-auth`
- `external-side-effect`
- `ui-runtime-surface`

`deep-risk` adds the applicable existing lifecycle trigger. Promotion to a graph requires a
measurable benefit: two non-overlapping bounded questions with independent inputs, a required
independent verifier, or a real permission/conditional-routing boundary. More agents are allowed
only for such independent bounded nodes. Otherwise keep an economy loop or standard sequence.

Default limits are two active read-only child nodes, child depth one, one shared-tree writer, and
at most two repair rounds. A reviewer is a separate surface from a verifier; do not create a second
reviewer for the same question. Use an adjudicator only for evidence-backed disagreement that would
change the root decision.

If child agents are unavailable, a branch times out, or a host cap is reached, label the route
`degraded-sequential`, run only the remaining authorized work in the root context, and do not claim
parallel or independent execution that did not occur.

## Give nodes compact, safe packets

Every child receives a compact packet, not a transcript:

```text
Objective and success bar:
Reason code and selected tier:
Bounded question or owned artifact:
Allowed and forbidden scope:
Permissions and external-effect boundary:
Evidence inputs and expected output schema:
Planned limits (tokens, wall time, tool calls):
Stop condition and failure route:
```

Before dispatch, remove secrets, credentials, personal data, customer data, and unrelated private
configuration. An external adviser is permitted only after a privacy gate confirms that the packet
is public or safely redacted; otherwise keep the question local or request explicit disclosure
authority. External advice is evidence, not a substitute for the root's inspection.

## One writer, fresh verification, and bounded repair

Choose a writer whose repository familiarity, tools, permissions, and implementation capability
match the approved change. Only that writer edits a shared working tree. The root inspects the
fresh diff before giving it to an independent, risk-proportional verifier. The verifier receives
acceptance criteria and artifact evidence, not an instruction to endorse the writer. Do not duplicate
an already-required reviewer or use a reviewer as a second verifier for the same acceptance claim.

On a verifier failure, return a minimal failure packet and retry only if it contains a new,
testable hypothesis. Do not spend retries on deterministic environment, permission, dependency, or
repeated unchanged failures. Preserve the existing two-round cap unless a stricter task rule applies.

## Reuse and stop early

Reuse or follow up with an agent only when its prior bounded question remains valid and continuation
is cheaper than reorientation. Send a reset packet containing the new objective, changed constraint,
fresh diff or evidence revision, invalidated conclusions, remaining budget, and new stop condition.
Use a fresh agent when isolation or independent judgment matters. Cancel idle branches, branches
whose fan-in input is no longer needed, and all pending branches when the root reaches a stop gate.

The root retains synthesis and final validation. Stop when all applicable gates are satisfied:

1. The delivered result matches authorized intent and the selected reason codes still fit.
2. Required focused checks passed, or a failure/blocker is recorded without a false pass claim.
3. The final diff is in scope and unrelated dirty work remains preserved.
4. Every unverified runtime, deployment, or external surface is explicitly named.
5. No required node, authorized repair, or decision-changing contradiction remains.

Report planned limits separately from observed counters, the topology actually executed, cancelled or
degraded nodes, raw evidence locations, and remaining proof boundaries.
