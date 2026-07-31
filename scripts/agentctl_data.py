from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from agentctl_json import decode_json
from agentctl_types import Config, DataError, JsonScalar, JsonValue, MemoryEntry, Problem, Route


MAX_JSONL_LINES = 10000
MAX_JSONL_LINE_BYTES = 65536
SCHEMA_VERSION = 1


def fail(code: str, message: str) -> DataError:
    return DataError(Problem(code, message))


def is_scalar(value: JsonValue) -> bool:
    return value is None or isinstance(value, (bool, int, float, str))


def is_integer(value: JsonValue) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def json_object(value: JsonValue, location: str) -> Dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise fail("invalid_shape", location + " must be a JSON object")
    return value


def string(value: JsonValue, location: str) -> str:
    if not isinstance(value, str) or not value:
        raise fail("invalid_value", location + " must be a non-empty string")
    return value


def allowed_keys(data: Dict[str, JsonValue], expected: Iterable[str], location: str) -> None:
    unknown = sorted(set(data) - set(expected))
    if unknown:
        raise fail("unknown_field", location + " has unknown field " + unknown[0])


def required_keys(data: Dict[str, JsonValue], expected: Iterable[str], location: str) -> None:
    missing = sorted(set(expected) - set(data))
    if missing:
        raise fail("missing_field", location + " is missing field " + missing[0])


def load_json(path: Path, label: str) -> JsonValue:
    try:
        source = path.read_bytes()
    except FileNotFoundError:
        raise fail("missing_file", label + " does not exist: " + str(path))
    except (OSError, ValueError) as error:
        raise fail("unreadable_file", label + " cannot be read: " + str(error))
    return decode_json(source, label, "invalid_json")


def parse_string_list(value: JsonValue, location: str) -> Tuple[str, ...]:
    if not isinstance(value, list):
        raise fail("invalid_shape", location + " must be an array")
    values = tuple(string(item, location + " item") for item in value)
    if len(set(values)) != len(values):
        raise fail("duplicate_value", location + " contains duplicate values")
    return values


def load_config(path_text: str) -> Config:
    try:
        path = Path(path_text).absolute()
    except (OSError, ValueError) as error:
        raise fail("unsafe_path", "config path cannot be resolved: " + str(error))
    root = json_object(load_json(path, "config"), "config")
    allowed_keys(root, ("schema_version", "memory", "routes"), "config")
    required_keys(root, ("schema_version", "memory", "routes"), "config")
    version = root["schema_version"]
    if not is_integer(version) or version != SCHEMA_VERSION:
        raise fail("unsupported_version", "config schema_version must be 1")
    memory = json_object(root["memory"], "config.memory")
    allowed_keys(memory, ("path", "scopes"), "config.memory")
    required_keys(memory, ("path", "scopes"), "config.memory")
    memory_name = string(memory["path"], "config.memory.path")
    memory_relative = Path(memory_name)
    if memory_relative.is_absolute() or ".." in memory_relative.parts:
        raise fail("unsafe_path", "config.memory.path must be a confined relative path")
    try:
        config_directory = path.resolve().parent
        memory_path = config_directory / memory_relative
        memory_path.resolve().relative_to(config_directory)
    except (OSError, RuntimeError, ValueError) as error:
        if isinstance(error, ValueError):
            raise fail("unsafe_path", "config.memory.path resolves outside the physical config directory")
        raise fail("unsafe_path", "config.memory.path cannot be resolved: " + str(error))
    scopes = parse_string_list(memory["scopes"], "config.memory.scopes")
    if not scopes:
        raise fail("invalid_value", "config.memory.scopes must not be empty")
    routes_value = root["routes"]
    if not isinstance(routes_value, list):
        raise fail("invalid_shape", "config.routes must be an array")
    routes: List[Route] = []
    identifiers: List[str] = []
    for index, item in enumerate(routes_value):
        route = json_object(item, "config.routes[" + str(index) + "]")
        allowed_keys(route, ("id", "priority", "when", "requires"), "route")
        required_keys(route, ("id", "priority", "when", "requires"), "route")
        identifier = string(route["id"], "route.id")
        priority = route["priority"]
        if not is_integer(priority) or priority < 0 or priority > 10000:
            raise fail("invalid_value", "route.priority must be an integer from 0 to 10000")
        when = json_object(route["when"], "route.when")
        if not when or any(not is_scalar(value) for value in when.values()):
            raise fail("invalid_value", "route.when must have scalar fields")
        requires = parse_string_list(route["requires"], "route.requires")
        routes.append(Route(identifier, priority, tuple(sorted(when.items())), requires))
        identifiers.append(identifier)
    if len(set(identifiers)) != len(identifiers):
        raise fail("duplicate_id", "config.routes contains duplicate ids")
    return Config(path, memory_path, scopes, tuple(routes))


def parse_memory_entry(value: JsonValue, line: int, scopes: Tuple[str, ...]) -> MemoryEntry:
    entry = json_object(value, "memory line " + str(line))
    allowed_keys(entry, ("id", "text", "scope", "sensitivity", "supersedes"), "memory entry")
    required_keys(entry, ("id", "text", "scope", "sensitivity"), "memory entry")
    identifier = string(entry["id"], "memory.id")
    text = string(entry["text"], "memory.text")
    scope = string(entry["scope"], "memory.scope")
    sensitivity = string(entry["sensitivity"], "memory.sensitivity")
    if scope not in scopes:
        raise fail("invalid_scope", "memory scope is not declared in config: " + scope)
    if sensitivity not in ("normal", "sensitive"):
        raise fail("invalid_sensitivity", "memory.sensitivity must be normal or sensitive")
    supersedes = None
    if "supersedes" in entry:
        supersedes = string(entry["supersedes"], "memory.supersedes")
    return MemoryEntry(identifier, text, scope, sensitivity, supersedes, line)


def check_supersedes(entries: Tuple[MemoryEntry, ...]) -> None:
    links = {entry.identifier: entry.supersedes for entry in entries if entry.supersedes}
    for identifier in links:
        seen = set()
        current = identifier
        while current in links:
            if current in seen:
                raise fail("supersedes_cycle", "memory supersedes graph contains a cycle at " + current)
            seen.add(current)
            current = links[current]
        if current not in {entry.identifier for entry in entries}:
            raise fail("unknown_supersedes", "memory supersedes unknown id " + current)


def load_memory(config: Config) -> Tuple[MemoryEntry, ...]:
    entries: List[MemoryEntry] = []
    try:
        with config.memory_path.open("rb") as memory_file:
            for line, raw in enumerate(memory_file, start=1):
                if line > MAX_JSONL_LINES:
                    raise fail("jsonl_limit", "memory exceeds maximum line count")
                if len(raw) > MAX_JSONL_LINE_BYTES:
                    raise fail("jsonl_limit", "memory line exceeds maximum byte length")
                if not raw.endswith(b"\n"):
                    raise fail("truncated_jsonl", "memory final line must end with a newline")
                if not raw.strip():
                    raise fail("invalid_jsonl", "memory contains a blank line")
                value = decode_json(raw, "memory line " + str(line), "invalid_jsonl")
                entries.append(parse_memory_entry(value, line, config.scopes))
    except FileNotFoundError:
        raise fail("missing_file", "memory does not exist: " + str(config.memory_path))
    except (OSError, ValueError) as error:
        raise fail("unreadable_file", "memory cannot be read: " + str(error))
    identifiers = [entry.identifier for entry in entries]
    if len(set(identifiers)) != len(identifiers):
        raise fail("duplicate_id", "memory contains duplicate ids")
    check_supersedes(tuple(entries))
    return tuple(entries)
