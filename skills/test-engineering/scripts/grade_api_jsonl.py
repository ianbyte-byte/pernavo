#!/usr/bin/env python3
"""Grade an API/business-test JSONL file against a pre-declared case matrix.

JSONL is process evidence. This script is the completion oracle. It does not
read assistant prose. Stdlib only so the Skill copy can run after install.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "pernavo.api_test_matrix.v1"
BUSINESS_SUCCESS = "business-success"
TERMINAL = {"passed", "failed", "blocked", "skipped"}
SIDE_EFFECT_EVENTS = {
    "database.reconciliation",
    "side_effect",
    "side-effect",
    "db.reconciliation",
}


class GradeError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GradeError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GradeError(f"invalid JSON in {path}: {exc}") from exc


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise GradeError(f"missing JSONL: {path}") from exc
    for index, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise GradeError(f"invalid JSONL at {path}:{index}: {exc}") from exc
        if isinstance(item, dict):
            records.append(item)
    return records


def case_id_of(record: dict[str, Any]) -> str | None:
    for key in ("case_id", "caseId", "case"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    value = record.get("id")
    if isinstance(value, str) and value.strip() and not str(record.get("event") or "").startswith("test-run"):
        return value.strip()
    return None


def nested_get(record: dict[str, Any], *paths: tuple[str, ...]) -> Any:
    for path in paths:
        cursor: Any = record
        for key in path:
            if not isinstance(cursor, dict) or key not in cursor:
                cursor = None
                break
            cursor = cursor[key]
        if cursor is not None:
            return cursor
    return None


def http_status_of(record: dict[str, Any]) -> int | None:
    value = nested_get(
        record,
        ("http_status",),
        ("httpStatus",),
        ("response", "httpStatus"),
        ("response", "http_status"),
        ("response", "status"),
    )
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def business_result_of(record: dict[str, Any]) -> Any:
    return nested_get(
        record,
        ("result",),
        ("response", "result"),
        ("response", "body", "result"),
        ("body", "result"),
    )


def verdict_of(record: dict[str, Any]) -> str | None:
    for key in ("verdict", "assertion_status", "assertionStatus", "evidence_status"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip().lower()
    status = record.get("status")
    if isinstance(status, str) and status.strip().lower() in TERMINAL:
        return status.strip().lower()
    return None


def reason_of(record: dict[str, Any]) -> str:
    for key in ("reason", "blocked_reason", "skip_reason", "resultdetail"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    detail = nested_get(record, ("response", "resultdetail"), ("response", "body", "resultdetail"))
    if isinstance(detail, str) and detail.strip():
        return detail.strip()
    return ""


def has_side_effect(records: list[dict[str, Any]]) -> bool:
    for record in records:
        event = str(record.get("event") or record.get("kind") or "")
        if event in SIDE_EFFECT_EVENTS or event.endswith("reconciliation"):
            return True
        if record.get("sideEffect") or record.get("side_effect") or record.get("database"):
            return True
    return False


def load_matrix(path: Path) -> dict[str, Any]:
    matrix = load_json(path)
    if not isinstance(matrix, dict):
        raise GradeError("matrix must be a JSON object")
    cases = matrix.get("required_cases")
    if not isinstance(cases, list) or not cases:
        raise GradeError("matrix.required_cases must be a non-empty list")
    ids: list[str] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or not isinstance(case.get("id"), str) or not case["id"].strip():
            raise GradeError(f"required_cases[{index}] needs a string id")
        case_id = case["id"].strip()
        if case_id in ids:
            raise GradeError(f"duplicate case id: {case_id}")
        ids.append(case_id)
        kind = case.get("kind", "other")
        if not isinstance(kind, str) or not kind.strip():
            raise GradeError(f"{case_id} needs a kind")
    return matrix


def resolve_jsonl(matrix: dict[str, Any], matrix_path: Path, explicit: Path | None, cwd: Path) -> Path:
    if explicit is not None:
        return explicit if explicit.is_absolute() else cwd / explicit
    raw = matrix.get("jsonl")
    if isinstance(raw, str) and raw.strip():
        candidate = Path(raw.strip())
        if candidate.is_absolute():
            return candidate
        beside_matrix = matrix_path.parent / candidate
        if beside_matrix.is_file():
            return beside_matrix
        return cwd / candidate
    sibling = matrix_path.with_suffix(".jsonl")
    if sibling.is_file():
        return sibling
    raise GradeError("matrix.jsonl is missing; point jsonl at the evidence file")


def records_for(case_id: str, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [record for record in records if case_id_of(record) == case_id]


def expect_map(case: dict[str, Any]) -> dict[str, Any]:
    expect = case.get("expect")
    return expect if isinstance(expect, dict) else {}


def needs_side_effects(case: dict[str, Any]) -> bool:
    value = case.get("side_effects")
    if value is False or value is None:
        return str(case.get("kind")) == BUSINESS_SUCCESS
    if value is True:
        return True
    if isinstance(value, list):
        return len(value) > 0
    return False


def evaluate_case(case: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    case_id = case["id"].strip()
    kind = str(case.get("kind")).strip()
    expect = expect_map(case)
    matched = records_for(case_id, records)
    result: dict[str, Any] = {"id": case_id, "kind": kind, "state": "missing", "reasons": []}
    if not matched:
        result["reasons"].append("no JSONL records for this case_id")
        return result

    verdicts = [verdict_of(record) for record in matched]
    explicit = [item for item in verdicts if item in TERMINAL]
    if "blocked" in explicit and "passed" not in explicit:
        result["state"] = "blocked"
        reasons = [reason_of(record) for record in matched if reason_of(record)]
        if not reasons:
            result["reasons"].append("blocked without reason")
        else:
            result["reasons"].extend(reasons)
        return result
    if "skipped" in explicit and "passed" not in explicit:
        result["state"] = "skipped"
        reasons = [reason_of(record) for record in matched if reason_of(record)]
        if not reasons:
            result["reasons"].append("skipped without reason")
        else:
            result["reasons"].extend(reasons)
        return result

    expected_http = expect.get("http")
    if expected_http is not None:
        statuses = [http_status_of(record) for record in matched]
        if expected_http not in statuses:
            result["state"] = "failed"
            result["reasons"].append(f"expected http {expected_http}, observed {statuses}")
            return result

    expected_result = expect.get("result")
    observed_results = [business_result_of(record) for record in matched]
    observed_results = [item for item in observed_results if item is not None]
    if expected_result is not None:
        if expected_result not in observed_results:
            result["state"] = "failed"
            result["reasons"].append(f"expected result {expected_result}, observed {observed_results}")
            return result

    if kind == BUSINESS_SUCCESS:
        if 1 not in observed_results and expected_result is None:
            result["state"] = "failed"
            result["reasons"].append("business-success requires result=1; HTTP 200 is not enough")
            return result
        if expected_result == -1 or (observed_results and all(item == -1 for item in observed_results)):
            result["state"] = "failed"
            result["reasons"].append("business-success cannot be satisfied by result=-1")
            return result
        if needs_side_effects(case) and not has_side_effect(matched):
            result["state"] = "failed"
            result["reasons"].append("business-success missing side-effect/reconciliation evidence")
            return result

    if "failed" in explicit:
        result["state"] = "failed"
        result["reasons"].extend(reason_of(record) or "verdict=failed" for record in matched if verdict_of(record) == "failed")
        return result

    result["state"] = "passed"
    return result


def grade(matrix: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    cases = [evaluate_case(case, records) for case in matrix["required_cases"]]
    by_state: dict[str, list[str]] = {state: [] for state in ("passed", "failed", "blocked", "skipped", "missing")}
    for case in cases:
        by_state[case["state"]].append(case["id"])

    business = [case for case in cases if case["kind"] == BUSINESS_SUCCESS]
    reasons: list[str] = []
    if not business:
        reasons.append("matrix_has_no_business_success")
    elif not any(case["state"] == "passed" for case in business):
        reasons.append("no_passed_business_success")

    for case in cases:
        if case["state"] == "missing":
            reasons.append(f"missing:{case['id']}")
        elif case["state"] == "failed":
            reasons.append(f"failed:{case['id']}:{'; '.join(case['reasons'])}")
        elif case["state"] in {"blocked", "skipped"} and case["reasons"] and "without reason" in case["reasons"][0]:
            reasons.append(f"{case['state']}_unexplained:{case['id']}")

    passed = not reasons
    status = "passed" if passed else ("incomplete" if "missing:" in " ".join(reasons) or reasons[:1] in (["matrix_has_no_business_success"], ["no_passed_business_success"]) else "failed")
    if not passed and any(item.startswith("missing:") or item in {"matrix_has_no_business_success", "no_passed_business_success"} for item in reasons):
        status = "incomplete"
    elif not passed:
        status = "failed"

    next_case = next((item.split(":", 1)[1] for item in reasons if item.startswith("missing:")), None)
    if next_case is None:
        next_case = next((item.split(":", 1)[1].split(":", 1)[0] for item in reasons if item.startswith("failed:")), None)
    if next_case is None and reasons:
        next_case = reasons[0]

    return {
        "schema_version": SCHEMA,
        "pass": passed,
        "status": status,
        "cases": cases,
        "counts": {key: len(value) for key, value in by_state.items()},
        "missing": by_state["missing"],
        "reasons": reasons,
        "next_case": next_case,
    }


def format_reason(report: dict[str, Any]) -> str:
    if report["pass"]:
        return "api-test-gate passed"
    next_case = report.get("next_case") or "unknown"
    status = report.get("status")
    missing = report.get("missing") or []
    if missing:
        return f"api-test-gate {status}: missing {', '.join(missing[:4])}; run {next_case} next"
    return f"api-test-gate {status}: {'; '.join(report.get('reasons', [])[:3])}; run {next_case} next"


def run(matrix_path: Path, jsonl_path: Path | None, cwd: Path | None = None) -> dict[str, Any]:
    cwd = cwd or Path.cwd()
    matrix = load_matrix(matrix_path)
    evidence = resolve_jsonl(matrix, matrix_path, jsonl_path, cwd)
    records = load_jsonl(evidence)
    report = grade(matrix, records)
    report["matrix"] = str(matrix_path)
    report["jsonl"] = str(evidence)
    report["reason"] = format_reason(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Grade API JSONL evidence against a case matrix")
    parser.add_argument("--matrix", required=True, type=Path)
    parser.add_argument("--jsonl", type=Path)
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--hook", action="store_true", help="emit Stop-hook JSON and use exit 2 on failure")
    args = parser.parse_args(argv)
    try:
        report = run(args.matrix.expanduser(), args.jsonl.expanduser() if args.jsonl else None, args.cwd)
    except GradeError as exc:
        report = {
            "schema_version": SCHEMA,
            "pass": False,
            "status": "incomplete",
            "reasons": [str(exc)],
            "next_case": "fix-matrix-or-jsonl",
            "reason": f"api-test-gate incomplete: {exc}",
            "missing": [],
            "cases": [],
        }
    print(json.dumps(report, ensure_ascii=True, indent=2))
    if report["pass"]:
        return 0
    return 2 if args.hook else 1


if __name__ == "__main__":
    raise SystemExit(main())
