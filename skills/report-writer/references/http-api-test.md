# HTTP API Test Report Module

Use this module when an AI tests project endpoints or reports HTTP API verification. The testing or
verification owner executes requests and owns assertions; `report-writer` preserves the complete
applicable case inventory, interaction evidence, and presentation artifact.

## Completion contract

Do not summarize an API test as only passed or failed. The handoff must include:

- target environment, base URL classification without secrets, build/revision, API version, time,
  client/tool version, and authorization role;
- an inventory of every applicable test case with executed, passed, failed, blocked, or skipped
  state and a reason for every non-executed case;
- sanitized request and response evidence for every executed case;
- explicit assertions, observed side effects, cleanup/recovery, and artifact references;
- known coverage exclusions, destructive-call boundaries, unavailable dependencies, and human
  gates.

"Complete" means all cases required by the endpoint contract and risk model have an explicit state.
It does not mean blindly executing destructive, production-mutating, rate-limit, concurrency, or
fault-injection cases without authorization.

## Applicable test-case matrix

Select every relevant category and mark non-applicable categories explicitly:

| Category | Examples |
|---|---|
| Success | canonical request, alternate valid representation, documented optional fields |
| Validation | missing required values, null/empty, malformed type/format, bounds, unknown fields |
| Authentication | missing, expired, malformed, or invalid credentials using safe fixtures |
| Authorization | allowed and denied roles/tenants; ownership and object-level access |
| Resource state | not found, conflict, duplicate, stale version, invalid transition |
| Idempotency | repeated request, same/different idempotency key, retry after uncertain response |
| Query behavior | filtering, sorting, pagination, empty result, page boundaries |
| Protocol | method, content type, accept negotiation, encoding, status and header contract |
| Error contract | stable error code, message shape, correlation ID, no sensitive leakage |
| Dependency behavior | authorized timeout, retry, partial failure, unavailable dependency |
| Limits | payload size, rate limit, batch limit, safe concurrency when authorized |
| Side effects | persistence, emitted events, external calls, rollback, cleanup, audit trail |

Derive expected results from API specifications, requirements, fixtures, or another trusted source,
not from the implementation response alone.

## Test-case manifest

Keep a machine-readable YAML or JSON manifest when cases will be rerun. Present the report summary
with:

```markdown
| Case ID | Category | Method/path | Preconditions/role | Request fixture | Expected status/assertions | Side-effect expectation | Result | Interaction artifact |
|---|---|---|---|---|---|---|---|---|
```

Each case must identify request data by a sanitized inline value or fixture/artifact path. Record
schema, business-rule, header, state, and side-effect assertions separately when they differ.

## HTTP interaction evidence

Use UTF-8 JSONL as the canonical execution log, with at least one request event and one response or
transport-error event per executed case. Use the shared log fields plus:

```json
{"ts":"2026-08-07T18:00:00+08:00","level":"info","source":"api-test-client","event":"http.request","target":"https://api.example.test/v1/orders","case_id":"AUTH-001","correlation_id":"api-run-123","method":"POST","url":"https://api.example.test/v1/orders","headers":{"content-type":"application/json","authorization":"[REDACTED]"},"body_artifact":"artifacts/AUTH-001-request.json","body_sha256":"...","body_bytes":128,"timeout_ms":5000,"redactions":["authorization"]}
{"ts":"2026-08-07T18:00:00+08:00","level":"info","source":"api-test-client","event":"http.response","target":"https://api.example.test/v1/orders","case_id":"AUTH-001","correlation_id":"api-run-123","status":"passed","http_status":201,"headers":{"content-type":"application/json","x-request-id":"req-123"},"body_artifact":"artifacts/AUTH-001-response.json","body_sha256":"...","body_bytes":256,"duration_ms":143,"assertion_status":"passed","redactions":[]}
```

Use `http_status` for the numeric HTTP response code; reserve shared `status` for the execution or
evidence state. For transport failures, record DNS/connect/TLS/timeout classification and observed
duration without inventing an HTTP status. Preserve a sanitized HAR 1.2 artifact when browser/proxy-level timing or
redirect detail matters. Preserve bounded raw client output as `.log` only when it adds evidence.
JSONL remains the canonical event index linking cases to artifacts.

## Redaction and body handling

- Redact `Authorization`, cookies, API keys, session identifiers, signatures, secrets, and personal
  or regulated fields before persistence or report inclusion.
- Prefer a header allowlist; do not dump every request or response header by default.
- Store large bodies as separate sanitized artifacts with byte size and SHA-256; embed only bounded
  excerpts needed for assertions.
- Record truncation, filtering, sampling, and redaction categories without storing removed values.
- Use non-production fixtures and safe accounts. Never log reusable credentials.

## Reproduction and result reporting

Provide a sanitized reproduction command or client fixture for failed cases when safe. Never place a
token on a command line. Report:

```markdown
## API test summary

| Endpoint | Cases | Passed | Failed | Blocked | Skipped | Evidence state |
|---|---:|---:|---:|---:|---:|---|

## HTTP interactions

| Case ID | Request | Response/error | Duration | Assertions | Request ID/trace | JSONL/HAR/body artifacts |
|---|---|---|---:|---|---|---|

## Coverage gaps and safety boundaries

| Case/category | State | Reason | Authority or prerequisite required |
|---|---|---|---|
```

For a small repository-native run, use Markdown plus adjacent JSONL/body artifacts. Use a spreadsheet
for a large rerunnable case register, HTML for interactive request/response exploration, and PDF for
a fixed formal assessment; always retain canonical JSONL and sanitized body artifacts separately.
