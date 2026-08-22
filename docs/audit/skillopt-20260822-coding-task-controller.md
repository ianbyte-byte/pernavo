# SkillOpt Iteration - coding-task-controller

- SkillOpt source: `microsoft/skillopt` at `bdfdc30a8e17309c06cdbe8449f01bdecc120203`
- Target: `skills/coding-task-controller/SKILL.md`
- Fixture: `tests/skillopt/coding-task-controller-tasks.json`

## Scope resolution

The user clarified that `undefined-xxx` meant the repository skill
`skills/unknowns-field-guide`. The earlier placeholder interpretation is superseded; this skill is
now optimized and has its own fixture and evidence record.

## Retained candidate

The controller now has an explicit decision and handoff contract for `fast`/`fast-local`,
`default`/`default-standard`, `deep`, and `analysis-only`. It records authority boundaries and
routes artifacts to their owners without pausing for ordinary internal handoffs. Local
implementation authority is explicitly separated from production data, deployment, publication,
and unrelated external actions.

## Gate evidence

Six reviewed real-language tasks were split into 3 train, 2 validation, and 1 test cases. All six
retained observable responses scored `1.0` hard and `1.000` soft under the local SkillOpt rule
judge. The fixture uses positive output checks and does not treat lexical absence as behavior proof.

No production change, deployment, external write, or approval was performed. This is a governance
prompt iteration, not proof of runtime host trigger behavior.
