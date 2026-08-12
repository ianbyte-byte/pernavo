#!/usr/bin/env python3
"""Create and validate a secret-safe, local performance evidence manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


TOOLS = ("curl", "git", "docker", "dotnet", "java", "node", "psql", "mysql", "wrk", "k6", "hey")


def run(argv: list[str], cwd: Path) -> dict[str, object]:
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=10)
        return {"argv": argv, "exit_code": p.returncode, "stdout_sha256": sha(p.stdout), "stderr_sha256": sha(p.stderr)}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"argv": argv, "status": "unavailable", "error_type": type(exc).__name__}


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", "replace")).hexdigest()


def inventory(target: Path) -> dict[str, object]:
    tools = {name: shutil.which(name) is not None for name in TOOLS}
    git = run(["git", "rev-parse", "--show-toplevel"], target)
    return {
        "schema": "pernavo.performance-evidence/v1",
        "state": "inventory-only",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "target": str(target.resolve()),
        "host": {"system": platform.system(), "release": platform.release(), "machine": platform.machine()},
        "tools_present": tools,
        "git_probe": git,
        "secret_environment_presence": {
            key: bool(os.environ.get(key))
            for key in ("EXA_API_KEY", "SONAR_TOKEN", "SONARQUBE_TOKEN", "DATABASE_URL")
        },
        "proof_boundary": "Does not run a workload, profiler, database query, or network call.",
    }


def validate(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ("schema", "state", "created_at", "target", "proof_boundary")
    missing = [key for key in required if key not in data]
    if missing:
        print(json.dumps({"valid": False, "missing": missing}, ensure_ascii=False))
        return 2
    if data.get("schema") != "pernavo.performance-evidence/v1":
        print(json.dumps({"valid": False, "reason": "unsupported schema"}, ensure_ascii=False))
        return 2
    print(json.dumps({"valid": True, "schema": data["schema"], "state": data["state"]}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inv = sub.add_parser("inventory")
    inv.add_argument("--target", type=Path, default=Path.cwd())
    inv.add_argument("--json", action="store_true")
    val = sub.add_parser("validate")
    val.add_argument("manifest", type=Path)
    args = parser.parse_args()
    if args.command == "inventory":
        result = inventory(args.target)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    return validate(args.manifest)


if __name__ == "__main__":
    sys.exit(main())
