# Engineering Review Report Module

Use this module for code, MR, PR, diff, codebase, SonarQube, security, QA, audit, or verification
reports. The review and verification Skills own findings and evidence; `report-writer` owns only the
presentation artifact.

## Required engineering fields

- repository, branch, base, revision, change scope, risk level, and review time;
- invoked reviewer and tool channels, including SonarQube state and analysis freshness;
- P1, P2, and P3 findings with file/line, impact, smallest safe fix, source, and status;
- commands or scenarios actually executed with target, exit/result, and artifact;
- unavailable or degraded channels, unverified layers, human gates, and next actions.

## Markdown specialization

Use the shared metadata and source tables from the main Skill, then use:

```markdown
## Review summary

| Priority | Count | Disposition |
|---|---:|---|
| P1 | <n> | <blocking status> |
| P2 | <n> | <follow-up status> |
| P3 | <n> | <advisory status> |

## Review channels

| Channel | Target/revision | State | Key result | Evidence boundary |
|---|---|---|---|---|
| SonarQube | <branch/revision> | <observed / baseline-only / unavailable> | <gate/issues> | <freshness> |
| Specialist review | <diff> | <state> | <reviewers/counts> | <coverage> |
| Tests/lint/typecheck | <target> | <state> | <commands/results> | <unrun layers> |

## Findings

| ID | Priority | Location | Finding | Impact | Smallest safe fix | Source | Status |
|---|---|---|---|---|---|---|---|

## Checks executed

| Check | Command or scenario | Target | Result | Evidence/artifact |
|---|---|---|---|---|

## Degraded and unverified channels

| Channel/layer | State | Reason | Required next evidence |
|---|---|---|---|
```

Never present default-branch or stale SonarQube analysis as current-diff evidence. A green quality
gate, test suite, or reviewer result is one source, not approval.

## Path compatibility

When called by `review-mr`, preserve
`docs/audit/<branch>-<YYYYMMDD>-mr-review.<md|html>`. Use HTML only when the main Skill's complexity
criteria apply. Keep existing report numbering behavior by appending `-2`, `-3`, and so on.

For other engineering-review uses, apply the main format router:

- repository/MR audit trail: Markdown;
- sortable findings register or recurring remediation tracker: spreadsheet;
- signed, printed, customer-facing, or archival assessment: PDF;
- large interactive evidence pack: self-contained HTML;
- collaborative narrative with redlines: Word;
- review readout or steering presentation: slides.
