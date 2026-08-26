#!/usr/bin/env python3
"""Run bounded SQL against an explicitly configured non-production database."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

MAX_TIMEOUT_SECONDS = 300
PRODUCTION_MARKERS = re.compile(r"(^|[-_.])(prod|production|live)([-_.]|$)", re.IGNORECASE)
READ_ONLY_PREFIXES = ("select", "show", "describe", "explain", "with", "pragma")


class RunnerError(Exception):
    pass


def redact_target(url: str) -> dict[str, str]:
    parsed = urlsplit(url)
    scheme = parsed.scheme.lower()
    if scheme == "sqlite":
        return {"driver": "sqlite", "target": Path(unquote(parsed.path)).name or ":memory:"}
    return {
        "driver": {
            "postgres": "postgresql",
            "mssql": "sqlserver",
            "mssql+pyodbc": "sqlserver",
            "mssql+pymssql": "sqlserver",
        }.get(scheme, scheme),
        "host": parsed.hostname or "",
        "database": (parsed.path or "").lstrip("/").split("/", 1)[0],
    }


def get_url(args: argparse.Namespace) -> str:
    if bool(args.url) == bool(args.url_env):
        raise RunnerError("provide exactly one of --url or --url-env")
    url = args.url or os.environ.get(args.url_env, "")
    if not url:
        raise RunnerError("the requested URL environment variable is unset")
    if urlsplit(url).scheme.lower() not in {"sqlite", "postgres", "postgresql", "mysql", "mssql", "sqlserver", "mssql+pyodbc", "mssql+pymssql"}:
        raise RunnerError("supported URL schemes are sqlite, postgresql, postgres, mysql, mssql, and sqlserver")
    return url


def validate_target(url: str) -> None:
    target = redact_target(url)
    values = " ".join(str(value) for key, value in target.items() if key != "driver")
    if PRODUCTION_MARKERS.search(values):
        raise RunnerError("refusing a target whose host or database name appears to be production")


def load_sql(args: argparse.Namespace) -> str:
    if bool(args.sql) == bool(args.file):
        raise RunnerError("provide exactly one of --sql or --file")
    if args.file:
        try:
            sql = Path(args.file).read_text(encoding="utf-8")
        except OSError as exc:
            raise RunnerError(f"cannot read SQL file: {exc}") from exc
    else:
        sql = args.sql
    if not sql.strip():
        raise RunnerError("SQL must not be empty")
    return sql


def sql_is_read_only(sql: str) -> bool:
    stripped = re.sub(r"/\*.*?\*/|--[^\n]*", " ", sql, flags=re.DOTALL).lstrip()
    first = stripped.split(None, 1)[0].lower() if stripped else ""
    statements = [statement.strip() for statement in stripped.split(";") if statement.strip()]
    return len(statements) == 1 and first in READ_ONLY_PREFIXES and not re.search(
        r"\b(insert|update|delete|merge|create|alter|drop|truncate|grant|revoke|vacuum|attach|detach)\b",
        stripped,
        flags=re.IGNORECASE,
    )


def authorize(args: argparse.Namespace, sql: str) -> None:
    if args.mode == "read":
        if not sql_is_read_only(sql):
            raise RunnerError("read mode accepts only a single read-only SQL operation; use explicit write gates")
        return
    if not args.allow_write or os.environ.get("DATABASE_TESTING_ALLOW_WRITE") != "1":
        raise RunnerError("write mode requires --allow-write and DATABASE_TESTING_ALLOW_WRITE=1")


def sqlite_command(url: str, sql: str, timeout: int, mode: str) -> dict[str, object]:
    parsed = urlsplit(url)
    database = ":memory:" if parsed.path in {"", "/:memory:"} else unquote(parsed.path)
    if mode == "read":
        if database == ":memory:":
            connection = sqlite3.connect(database, timeout=timeout)
        else:
            database = f"file:{Path(database).resolve()}?mode=ro"
            connection = sqlite3.connect(database, timeout=timeout, uri=True)
        connection.execute("PRAGMA query_only = ON")
    else:
        connection = sqlite3.connect(database, timeout=timeout)
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        if cursor.description:
            columns = [column[0] for column in cursor.description]
            rows = [list(row) for row in cursor.fetchmany(100)]
            return {"status": "ok", "columns": columns, "rows": rows, "rows_truncated": cursor.fetchone() is not None}
        connection.commit()
        return {"status": "ok", "rows_affected": cursor.rowcount}
    except sqlite3.Error as exc:
        connection.rollback()
        raise RunnerError(f"SQLite execution failed: {exc}") from exc
    finally:
        connection.close()


def client_command(url: str, sql: str, timeout: int, mode: str) -> dict[str, object]:
    parsed = urlsplit(url)
    scheme = parsed.scheme.lower()
    executable = "psql" if scheme in {"postgres", "postgresql"} else "mysql" if scheme == "mysql" else "sqlcmd"
    if not shutil.which(executable):
        raise RunnerError(f"{executable} is not installed or is not on PATH")
    database = unquote(parsed.path.lstrip("/"))
    env = os.environ.copy()
    if scheme in {"postgres", "postgresql"}:
        env.update({"PGHOST": parsed.hostname or "", "PGPORT": str(parsed.port or 5432), "PGUSER": unquote(parsed.username or ""), "PGPASSWORD": unquote(parsed.password or ""), "PGDATABASE": database})
        query = parse_qs(parsed.query)
        if query.get("sslmode"):
            env["PGSSLMODE"] = query["sslmode"][0]
        statement = f"BEGIN READ ONLY; {sql}; ROLLBACK;" if mode == "read" else sql
        command = ["psql", "--no-psqlrc", "--set", "ON_ERROR_STOP=1", "--command", statement]
    elif scheme == "mysql":
        env["MYSQL_PWD"] = unquote(parsed.password or "")
        command = ["mysql", "--protocol=TCP", "--host", parsed.hostname or "", "--port", str(parsed.port or 3306)]
        if parsed.username:
            command.extend(["--user", unquote(parsed.username)])
        statement = f"START TRANSACTION READ ONLY; {sql}; ROLLBACK;" if mode == "read" else sql
        command.extend(["--batch", "--raw", "--execute", statement, database])
    else:
        env["SQLCMDPASSWORD"] = unquote(parsed.password or "")
        server = parsed.hostname or ""
        if parsed.port:
            server = f"{server},{parsed.port}"
        command = ["sqlcmd", "-b", "-l", str(timeout), "-S", server, "-d", database]
        if parsed.username:
            command.extend(["-U", unquote(parsed.username)])
        statement = f"SET XACT_ABORT ON; BEGIN TRANSACTION; {sql}; ROLLBACK TRANSACTION;" if mode == "read" else sql
        command.extend(["-Q", statement])
    try:
        completed = subprocess.run(command, env=env, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RunnerError(f"database command exceeded {timeout}s timeout") from exc
    if completed.returncode:
        message = completed.stderr.strip() or "database client returned a non-zero exit status"
        raise RunnerError(f"{executable} execution failed: {message[:2000]}")
    stdout = completed.stdout[:100000]
    return {"status": "ok", "client": executable, "stdout": stdout, "output_truncated": len(completed.stdout) > len(stdout)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    for name in ("preflight", "run"):
        command = subcommands.add_parser(name)
        source = command.add_mutually_exclusive_group(required=True)
        source.add_argument("--url")
        source.add_argument("--url-env")
        if name == "run":
            input_group = command.add_mutually_exclusive_group(required=True)
            input_group.add_argument("--sql")
            input_group.add_argument("--file", type=Path)
            command.add_argument("--mode", choices=("read", "write"), default="read")
            command.add_argument("--allow-write", action="store_true")
            command.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    try:
        url = get_url(args)
        validate_target(url)
        if args.command == "preflight":
            target = redact_target(url)
            client = {"sqlite": "stdlib sqlite3", "postgresql": "psql", "mysql": "mysql", "sqlserver": "sqlcmd"}[target["driver"]]
            if client != "stdlib sqlite3":
                target["client_available"] = shutil.which(client) is not None
            print(json.dumps({"status": "ready", "target": target}, ensure_ascii=False))
            return 0
        if not 1 <= args.timeout <= MAX_TIMEOUT_SECONDS:
            raise RunnerError(f"timeout must be between 1 and {MAX_TIMEOUT_SECONDS} seconds")
        sql = load_sql(args)
        authorize(args, sql)
        target = redact_target(url)
        result = sqlite_command(url, sql, args.timeout, args.mode) if target["driver"] == "sqlite" else client_command(url, sql, args.timeout, args.mode)
        print(json.dumps({"target": target, "mode": args.mode, "result": result}, ensure_ascii=False, default=str))
        return 0
    except RunnerError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
