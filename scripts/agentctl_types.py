from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union


JsonScalar = Union[None, bool, int, float, str]
JsonValue = Union[JsonScalar, List["JsonValue"], Dict[str, "JsonValue"]]


@dataclass(frozen=True)  # noqa: SLOTS_OK - Python 3.9 dataclass has no slots parameter
class Problem:
    code: str
    message: str


class DataError(Exception):
    def __init__(self, problem: Problem) -> None:
        super().__init__(problem.message)
        self.problem = problem


@dataclass(frozen=True)  # noqa: SLOTS_OK - Python 3.9 dataclass has no slots parameter
class Route:
    identifier: str
    priority: int
    when: Tuple[Tuple[str, JsonScalar], ...]
    requires: Tuple[str, ...]


@dataclass(frozen=True)  # noqa: SLOTS_OK - Python 3.9 dataclass has no slots parameter
class Config:
    path: Path
    memory_path: Path
    scopes: Tuple[str, ...]
    routes: Tuple[Route, ...]


@dataclass(frozen=True)  # noqa: SLOTS_OK - Python 3.9 dataclass has no slots parameter
class MemoryEntry:
    identifier: str
    text: str
    scope: str
    sensitivity: str
    supersedes: Optional[str]
    line: int
