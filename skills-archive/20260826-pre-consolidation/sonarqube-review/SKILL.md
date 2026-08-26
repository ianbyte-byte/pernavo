---
name: sonarqube-review
description: >
  Inspect an existing SonarQube project, quality gate, measures, and issues through exposed MCP
  tools or the bundled read-only Web API client. Always use during a code, MR, PR, diff, or project
  review, even when no SonarQube configuration signal is initially visible; an unavailable result
  is evidence that must be reported, not a reason to silently skip the attempt. Also use when the
  user names SonarQube or requests quality evidence. Do not trigger for non-review code explanation,
  installing SonarQube, changing server configuration, or implicitly running a new scanner analysis.
---

# SonarQube Review

## Query and evidence boundaries

- Perform a bounded preflight and record URL resolution, project-key match, branch, reachability, freshness, and unavailable reasons without printing or requesting token values.
- Keep SonarQube gate, measures, and issues separate from specialist findings and deterministic checks. Baseline-only or unavailable results are not current-branch approval.
- Query existing analysis only; do not run a scanner, change server configuration, mutate project data, or block the remaining review when this evidence channel is unavailable.

Produce a bounded, read-only review of analysis that already exists in SonarQube. Do not spend a
general repository-discovery pass rediscovering a named tool request.

## Proactive evidence routing

Treat SonarQube as a mandatory static-analysis evidence channel during every code review, not as an
opt-in tool that must be named by the user. Before specialist review, always perform a cheap,
bounded preflight. Resolve the target more quickly when any of these signals is already visible:

- `sonar-project.properties` or another inspected project file declares a SonarQube project key;
- `SONARQUBE_URL`, `SONAR_HOST_URL`, or `SONARQUBE_TOKEN` is present (check presence only; never
  print a token value);
- relevant SonarQube MCP tools are exposed in the active session; or
- repository instructions or an earlier verified lookup in the same task identify an existing
  SonarQube project.

Do not require the user to say "use SonarQube". Route the read-only preflight automatically and
compose it with `review-mr`. If no signal exists, still load this skill and record the attempted
default resolution path, but do not perform broad server discovery. If credentials, reachability,
or the project are unavailable, record SonarQube as an attempted but unavailable evidence source;
do not block the remaining review and do not ask the user for the secret value in chat.

## Companion review channels

SonarQube must not run as the only review channel. For MR, PR, and diff review, compose with
`review-mr`. For a broader codebase or project review outside a bounded diff, also invoke the
available general code-review tool, reviewers appropriate to the inspected domains and risks, and
safe existing repository checks such as tests, linters, and type checks. Keep each source labeled.
If a companion tool is unavailable, mark that channel degraded rather than silently omitting it.
No single green tool result constitutes approval.

When a report is requested, hand the collected SonarQube evidence and freshness boundary to
[report-writer](../report-writer/SKILL.md) and select its engineering review module. Keep SonarQube
as a labeled source; the writer must not reinterpret baseline-only or unavailable evidence.

## Resolve the target first

Collect only the inputs that change the query:

1. SonarQube URL: explicit user value, then `SONARQUBE_URL`, then `SONAR_HOST_URL`, then
   `http://localhost:9000`.
2. Project key: a value explicitly labeled as the SonarQube project key, then `sonar.projectKey`
   in `sonar-project.properties`. Treat a repository or product name such as `hxycwms` only as an
   exact-match discovery hint, not as a proven key.
3. Branch or pull request: explicit user value, then the current Git branch when branch evidence is
   requested. Never assume the server contains that branch.
4. Token: read only the environment-variable name `SONARQUBE_TOKEN` by default. Never print, store,
   pass on a command line, or request the token value in chat.

If the project key is still unknown, pass the target name with `--project-name` and use the API
client's bounded project search only when network access is authorized. Match an exact key first,
then an exact case-insensitive project name. If the result is empty or ambiguous, stop and report
the URL, attempted match, and the missing project key.
Do not compensate by recursively browsing unrelated repository history or modules.

## Choose one query path

Prefer SonarQube MCP only when the active session actually exposes relevant SonarQube tools. Tool
configuration, an installed image, or a running container is not tool exposure. Query the resolved
project directly; do not begin with an unfiltered global project listing when a key is available.

When MCP tools are absent, use the bundled standard-library client:

```bash
python3 scripts/sonarqube_review.py review \
  --url http://localhost:9000 \
  --project-key my-project \
  --token-env SONARQUBE_TOKEN \
  --allow-network \
  --json
```

Resolve `scripts/sonarqube_review.py` relative to this `SKILL.md`. The client performs GET requests
only, accepts local URLs by default, requires `--allow-remote` for remote hosts, bounds pagination,
and never emits the token. Do not install a CLI, start or pull a container, edit host configuration,
or run a scanner as an implicit fallback.

Use `preflight` when prerequisites are uncertain:

```bash
python3 scripts/sonarqube_review.py preflight \
  --url http://localhost:9000 \
  --project-key my-project \
  --token-env SONARQUBE_TOKEN \
  --allow-network \
  --json
```

## Interpret evidence conservatively

Keep these states distinct:

1. `configured`: URL, project key, and credential source are known.
2. `reachable`: the server answered the system-status query.
3. `authenticated`: an authenticated project query succeeded.
4. `project-resolved`: the exact project key exists.
5. `analysis-observed`: quality gate, measures, or issues were returned for the requested target.
6. `target-current`: the observed analysis revision and branch match the intended Git target.

Never claim a current-branch review from main-branch or stale analysis. When the requested branch is
absent but the project default branch has existing analysis, it may be queried read-only as
`baseline-only` evidence without another user prompt. Label its branch, revision, and date and state
that it does not cover the current diff. A green quality gate is one evidence source, not proof that
the diff is correct. Keep SonarQube findings separate from human or specialist diff findings; during
code review, compose with `review-mr` and label the sources.

## Output contract

Return:

```markdown
# SonarQube Review

- Target: <url> / <project-key> / <branch-or-default>
- Evidence state: <highest state reached>
- Quality gate: <status or unavailable>
- Analysis: <revision/date when returned>
- Issues: blocker <n>, critical <n>, major <n>, minor <n>, info <n>
- Key measures: bugs, vulnerabilities, code smells, coverage, duplications

## Findings
1. [severity] <component>:<line> - <message> (`<rule>`)

## Evidence boundary
- Observed: <queries that completed>
- Unverified: <branch freshness, scanner execution, unavailable endpoints, or omitted pages>
- Next action: <one concrete command or required input>
```

Order findings by severity, then file and line. Report an empty issue result as “0 issues returned
for this query,” not “the code has no defects.”

## Failure handling

| Failure | Action |
|---------|--------|
| Token missing | Stop before network access and name the required environment variable |
| Server unreachable | Report the URL and connection error; do not search unrelated projects |
| HTTP 401/403 | Report authentication/authorization failure without echoing credentials |
| Project absent | Report the exact attempted key and bounded discovery result |
| Branch absent | During review composition, query the default branch only as labeled `baseline-only` evidence; otherwise stop at project evidence |
| MCP unavailable | Use the bundled API client when authorized; label the path `web-api` |
| Partial endpoint failure | Preserve successful evidence, list failed queries, and mark the review partial |

Do not change issues, quality gates, permissions, projects, tokens, server settings, or source code.
Do not approve, merge, push, or publish.
