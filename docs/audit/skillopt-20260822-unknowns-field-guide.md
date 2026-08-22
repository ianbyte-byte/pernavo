# SkillOpt Iteration - unknowns-field-guide

- SkillOpt source: `microsoft/skillopt` at `bdfdc30a8e17309c06cdbe8449f01bdecc120203`
- Target: `skills/unknowns-field-guide/SKILL.md`
- Fixture: `tests/skillopt/unknowns-field-guide-tasks.json`

## Scope resolution

The user clarified that the earlier `undefined-xxx` name referred to
`skills/unknowns-field-guide`. No placeholder skill was created.

## Retained candidate

The skill now requires explicit handling of unavailable tenant, environment, dependency-owner, and
runtime context; all four Known/Unknown classifications; a P0 threshold tied to behavior or data
safety; reverse-interview questions with why/default/risk; and a complete handoff to
`plan-code-change` without turning discovery into planning or implementation.

## Gate evidence

Six reviewed real-language tasks were split into 3 train, 2 validation, and 1 test cases. All six
retained observable responses scored `1.0` hard and `1.000` soft under the local SkillOpt rule
judge. Checks use positive observable outputs rather than lexical absence as behavior evidence.

No production change, runtime operation, external write, or deployment was performed. This is a
prompt-level iteration, not proof of runtime host trigger behavior.
