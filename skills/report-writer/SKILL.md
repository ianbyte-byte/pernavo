---
name: report-writer
description: >
  Turn supplied facts, analysis, findings, metrics, and evidence into a consistent formal report.
  Use whenever the user asks to write, create, generate, format, or persist a report, including
  写报告, 生成报告, 输出报告, 报告格式, or when another Skill must produce a report artifact. Select
  Markdown, spreadsheet, PDF, HTML, Word, or slides from the report's purpose, audience, lifecycle,
  and interaction needs; default to Markdown only when no specialized use applies. Do not collect
  missing evidence, invent conclusions, or replace specialized artifact or domain-analysis tools.
---

# Report Writer

Own report structure, format selection, and presentation after upstream owners supply the content.
Do not invent facts, rerun analysis, silently resolve missing evidence, or turn a report into
approval. A report may present another Skill's work without absorbing that Skill's responsibility.

## Evidence and authority boundaries

- Require a supplied purpose, audience, scope, as-of time, source owners, evidence state, freshness
  boundary, limitations, and accountable authority. Mark missing inputs unavailable; do not infer,
  rerun analysis, or turn presentation into approval.
- Preserve observed, inferred, partial, degraded, unavailable, and unverified states, including
  provenance, dates, revisions, units, and excluded surfaces. A polished format is not evidence.
- Keep findings, interpretation, recommendations, and decisions separate. The report writer owns
  structure and format only; domain skills retain finding ownership and specialized artifact skills
  retain container authority.

## Select the report module

Read only the module that matches the requested report:

- Engineering review, code review, audit, SonarQube, security, QA, or verification report: use
  [engineering review](references/engineering-review.md).
- HTTP API test report, endpoint verification, request/response evidence, or contract-test report:
  use [HTTP API test](references/http-api-test.md) and [log evidence](references/log-evidence.md).
- A report that cites command output, runtime events, audit trails, or agent/tool execution: use
  [log evidence](references/log-evidence.md).
- No matching module: use the general report contract below and label domain-specific sections
  supplied by the caller without inventing a domain template.

Future report types belong in small files under `references/`; keep this entrypoint focused on
routing, format selection, and shared truthfulness rules.

## Required handoff

Collect or mark unavailable:

- report purpose, audience, title, target, scope, as-of time, and requested output path;
- supplied facts, analysis, findings, metrics, decisions, and their owners or sources;
- evidence or data status, provenance, relevant revision/date, and freshness boundary;
- referenced log artifacts, their format, time range, redaction state, and integrity identifier;
- limitations, excluded surfaces, open decisions, actions, and accountable authority;
- requested container such as chat, `.md`, `.html`, Word, PDF, slides, or spreadsheet.

If the requested container has a specialized Skill, use it to create that artifact and apply this
Skill's structure inside it. Formatting ownership never grants authority to query an external
system, modify source data, approve, publish, send, merge, or deploy.

## Choose the file format from the report's use

Honor an explicit file format unless it conflicts with safety or the requested use. Otherwise choose
the primary artifact with this routing table:

| Intended use | Primary format | Route to specialized artifact Skill when available |
|---|---|---|
| Repository-native record, technical review, version control, easy diff | Markdown (`.md`) | No additional container Skill required |
| Tabular detail, formulas, sorting, filtering, pivots, recurring tracking | Spreadsheet (`.xlsx`) | Spreadsheet Skill |
| Formal distribution, printing, sign-off, fixed layout, archival snapshot | PDF (`.pdf`) | PDF Skill |
| Browser reading, interactive filtering, expandable evidence, rich navigation | Self-contained HTML (`.html`) | Build directly under this contract |
| Long narrative, comments, redlines, collaborative editing | Word (`.docx`) | Document Skill |
| Live presentation, executive briefing, speaker-led storytelling | Slides (`.pptx`) | Presentation Skill |

Use Markdown as the fallback when no specialized use applies and it remains readable with at most
eight table columns, twenty primary rows or findings, and short evidence references.

Use self-contained HTML instead of Markdown when browser interaction is part of the intended use or
any condition applies:

- more than twenty primary rows need grouping, filtering, or a table of contents;
- a source-by-target, period-by-segment, or other comparison matrix needs more than eight columns;
- rows need nested evidence, expandable bounded logs, or multiple artifacts;
- four or more evidence channels must be compared across three or more dimensions;
- the Markdown version would repeat large blocks or be materially harder to navigate.

For mixed needs, create one primary artifact and derive secondary artifacts only when requested.
Do not disguise a static table as a spreadsheet, a Markdown printout as a verified PDF, or an HTML
page as a slide deck. State `Format`, `Format reason`, and the specialized artifact Skill used in the
handoff. Do not choose a format merely for decoration.

## General Markdown contract

Use this baseline and adapt section names to the report domain:

```markdown
# <Report title>

| Field | Value |
|---|---|
| Purpose | <decision or reader need> |
| Audience | <audience> |
| Target and scope | <included and excluded> |
| As of | <timestamp and timezone> |
| Overall evidence/data state | <observed / partial / degraded / unavailable> |

## Executive summary

| Topic | Result | Significance | Required action |
|---|---|---|---|

## Inputs and sources

| Source | Owner | Date/revision | State | Boundary |
|---|---|---|---|---|

## Findings or analysis

| ID | Topic/priority | Observation | Evidence | Implication | Recommendation | Status |
|---|---|---|---|---|---|---|

## Metrics or comparisons

| Metric | Current | Baseline/target | Change | Interpretation |
|---|---:|---:|---:|---|

## Limitations and unresolved questions

| Surface | State | Reason | Required next evidence or decision |
|---|---|---|---|

## Actions

| Priority | Action | Owner/authority | Due/trigger | Completion evidence |
|---|---|---|---|---|
```

Omit a section only when it is genuinely not applicable. Use `None observed`, `Not supplied`, or
`Not applicable` rather than ambiguous empty cells. Keep long logs in linked artifacts.

## Self-contained HTML contract

Produce semantic HTML5 with embedded CSS, no network dependency, and:

- title, metadata summary, table of contents, key totals, and a state legend;
- accessible tables with captions, scoped headers, keyboard focus, and sufficient contrast;
- stable fragment identifiers for grouped sections;
- `<details>` for nested evidence and bounded logs;
- print styles and text labels so status is not communicated only through color.

Escape untrusted text, paths, messages, and command output. Do not embed external scripts, fonts,
trackers, remote assets, or executable source data. Optional inline JavaScript may only support
local filtering or sorting; the complete report must remain readable when JavaScript is disabled.

## Truthfulness and safety

- Preserve source attribution, dates, revisions, units, denominators, and excluded scope.
- Distinguish observed, inferred, partial, degraded, unavailable, and unverified states.
- Never convert a missing value to zero or an unavailable check to passed.
- Do not expose secrets, credentials, personal data, or unbounded raw output.
- Separate findings, interpretation, recommendations, and decisions.
- A polished report is not evidence that the underlying work occurred.

## File naming and output

Use the caller's authorized path. If persistence is requested without a path, write under
`docs/reports/` as `<report-type>-<target-slug>-<YYYYMMDD>.<md|xlsx|pdf|html|docx|pptx>`. Avoid
overwriting an existing report; append `-2`, `-3`, and so on.

After writing, return:

```text
Report: <absolute path or chat response>
Format: markdown | spreadsheet | pdf | html | word | slides
Format reason: <default or complexity trigger>
Artifact Skill: <name or not required>
Overall evidence/data state: <state>
Primary rows/findings: <count>
Degraded/unverified inputs: <count and names>
```
