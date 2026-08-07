#!/usr/bin/env python3
"""Plan local SonarQube CLI/MCP integration without persisting credentials."""

import argparse
import base64
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen


SCHEMA_VERSION = 1
ENVIRONMENT_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", "host.docker.internal"}


class SonarQubeError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def emit(value: Mapping[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def validate_env_name(value: str) -> str:
    if not ENVIRONMENT_NAME.fullmatch(value):
        raise SonarQubeError("invalid_environment", "token environment variable name is invalid")
    return value


def normalize_url(value: str, allow_remote: bool) -> str:
    parsed = urlsplit(value)
    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise SonarQubeError("invalid_url", "SonarQube URL must be HTTP(S) without embedded credentials")
    if not allow_remote and parsed.hostname.casefold() not in LOCAL_HOSTS:
        raise SonarQubeError("remote_url_gate", "non-local SonarQube URL requires --allow-remote")
    return value.rstrip("/")


def authorization_header(token: str) -> str:
    encoded = base64.b64encode((token + ":").encode("utf-8")).decode("ascii")
    return "Basic " + encoded


def fetch(url: str, token: Optional[str], timeout: int) -> Tuple[int, bytes, str]:
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = authorization_header(token)
    request = Request(url, headers=headers, method="GET")
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status, response.read(1024 * 1024), response.headers.get("Content-Type", "")
    except HTTPError as error:
        raise SonarQubeError("http_error", "SonarQube returned HTTP " + str(error.code)) from error
    except URLError as error:
        raise SonarQubeError("connection_error", "could not connect to SonarQube: " + str(error.reason)) from error


def probe(arguments: argparse.Namespace) -> Dict[str, Any]:
    if not arguments.allow_network:
        raise SonarQubeError("network_gate", "probe requires --allow-network")
    if arguments.timeout < 1 or arguments.timeout > 60:
        raise SonarQubeError("invalid_timeout", "timeout must be between 1 and 60 seconds")
    base_url = normalize_url(arguments.url, arguments.allow_remote)
    token_env = validate_env_name(arguments.token_env)
    token = os.environ.get(token_env)
    status_code, status_body, _ = fetch(base_url + "/api/system/status", token, arguments.timeout)
    version_code, version_body, _ = fetch(base_url + "/api/server/version", token, arguments.timeout)
    try:
        status_data = json.loads(status_body.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise SonarQubeError("invalid_response", "system status response was not valid JSON") from error
    version = version_body.decode("utf-8", errors="replace").strip()
    return {
        "schema_version": SCHEMA_VERSION,
        "command": "probe",
        "valid": True,
        "url": base_url,
        "local": urlsplit(base_url).hostname.casefold() in LOCAL_HOSTS,
        "authentication": {"token_env": token_env, "present": bool(token), "token_type_required": "USER"},
        "service": {
            "status_http": status_code,
            "status": status_data.get("status") if isinstance(status_data, dict) else None,
            "server_id": status_data.get("id") if isinstance(status_data, dict) else None,
            "version_http": version_code,
            "version": version,
        },
        "proof_boundary": "connectivity and SonarQube system identity only; project analysis and quality gates were not executed",
    }


def docker_server_url(base_url: str) -> Tuple[str, bool]:
    parsed = urlsplit(base_url)
    if parsed.hostname.casefold() not in {"localhost", "127.0.0.1", "::1"}:
        return base_url, False
    port = (":" + str(parsed.port)) if parsed.port else ""
    converted = urlunsplit((parsed.scheme, "host.docker.internal" + port, parsed.path, parsed.query, parsed.fragment))
    return converted, True


def json_mcp_config(args: Sequence[str], environment: Mapping[str, str]) -> Dict[str, Any]:
    return {
        "mcpServers": {
            "sonarqube": {
                "command": "docker",
                "args": list(args),
                "env": dict(environment),
            }
        }
    }


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def codex_mcp_config(args: Sequence[str], environment: Mapping[str, str]) -> str:
    args_text = ", ".join(toml_string(value) for value in args)
    env_text = ", ".join(
        toml_string(key) + " = " + toml_string(value) for key, value in sorted(environment.items())
    )
    return "\n".join(
        (
            "[mcp_servers.sonarqube]",
            'command = "docker"',
            "args = [" + args_text + "]",
            "env = { " + env_text + " }",
        )
    )


def mcp_config(arguments: argparse.Namespace) -> Dict[str, Any]:
    base_url = normalize_url(arguments.url, arguments.allow_remote)
    token_env = "SONARQUBE_TOKEN"
    workspace = Path(arguments.workspace).expanduser().resolve()
    if not workspace.is_dir():
        raise SonarQubeError("invalid_workspace", "workspace must be an existing directory")
    if arguments.image.startswith("-") or any(character.isspace() for character in arguments.image):
        raise SonarQubeError("invalid_image", "container image must not start with '-' or contain whitespace")
    container_url, host_rewrite = docker_server_url(base_url)
    docker_args = ["run", "--init", "-i", "--rm"]
    if host_rewrite:
        docker_args += ["--add-host", "host.docker.internal:host-gateway"]
    docker_args += [
        "-e",
        "SONARQUBE_TOKEN",
        "-e",
        "SONARQUBE_URL",
        "-e",
        "SONARQUBE_TOOLSETS",
        "-e",
        "SONARQUBE_READ_ONLY",
        "-v",
        str(workspace) + ":/app/mcp-workspace:ro",
        arguments.image,
    ]
    environment = {
        "SONARQUBE_URL": container_url,
        "SONARQUBE_TOOLSETS": arguments.toolsets,
        "SONARQUBE_READ_ONLY": "true",
    }
    if arguments.project_key:
        environment["SONARQUBE_PROJECT_KEY"] = arguments.project_key
        image_index = docker_args.index(arguments.image)
        docker_args[image_index:image_index] = ["-e", "SONARQUBE_PROJECT_KEY"]
    config: Any = (
        codex_mcp_config(docker_args, environment)
        if arguments.client == "codex"
        else json_mcp_config(docker_args, environment)
    )
    image_unpinned = ":" not in arguments.image or arguments.image.endswith(":latest")
    return {
        "schema_version": SCHEMA_VERSION,
        "command": "mcp-config",
        "valid": True,
        "client": arguments.client,
        "transport": "stdio",
        "runtime": {"name": "docker", "executable": shutil.which("docker"), "image": arguments.image},
        "server": {"requested_url": base_url, "container_url": container_url, "localhost_rewritten": host_rewrite},
        "workspace": {"host_path": str(workspace), "container_path": "/app/mcp-workspace", "read_only": True},
        "authentication": {
            "required_host_environment": token_env,
            "present": bool(os.environ.get(token_env)),
            "container_environment": "SONARQUBE_TOKEN",
            "token_type_required": "USER",
            "persisted_in_config": False,
        },
        "configuration": config,
        "warnings": (["container image is not version-pinned"] if image_unpinned else []),
        "proof_boundary": "configuration generated only; Docker image, MCP handshake, SonarQube authentication, and tool calls were not executed",
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="sonarqube-local", description="Local SonarQube CLI and MCP helper")
    commands = root.add_subparsers(dest="command", required=True)
    probe_parser = commands.add_parser("probe", help="probe a local SonarQube Server")
    probe_parser.add_argument("--url", default="http://localhost:9000")
    probe_parser.add_argument("--token-env", default="SONARQUBE_TOKEN")
    probe_parser.add_argument("--timeout", type=int, default=10)
    probe_parser.add_argument("--allow-network", action="store_true")
    probe_parser.add_argument("--allow-remote", action="store_true")
    probe_parser.add_argument("--json", action="store_true")
    config_parser = commands.add_parser("mcp-config", help="generate a secret-free stdio MCP configuration")
    config_parser.add_argument("--client", choices=("codex", "json"), default="codex")
    config_parser.add_argument("--url", default="http://localhost:9000")
    config_parser.add_argument("--project-key")
    config_parser.add_argument("--workspace", required=True)
    config_parser.add_argument("--toolsets", default="analysis,issues,quality-gates")
    config_parser.add_argument("--image", default="mcp/sonarqube")
    config_parser.add_argument("--allow-remote", action="store_true")
    config_parser.add_argument("--json", action="store_true")
    return root


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        result = probe(arguments) if arguments.command == "probe" else mcp_config(arguments)
        emit(result)
        return 0
    except SonarQubeError as error:
        emit(
            {
                "schema_version": SCHEMA_VERSION,
                "command": arguments.command,
                "valid": False,
                "error": {"code": error.code, "message": error.message},
            }
        )
        return 2


if __name__ == "__main__":
    sys.exit(main())
