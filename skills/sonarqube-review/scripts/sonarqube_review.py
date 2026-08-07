#!/usr/bin/env python3
"""Read-only, secret-safe SonarQube review client."""

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen


LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}
SEVERITIES = ("BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO")
METRICS = "bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density"


class ReviewError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def emit(value: Mapping[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def normalize_url(value: str, allow_remote: bool) -> str:
    parsed = urlsplit(value)
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password:
        raise ReviewError("invalid_url", "SonarQube URL must be HTTP(S) without embedded credentials")
    if (parsed.query or parsed.fragment) or (not allow_remote and parsed.hostname.casefold() not in LOCAL_HOSTS):
        code = "remote_url_gate" if parsed.hostname.casefold() not in LOCAL_HOSTS else "invalid_url"
        raise ReviewError(code, "remote SonarQube URL requires --allow-remote" if code == "remote_url_gate" else "SonarQube URL must not contain query or fragment")
    return value.rstrip("/")


def project_key_from_file(workspace: Path) -> Optional[str]:
    path = workspace / "sonar-project.properties"
    if not path.is_file():
        return None
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == "sonar.projectKey" and value.strip():
            return value.strip()
    return None


class Client:
    def __init__(self, base_url: str, token: str, timeout: int) -> None:
        self.base_url = base_url
        self.token = token
        self.timeout = timeout

    def get(self, endpoint: str, parameters: Optional[Mapping[str, Any]] = None) -> Any:
        query = urlencode({key: value for key, value in (parameters or {}).items() if value is not None})
        url = self.base_url + endpoint + (("?" + query) if query else "")
        authorization = base64.b64encode((self.token + ":").encode("utf-8")).decode("ascii")
        request = Request(url, headers={"Accept": "application/json", "Authorization": "Basic " + authorization}, method="GET")
        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = response.read(4 * 1024 * 1024)
        except HTTPError as error:
            code = "authentication_error" if error.code in (401, 403) else "http_error"
            raise ReviewError(code, "SonarQube returned HTTP " + str(error.code) + " for " + endpoint) from error
        except URLError as error:
            raise ReviewError("connection_error", "could not connect to SonarQube: " + str(error.reason)) from error
        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise ReviewError("invalid_response", "SonarQube returned invalid JSON for " + endpoint) from error


def common(arguments: argparse.Namespace) -> Dict[str, Any]:
    if not arguments.allow_network:
        raise ReviewError("network_gate", "SonarQube query requires --allow-network")
    if arguments.timeout < 1 or arguments.timeout > 60:
        raise ReviewError("invalid_timeout", "timeout must be between 1 and 60 seconds")
    base_url = normalize_url(arguments.url, arguments.allow_remote)
    token = os.environ.get(arguments.token_env)
    if not token:
        raise ReviewError("missing_secret", "SonarQube query requires a token in " + arguments.token_env)
    workspace = Path(arguments.workspace).expanduser().resolve()
    project_key = arguments.project_key or project_key_from_file(workspace)
    return {
        "url": base_url,
        "token": token,
        "project_key": project_key,
        "workspace": str(workspace),
        "project_hint": arguments.project_name or workspace.name,
    }


def resolve_project(client: Client, context: Dict[str, Any]) -> Mapping[str, Any]:
    if context["project_key"]:
        response = client.get("/api/components/show", {"component": context["project_key"]})
        component = response.get("component") if isinstance(response, dict) else None
        if not isinstance(component, dict):
            raise ReviewError("project_not_found", "SonarQube did not return project " + context["project_key"])
        return component
    hint = context["project_hint"]
    response = client.get("/api/components/search", {"qualifiers": "TRK", "q": hint, "ps": 100, "p": 1})
    components = response.get("components", []) if isinstance(response, dict) else []
    exact = [
        item for item in components
        if str(item.get("key", "")).casefold() == hint.casefold()
        or str(item.get("name", "")).casefold() == hint.casefold()
    ]
    if len(exact) != 1:
        detail = "no exact match" if not exact else str(len(exact)) + " exact matches"
        raise ReviewError("project_not_found", detail + " for project hint " + hint + "; provide --project-key")
    context["project_key"] = exact[0]["key"]
    return exact[0]


def safe_get(
    client: Client,
    endpoint: str,
    parameters: Mapping[str, Any],
) -> tuple:
    try:
        return client.get(endpoint, parameters), None
    except ReviewError as error:
        return None, {"endpoint": endpoint, "code": error.code, "message": error.message}


def preflight(arguments: argparse.Namespace) -> Dict[str, Any]:
    context = common(arguments)
    client = Client(context["url"], context["token"], arguments.timeout)
    status = client.get("/api/system/status")
    component = resolve_project(client, context)
    return {
        "command": "preflight",
        "valid": True,
        "path": "web-api",
        "target": {"url": context["url"], "project_key": context["project_key"]},
        "authentication": {"token_env": arguments.token_env, "present": True, "token_exposed": False},
        "service": {"status": status.get("status") if isinstance(status, dict) else None},
        "project": component,
        "evidence_state": "project-resolved",
        "proof_boundary": "server reachability, authentication, and exact project resolution only; no quality evidence queried",
    }


def review(arguments: argparse.Namespace) -> Dict[str, Any]:
    context = common(arguments)
    client = Client(context["url"], context["token"], arguments.timeout)
    client.get("/api/system/status")
    component = resolve_project(client, context)
    branch_parameters = {"branch": arguments.branch} if arguments.branch else {}
    gate, gate_error = safe_get(
        client,
        "/api/qualitygates/project_status",
        {"projectKey": context["project_key"], **branch_parameters},
    )
    measures, measures_error = safe_get(
        client,
        "/api/measures/component",
        {"component": context["project_key"], "metricKeys": METRICS, **branch_parameters},
    )
    issues, issues_error = safe_get(
        client,
        "/api/issues/search",
        {
            "componentKeys": context["project_key"],
            "resolved": "false",
            "ps": arguments.page_size,
            "p": 1,
            **branch_parameters,
        },
    )
    analysis, analysis_error = safe_get(
        client,
        "/api/project_analyses/search",
        {"project": context["project_key"], "ps": 1, **branch_parameters},
    )
    issue_list: List[Mapping[str, Any]] = issues.get("issues", []) if isinstance(issues, dict) else []
    counts = {severity.lower(): 0 for severity in SEVERITIES}
    for issue in issue_list:
        severity = str(issue.get("severity", "")).upper()
        if severity in SEVERITIES:
            counts[severity.lower()] += 1
    paging = issues.get("paging", {}) if isinstance(issues, dict) else {}
    total = int(paging.get("total", len(issue_list)))
    errors = [error for error in (gate_error, measures_error, issues_error, analysis_error) if error]
    completed_queries = sum(value is not None for value in (gate, measures, issues, analysis))
    evidence_state = "analysis-observed" if completed_queries else "project-resolved"
    return {
        "command": "review",
        "valid": True,
        "path": "web-api",
        "target": {"url": context["url"], "project_key": context["project_key"], "branch": arguments.branch},
        "authentication": {"token_env": arguments.token_env, "present": True, "token_exposed": False},
        "project": component,
        "quality_gate": gate.get("projectStatus") if isinstance(gate, dict) else None,
        "measures": measures.get("component") if isinstance(measures, dict) else None,
        "analysis": analysis.get("analyses", []) if isinstance(analysis, dict) else None,
        "issues": {"returned": len(issue_list), "total": total, "truncated": total > len(issue_list), "counts": counts, "items": issue_list},
        "partial": bool(errors),
        "errors": errors,
        "evidence_state": evidence_state,
        "proof_boundary": "existing SonarQube analysis queried; scanner execution and Git revision or branch freshness were not independently verified",
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="sonarqube-review")
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("preflight", "review"):
        command = commands.add_parser(name)
        command.add_argument("--url", default=os.environ.get("SONARQUBE_URL") or os.environ.get("SONAR_HOST_URL") or "http://localhost:9000")
        command.add_argument("--project-key")
        command.add_argument("--project-name", help="exact project name or key hint for bounded discovery")
        command.add_argument("--workspace", default=".")
        command.add_argument("--branch")
        command.add_argument("--token-env", default="SONARQUBE_TOKEN")
        command.add_argument("--timeout", type=int, default=10)
        command.add_argument("--allow-network", action="store_true")
        command.add_argument("--allow-remote", action="store_true")
        command.add_argument("--json", action="store_true")
        if name == "review":
            command.add_argument("--page-size", type=int, choices=range(1, 501), default=100)
    return root


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        emit(preflight(arguments) if arguments.command == "preflight" else review(arguments))
        return 0
    except ReviewError as error:
        emit({"command": arguments.command, "valid": False, "error": {"code": error.code, "message": error.message}})
        return 2


if __name__ == "__main__":
    sys.exit(main())
