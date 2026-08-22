# SkillOpt Pilot - database-testing

- SkillOpt source: `microsoft/skillopt` at `bdfdc30a8e17309c06cdbe8449f01bdecc120203`
- Target: `skills/database-testing/SKILL.md`
- Task fixture: `tests/skillopt/database-testing-tasks.json`
- Method: one skill, bounded two-edit candidates, train/validation/test split, held-out gate

## Evidence

The first real-backend baseline used the two validation tasks and scored `0.2875` on the mixed
hard/soft gate. Reflection proposed two bounded edits. An independent candidate check rejected the
first proposal: it scored `0.275` and regressed the performance-review task.

The retained candidate was then checked independently against the same validation prompts. It
produced all required SQL Server safety fields (`preflight`, read-only, `sqlcmd`, credential
redaction, and production boundary), and routed the read-only performance review to
`database-performance` while naming cardinality and query-plan evidence. The fixture uses positive
outcome checks rather than lexical `not_contains` checks, because a safe answer may need to mention
a prohibited command while explaining that it was not executed. Under that corrected judge, the
candidate passed both validation tasks (`2/2` hard, `1.000` soft).

The candidate was applied as two general routing/output rules in the skill. No database connection,
write, credential access, or production target was used. This is a prompt-level pilot, not proof of
all runtime host trigger behavior; the repository's 26-skill/78-case static validator remains the
separate routing gate.
