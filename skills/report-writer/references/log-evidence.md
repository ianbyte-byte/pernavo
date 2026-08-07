# Log Evidence Module

Use this module whenever a report cites command output, runtime logs, audit events, agent/tool
execution, traces, or other chronological evidence. Keep canonical log artifacts separate from the
presentation report.

## Canonical formats

| Log purpose | Canonical format | Rule |
|---|---|---|
| Machine, agent, tool, audit, or workflow events | UTF-8 JSONL / NDJSON (`.jsonl`) | One complete JSON object per line; append-only when practical |
| Raw stdout or stderr | UTF-8 plain text (`.log`) | Preserve byte/order semantics as closely as possible; do not rewrite into prose |
| Metrics exchanged for analysis | CSV or Parquet when appropriate | Derived data, not a substitute for the canonical event log |
| Human-readable report summary | Markdown/HTML table | Include bounded summaries and links, never the only copy of raw logs |

Do not use Excel, PDF, Word, or slides as the sole source of truth for raw logs. Those artifacts may
contain derived summaries or bounded excerpts.

## JSONL event contract

Prefer these fields; omit genuinely unavailable optional fields instead of fabricating values:

```json
{"ts":"2026-08-07T17:30:00+08:00","level":"info","source":"pytest","event":"command.completed","target":"tests/test_report.py","correlation_id":"review-123","status":"passed","exit_code":0,"duration_ms":412,"artifact":"artifacts/test.log","redactions":[]}
```

| Field | Required | Meaning |
|---|---|---|
| `ts` | yes | ISO 8601 timestamp with timezone |
| `level` | yes | `debug`, `info`, `warning`, `error`, or documented domain level |
| `source` | yes | Tool, service, agent, process, or component that emitted the event |
| `event` | yes | Stable event name such as `command.started` or `command.completed` |
| `target` | when applicable | File, endpoint, environment, task, or entity acted on |
| `correlation_id` | when available | Connects events belonging to one command, request, review, or workflow |
| `status` | when applicable | Observed state such as `passed`, `failed`, `partial`, or `blocked` |
| `exit_code` | command events | Actual process exit code; never infer from surrounding output |
| `duration_ms` | when measured | Observed duration in milliseconds |
| `artifact` | when persisted | Relative or absolute artifact path/identifier without embedded secrets |
| `redactions` | when redacted | Categories removed, never the removed secret values |

Keep event names stable and put variable details in fields. Do not log credentials, authorization
headers, tokens, private keys, raw personal data, or secrets. Record that redaction occurred.

## Report inclusion

In Markdown, summarize logs as:

```markdown
| Source | Time range | Events/lines | Key result | Artifact | Integrity/redaction |
|---|---|---:|---|---|---|
```

Include at most the bounded excerpt needed to support a claim and identify its source line/event.
For HTML, place excerpts in `<details><summary>...</summary><pre><code>...</code></pre></details>` and
escape the content. For PDF, Word, slides, and spreadsheets, include summaries and artifact
references; keep full canonical logs as `.jsonl` or `.log` attachments or adjacent artifacts.

## Integrity and boundaries

- Record path or artifact ID, producer, time range, byte size, and SHA-256 when integrity matters.
- Distinguish complete logs from sampled, truncated, filtered, or redacted logs.
- Bound command output and document omitted line/event counts when known.
- Preserve timezone and clock-source uncertainty for cross-system timelines.
- A log proves only the events it contains; absence of an event is not proof that an action did not
  occur unless logging completeness is independently established.

