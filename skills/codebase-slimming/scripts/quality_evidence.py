#!/usr/bin/env python3
"""Collect reproducible quality evidence from explicitly selected external tools.

The runner is intentionally dependency-free and never invokes a shell. It does not install tools,
restore dependencies, delete artifacts, or infer that a configured adapter has actually run.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


SCHEMA_VERSION = 1
MAX_METRICS_BYTES = 8 * 1024 * 1024
TOOL_NAMES = (
    "scc",
    "knip",
    "dotnet-packages",
    "dotnet-analyzers",
    "roslyn-analyzers",
    "coverlet",
    "sonarqube",
    "dependency-check",
)


class EvidenceError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def emit(value: Mapping[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_target(path_text: str) -> Path:
    target = Path(path_text).expanduser().resolve()
    if not target.is_dir():
        raise EvidenceError("invalid_target", "target must be an existing directory")
    return target


def project_signals(target: Path) -> Dict[str, bool]:
    ignored = {".git", ".next", "bin", "dist", "node_modules", "obj"}

    def visible_match(patterns: Iterable[str]) -> bool:
        for pattern in patterns:
            for path in target.rglob(pattern):
                if path.is_file() and ignored.isdisjoint(path.relative_to(target).parts):
                    return True
        return False

    def project_text_contains(needle: str) -> bool:
        for pattern in ("*.csproj", "*.fsproj", "*.vbproj", "*.props"):
            for path in target.rglob(pattern):
                if not path.is_file() or not ignored.isdisjoint(path.relative_to(target).parts):
                    continue
                try:
                    if path.stat().st_size <= 1024 * 1024 and needle.casefold() in path.read_text(encoding="utf-8").casefold():
                        return True
                except (OSError, UnicodeError):
                    continue
        return False

    return {
        "has_files": visible_match(("*",)),
        "javascript_typescript": visible_match(("package.json", "tsconfig*.json", "*.js", "*.jsx", "*.ts", "*.tsx")),
        "dotnet": visible_match(("*.sln", "*.slnx", "*.csproj", "*.fsproj", "*.vbproj")),
        "net_analyzers_package": project_text_contains("Microsoft.CodeAnalysis.NetAnalyzers"),
        "coverlet_collector": project_text_contains("coverlet.collector"),
        "coverlet_mtp": project_text_contains("coverlet.MTP"),
        "sonarqube_config": (target / "sonar-project.properties").is_file(),
        "dependency_manifest": visible_match(
            ("package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "*.csproj", "*.fsproj", "packages.lock.json")
        ),
    }


def local_executable(target: Path, name: str) -> Optional[str]:
    local = target / "node_modules" / ".bin" / name
    if local.is_file() and os.access(str(local), os.X_OK):
        return str(local)
    return shutil.which(name)


def resolve_executable(target: Path, tool: str) -> Optional[str]:
    candidates = {
        "scc": ("scc",),
        "knip": ("knip",),
        "dotnet-packages": ("dotnet",),
        "dotnet-analyzers": ("dotnet",),
        "roslyn-analyzers": ("dotnet",),
        "coverlet": ("dotnet",),
        "sonarqube": ("sonar-scanner",),
        "dependency-check": ("dependency-check", "dependency-check.sh"),
    }[tool]
    for candidate in candidates:
        resolved = local_executable(target, candidate) if tool == "knip" else shutil.which(candidate)
        if resolved:
            return resolved
    return None


def applicable(tool: str, signals: Mapping[str, bool]) -> bool:
    if tool == "scc":
        return signals["has_files"]
    if tool == "knip":
        return signals["javascript_typescript"]
    if tool in ("dotnet-packages", "dotnet-analyzers", "roslyn-analyzers"):
        return signals["dotnet"]
    if tool == "coverlet":
        return signals["dotnet"] and (signals["coverlet_collector"] or signals["coverlet_mtp"])
    if tool == "sonarqube":
        return signals["sonarqube_config"]
    return signals["dependency_manifest"]


def gates(tool: str) -> Tuple[str, ...]:
    if tool == "sonarqube":
        return ("allow_network", "allow_worktree_writes")
    if tool in ("coverlet", "dotnet-analyzers", "roslyn-analyzers"):
        return ("allow_worktree_writes",)
    return ()


def tool_inventory(target: Path, signals: Optional[Mapping[str, bool]] = None) -> List[Dict[str, Any]]:
    detected = signals or project_signals(target)
    result = []
    for tool in TOOL_NAMES:
        is_applicable = applicable(tool, detected)
        executable = resolve_executable(target, tool) if is_applicable else None
        state = "available" if executable else ("missing" if is_applicable else "not_applicable")
        result.append(
            {
                "name": tool,
                "applicable": is_applicable,
                "state": state,
                "executable": executable,
                "required_gates": list(gates(tool)),
            }
        )
    return result


def dotnet_major(executable: str, target: Path) -> Optional[int]:
    try:
        process = subprocess.run(
            [executable, "--version"], cwd=str(target), check=False, capture_output=True, text=True, timeout=10
        )
        text = process.stdout.strip()
        return int(text.split(".", 1)[0]) if process.returncode == 0 else None
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


def command_for(
    tool: str,
    executable: str,
    target: Path,
    evidence_dir: Path,
    signals: Optional[Mapping[str, bool]] = None,
) -> List[str]:
    if tool == "scc":
        return [executable, "--format", "json", "--no-cocomo", str(target)]
    if tool == "knip":
        return [executable, "--reporter", "json", "--no-progress"]
    if tool == "dotnet-packages":
        prefix = ["package", "list"] if (dotnet_major(executable, target) or 0) >= 10 else ["list", "package"]
        return [executable] + prefix + ["--include-transitive", "--format", "json", "--no-restore"]
    if tool == "dotnet-analyzers":
        command = [
            executable,
            "build",
            "--no-restore",
            "--configuration",
            "Release",
            "--verbosity",
            "minimal",
            "-p:RunAnalyzers=true",
            "-p:RunAnalyzersDuringBuild=true",
            "-p:AnalysisMode=All",
            "-p:GenerateFullPaths=true",
        ]
        detected = signals or project_signals(target)
        if not detected["net_analyzers_package"]:
            command.append("-p:EnableNETAnalyzers=true")
        return command
    if tool == "roslyn-analyzers":
        return [
            executable,
            "format",
            "analyzers",
            "--no-restore",
            "--verify-no-changes",
            "--severity",
            "info",
            "--report",
            str(evidence_dir / "roslyn-analyzers"),
            "--verbosity",
            "diagnostic",
        ]
    if tool == "coverlet":
        detected = signals or project_signals(target)
        if detected["coverlet_mtp"]:
            return [
                executable,
                "test",
                "--no-restore",
                "--coverlet",
                "--coverlet-output-format",
                "cobertura",
                "--coverlet-output",
                str(evidence_dir / "coverlet" / "coverage"),
            ]
        return [
            executable,
            "test",
            "--no-restore",
            "--collect",
            "XPlat Code Coverage",
            "--results-directory",
            str(evidence_dir / "coverlet"),
        ]
    if tool == "sonarqube":
        return [executable, "-Dsonar.projectBaseDir=" + str(target)]
    return [
        executable,
        "--noupdate",
        "--scan",
        str(target),
        "--format",
        "JSON",
        "--out",
        str(evidence_dir / "dependency-check"),
    ]


def inventory_command(target: Path) -> Dict[str, Any]:
    signals = project_signals(target)
    return {
        "schema_version": SCHEMA_VERSION,
        "command": "inventory",
        "valid": True,
        "target": str(target),
        "signals": signals,
        "tools": tool_inventory(target, signals),
        "proof_boundary": "availability and project signals only; no analyzer was executed",
    }


def ensure_empty_output(path: Path) -> None:
    if path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise EvidenceError("output_not_empty", "evidence directory must be absent or empty")


def validate_run(
    target: Path,
    selected: Sequence[str],
    allow_network: bool,
    allow_worktree_writes: bool,
    signals: Optional[Mapping[str, bool]] = None,
) -> Dict[str, str]:
    tools = {item["name"]: item for item in tool_inventory(target, signals)}
    executables: Dict[str, str] = {}
    for tool in selected:
        item = tools[tool]
        if not item["applicable"]:
            raise EvidenceError("not_applicable", tool + " is not applicable to detected project signals")
        if not item["executable"]:
            raise EvidenceError("tool_missing", tool + " executable was not found; install it outside this runner")
        if "allow_network" in item["required_gates"] and not allow_network:
            raise EvidenceError("network_gate", tool + " requires --allow-network")
        if "allow_worktree_writes" in item["required_gates"] and not allow_worktree_writes:
            raise EvidenceError("worktree_gate", tool + " requires --allow-worktree-writes")
        executables[tool] = item["executable"]
    return executables


def read_json(path: Path) -> Optional[Any]:
    try:
        if path.stat().st_size > MAX_METRICS_BYTES:
            return None
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def number(value: Any) -> Optional[float]:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


DIAGNOSTIC_PATTERN = re.compile(r"\b(?P<severity>warning|error)\s+(?P<identifier>[A-Z]{2,}[0-9]{3,})\s*:", re.IGNORECASE)


def diagnostic_metrics(text: str) -> Dict[str, float]:
    metrics: Dict[str, float] = {}
    seen = set()
    for line in text.splitlines():
        match = DIAGNOSTIC_PATTERN.search(line)
        if match is None or line.strip() in seen:
            continue
        seen.add(line.strip())
        severity = match.group("severity").casefold() + "s"
        identifier = match.group("identifier").upper()
        metrics[severity] = metrics.get(severity, 0.0) + 1
        key = "diagnostic_" + identifier
        metrics[key] = metrics.get(key, 0.0) + 1
    if metrics:
        metrics["diagnostics_total"] = metrics.get("warnings", 0.0) + metrics.get("errors", 0.0)
    return metrics


def roslyn_report_metrics(value: Any, metrics: Dict[str, float]) -> None:
    if isinstance(value, dict):
        identifier = value.get("DiagnosticId") or value.get("diagnosticId")
        if isinstance(identifier, str) and identifier.strip():
            key = "diagnostic_" + identifier.strip().upper()
            metrics[key] = metrics.get(key, 0.0) + 1
            metrics["diagnostics_total"] = metrics.get("diagnostics_total", 0.0) + 1
        for child in value.values():
            roslyn_report_metrics(child, metrics)
    elif isinstance(value, list):
        for child in value:
            roslyn_report_metrics(child, metrics)


def scc_metrics(data: Any) -> Dict[str, float]:
    if not isinstance(data, list):
        return {}
    fields = {"Files": "files", "Lines": "lines", "Code": "code", "Comment": "comments", "Blank": "blanks", "Complexity": "complexity"}
    metrics = {name: 0.0 for name in fields.values()}
    found = False
    for row in data:
        if not isinstance(row, dict):
            continue
        for source, name in fields.items():
            value = number(row.get(source))
            if value is not None:
                metrics[name] += value
                found = True
    return metrics if found else {}


def knip_metrics(data: Any) -> Dict[str, float]:
    if not isinstance(data, dict) or not isinstance(data.get("issues"), list):
        return {}
    metrics: Dict[str, float] = {"issue_files": float(len(data["issues"]))}
    for issue in data["issues"]:
        if not isinstance(issue, dict):
            continue
        for name, entries in issue.items():
            if name not in ("file", "owners") and isinstance(entries, list):
                metrics[name] = metrics.get(name, 0.0) + len(entries)
    metrics["issues_total"] = sum(value for key, value in metrics.items() if key != "issue_files")
    return metrics


def walk_package_metrics(value: Any, metrics: Dict[str, float]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in ("topLevelPackages", "transitivePackages") and isinstance(child, list):
                metric = "top_level_packages" if key == "topLevelPackages" else "transitive_packages"
                metrics[metric] = metrics.get(metric, 0.0) + len(child)
            walk_package_metrics(child, metrics)
    elif isinstance(value, list):
        for child in value:
            walk_package_metrics(child, metrics)


def extract_metrics(tool: str, stdout_path: Path, stderr_path: Optional[Path] = None) -> Dict[str, float]:
    data = read_json(stdout_path)
    if tool == "scc":
        return scc_metrics(data)
    if tool == "knip":
        return knip_metrics(data)
    if tool == "dotnet-packages" and data is not None:
        metrics: Dict[str, float] = {}
        walk_package_metrics(data, metrics)
        return metrics
    if tool == "dotnet-analyzers":
        try:
            output = stdout_path.read_text(encoding="utf-8", errors="replace")
            if stderr_path is not None:
                output += "\n" + stderr_path.read_text(encoding="utf-8", errors="replace")
            return diagnostic_metrics(output[:MAX_METRICS_BYTES])
        except OSError:
            return {}
    return {}


def artifact_root(tool: str, evidence_dir: Path) -> Optional[Path]:
    if tool in ("coverlet", "dependency-check", "roslyn-analyzers"):
        return evidence_dir / tool
    return None


def collect_artifacts(tool: str, evidence_dir: Path) -> List[Dict[str, Any]]:
    root = artifact_root(tool, evidence_dir)
    if root is None or not root.is_dir():
        return []
    artifacts = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        artifacts.append(
            {
                "path": str(path),
                "relative_path": str(path.relative_to(evidence_dir)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return artifacts


def artifact_metrics(tool: str, evidence_dir: Path) -> Dict[str, float]:
    if tool != "roslyn-analyzers":
        return {}
    metrics: Dict[str, float] = {}
    root = artifact_root(tool, evidence_dir)
    if root is None or not root.is_dir():
        return metrics
    for path in sorted(root.rglob("*.json")):
        data = read_json(path)
        if data is not None:
            roslyn_report_metrics(data, metrics)
    return metrics


def probe_version(executable: str, target: Path) -> Dict[str, Any]:
    command = [executable, "--version"]
    try:
        process = subprocess.run(
            command,
            cwd=str(target),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=False,
            timeout=10,
        )
        output = (process.stdout + process.stderr)[:32768].decode("utf-8", errors="replace").strip()
        return {"command": command, "return_code": process.returncode, "output": output}
    except subprocess.TimeoutExpired:
        return {"command": command, "return_code": None, "output": "", "timed_out": True}
    except OSError as error:
        return {"command": command, "return_code": None, "output": str(error), "launch_failed": True}


def run_tool(tool: str, command: Sequence[str], target: Path, evidence_dir: Path, timeout: int) -> Dict[str, Any]:
    stdout_path = evidence_dir / (tool + ".stdout")
    stderr_path = evidence_dir / (tool + ".stderr")
    version_probe = probe_version(command[0], target)
    started_at = utc_now()
    timed_out = False
    return_code: Optional[int]
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        try:
            process = subprocess.run(
                list(command), cwd=str(target), stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, check=False, timeout=timeout
            )
            return_code = process.returncode
        except subprocess.TimeoutExpired:
            return_code = None
            timed_out = True
        except OSError as error:
            stderr.write((str(error) + "\n").encode("utf-8", errors="replace"))
            return_code = None
    metrics = extract_metrics(tool, stdout_path, stderr_path)
    metrics.update(artifact_metrics(tool, evidence_dir))
    return {
        "name": tool,
        "command": list(command),
        "version_probe": version_probe,
        "started_at": started_at,
        "finished_at": utc_now(),
        "return_code": return_code,
        "timed_out": timed_out,
        "status": (
            "timed_out"
            if timed_out
            else ("completed" if return_code == 0 else ("completed_nonzero" if return_code is not None else "launch_failed"))
        ),
        "stdout": {"path": str(stdout_path), "sha256": sha256(stdout_path), "bytes": stdout_path.stat().st_size},
        "stderr": {"path": str(stderr_path), "sha256": sha256(stderr_path), "bytes": stderr_path.stat().st_size},
        "artifacts": collect_artifacts(tool, evidence_dir),
        "metrics": metrics,
    }


def run_command(arguments: argparse.Namespace) -> Tuple[int, Dict[str, Any]]:
    target = resolve_target(arguments.target)
    evidence_dir = Path(arguments.evidence_dir).expanduser().resolve()
    selected = tuple(dict.fromkeys(arguments.tool))
    signals = project_signals(target)
    executables = validate_run(
        target, selected, arguments.allow_network, arguments.allow_worktree_writes, signals
    )
    commands = {
        tool: command_for(tool, executables[tool], target, evidence_dir, signals) for tool in selected
    }
    if arguments.dry_run:
        return 0, {
            "schema_version": SCHEMA_VERSION,
            "command": "run",
            "valid": True,
            "dry_run": True,
            "target": str(target),
            "evidence_dir": str(evidence_dir),
            "tools": [{"name": tool, "command": commands[tool], "required_gates": list(gates(tool))} for tool in selected],
            "proof_boundary": "commands planned only; no analyzer was executed and no evidence directory was written",
        }
    ensure_empty_output(evidence_dir)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    results = [run_tool(tool, commands[tool], target, evidence_dir, arguments.timeout) for tool in selected]
    manifest: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "command": "run",
        "valid": True,
        "dry_run": False,
        "target": str(target),
        "evidence_dir": str(evidence_dir),
        "created_at": utc_now(),
        "tools": results,
        "proof_boundary": "local tool execution only; no production behavior, safe deletion, or architectural correctness is implied",
    }
    manifest_path = evidence_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest["manifest"] = {"path": str(manifest_path), "sha256": sha256(manifest_path)}
    failed = any(item["return_code"] != 0 for item in results)
    return (1 if failed else 0), manifest


def load_manifest(path_text: str) -> Dict[str, Any]:
    path = Path(path_text).expanduser().resolve()
    data = read_json(path)
    if (
        not isinstance(data, dict)
        or data.get("schema_version") != SCHEMA_VERSION
        or data.get("command") != "run"
        or not isinstance(data.get("target"), str)
        or not isinstance(data.get("tools"), list)
    ):
        raise EvidenceError("invalid_manifest", "manifest must be a version 1 quality evidence run")
    return data


def compare_command(before_path: str, after_path: str) -> Dict[str, Any]:
    before = load_manifest(before_path)
    after = load_manifest(after_path)
    if Path(before["target"]).resolve() != Path(after["target"]).resolve():
        raise EvidenceError("target_mismatch", "before and after manifests must describe the same target")
    before_tools = {item.get("name"): item for item in before["tools"] if isinstance(item, dict)}
    after_tools = {item.get("name"): item for item in after["tools"] if isinstance(item, dict)}
    comparisons = []
    for tool in sorted(set(before_tools) & set(after_tools)):
        before_metrics = before_tools[tool].get("metrics", {})
        after_metrics = after_tools[tool].get("metrics", {})
        if not isinstance(before_metrics, dict) or not isinstance(after_metrics, dict):
            continue
        deltas = []
        for metric in sorted(set(before_metrics) & set(after_metrics)):
            first = number(before_metrics[metric])
            second = number(after_metrics[metric])
            if first is not None and second is not None:
                deltas.append({"metric": metric, "before": first, "after": second, "delta": second - first})
        comparisons.append({"name": tool, "metrics": deltas})
    return {
        "schema_version": SCHEMA_VERSION,
        "command": "compare",
        "valid": True,
        "before": str(Path(before_path).expanduser().resolve()),
        "after": str(Path(after_path).expanduser().resolve()),
        "tools": comparisons,
        "proof_boundary": "numeric delta only; metric direction and behavior preservation require engineering review",
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="quality-evidence", description="External quality evidence runner for coding agents")
    commands = root.add_subparsers(dest="command", required=True)
    inventory = commands.add_parser("inventory", help="detect project signals and installed analyzers")
    inventory.add_argument("--target", required=True)
    inventory.add_argument("--json", action="store_true", help="accepted for a stable machine-readable interface")
    run = commands.add_parser("run", help="run explicitly selected analyzers and write an evidence manifest")
    run.add_argument("--target", required=True)
    run.add_argument("--evidence-dir", required=True)
    run.add_argument("--tool", action="append", choices=TOOL_NAMES, required=True)
    run.add_argument("--timeout", type=int, default=900)
    run.add_argument("--allow-network", action="store_true")
    run.add_argument("--allow-worktree-writes", action="store_true")
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--json", action="store_true", help="accepted for a stable machine-readable interface")
    compare = commands.add_parser("compare", help="compare normalized metrics from two manifests")
    compare.add_argument("--before", required=True)
    compare.add_argument("--after", required=True)
    compare.add_argument("--json", action="store_true", help="accepted for a stable machine-readable interface")
    return root


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        if arguments.command == "inventory":
            result = inventory_command(resolve_target(arguments.target))
            exit_code = 0
        elif arguments.command == "run":
            if arguments.timeout < 1 or arguments.timeout > 86400:
                raise EvidenceError("invalid_timeout", "timeout must be between 1 and 86400 seconds")
            exit_code, result = run_command(arguments)
        else:
            result = compare_command(arguments.before, arguments.after)
            exit_code = 0
        emit(result)
        return exit_code
    except EvidenceError as error:
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
