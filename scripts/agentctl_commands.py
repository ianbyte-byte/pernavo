import stat
import unicodedata
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from agentctl_data import SCHEMA_VERSION, fail, json_object, load_json
from agentctl_types import Config, DataError, JsonValue, MemoryEntry


def error_result(command: str, error: DataError) -> Dict[str, JsonValue]:
    return {
        "schema_version": SCHEMA_VERSION,
        "command": command,
        "valid": False,
        "error": {"code": error.problem.code, "message": error.problem.message},
    }


def path_warnings(path: Path, label: str) -> List[str]:
    warnings: List[str] = []
    if path.is_symlink():
        warnings.append(label + " is a symlink")
    try:
        mode = stat.S_IMODE(path.stat().st_mode)
    except OSError:
        return warnings
    if mode & 0o022:
        warnings.append(label + " is group or world writable")
    return warnings


def doctor(config: Config, entries: Tuple[MemoryEntry, ...]) -> Dict[str, JsonValue]:
    warnings = path_warnings(config.path, "config") + path_warnings(config.memory_path, "memory")
    return {
        "schema_version": SCHEMA_VERSION,
        "command": "doctor",
        "valid": True,
        "config": {"path": str(config.path), "warnings": path_warnings(config.path, "config")},
        "memory": {
            "path": str(config.memory_path),
            "entries": len(entries),
            "warnings": path_warnings(config.memory_path, "memory"),
        },
        "warnings": warnings,
        "runtime": {"capabilities": "unknown", "hooks": "unknown", "auth": "unknown"},
    }


def load_event(path_text: str) -> Dict[str, JsonValue]:
    return json_object(load_json(Path(path_text).absolute(), "event"), "event")


def explain(config: Config, event: Dict[str, JsonValue]) -> Dict[str, JsonValue]:
    matched = []
    skipped = []
    for route in config.routes:
        missing = [field for field, value in route.when if field not in event or event[field] != value]
        item = {"id": route.identifier, "priority": route.priority, "requires": list(route.requires)}
        if missing:
            item["reason"] = "event mismatch: " + missing[0]
            skipped.append(item)
        else:
            matched.append(item)
    matched.sort(key=lambda item: (-item["priority"], item["id"]))
    skipped.sort(key=lambda item: item["id"])
    conflicts = []
    for priority in sorted({item["priority"] for item in matched}, reverse=True):
        route_ids = sorted(item["id"] for item in matched if item["priority"] == priority)
        if len(route_ids) > 1:
            conflicts.append({"priority": priority, "route_ids": route_ids})
    capabilities = sorted({name for item in matched for name in item["requires"]})
    return {
        "schema_version": SCHEMA_VERSION,
        "command": "explain",
        "valid": True,
        "matched": matched,
        "skipped": skipped,
        "conflicts": conflicts,
        "required_capabilities": [{"name": name, "state": "unknown"} for name in capabilities],
    }


def normalized(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold()


def score(query: str, text: str) -> int:
    return normalized(text).count(normalized(query))


def memory_search(
    config: Config, entries: Sequence[MemoryEntry], query: str, scopes: Sequence[str], include_sensitive: bool
) -> Dict[str, JsonValue]:
    wanted_scopes = tuple(scopes) if scopes else config.scopes
    unknown_scopes = sorted(set(wanted_scopes) - set(config.scopes))
    if unknown_scopes:
        raise fail("invalid_scope", "scope is not declared in config: " + unknown_scopes[0])
    if not normalized(query).strip():
        raise fail("invalid_query", "query must contain visible text")
    superseded_ids = {entry.supersedes for entry in entries if entry.supersedes}
    results = []
    for entry in entries:
        match_score = score(query, entry.text)
        if entry.identifier not in superseded_ids and entry.scope in wanted_scopes and match_score and (include_sensitive or entry.sensitivity != "sensitive"):
            results.append((match_score, entry))
    results.sort(key=lambda item: (-item[0], item[1].identifier))
    return {
        "schema_version": SCHEMA_VERSION,
        "command": "memory search",
        "valid": True,
        "query": query,
        "scopes": list(wanted_scopes),
        "include_sensitive": include_sensitive,
        "results": [
            {
                "id": entry.identifier,
                "text": entry.text,
                "scope": entry.scope,
                "sensitivity": entry.sensitivity,
                "score": match_score,
                "provenance": {"path": str(config.memory_path), "line": entry.line},
            }
            for match_score, entry in results
        ],
    }
