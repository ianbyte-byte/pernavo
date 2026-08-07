---
name: sonarqube-review
description: >
  Inspect an existing SonarQube project, quality gate, measures, and issues through exposed MCP
  tools or the bundled read-only Web API client. Use when the user says use SonarQube, Sonar review,
  SonarQube audit, quality gate, sonar issues, 使用 SonarQube, or requests SonarQube evidence during
  an MR/PR review. Do not trigger for generic diff review, installing SonarQube, changing server
  configuration, or running a new scanner analysis unless explicitly requested.
---

# SonarQube Review

Produce a bounded, read-only review of analysis that already exists in SonarQube. Do not spend a
general repository-discovery pass rediscovering a named tool request.

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

Never claim a current-branch review from main-branch or stale analysis. A green quality gate is one
evidence source, not proof that the diff is correct. Keep SonarQube findings separate from human or
specialist diff findings; when both are requested, compose with `review-mr` and label the sources.

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
| Branch absent | Fall back only with explicit user approval; otherwise stop at project evidence |
| MCP unavailable | Use the bundled API client when authorized; label the path `web-api` |
| Partial endpoint failure | Preserve successful evidence, list failed queries, and mark the review partial |

Do not change issues, quality gates, permissions, projects, tokens, server settings, or source code.
Do not approve, merge, push, or publish.
