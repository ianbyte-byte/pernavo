from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .json_extract import JsonExtractionError, extract_first_json_value


class AgentRole(str, Enum):
    ROUTER = "Router"
    CODER = "Coder"
    REVIEWER = "Reviewer"
    TESTER = "Tester"
    ARCHITECT = "Architect"
    AI_NATIVE_ARCHITECT = "AiNativeArchitect"
    PRODUCT = "Product"
    SECURITY_REVIEWER = "SecurityReviewer"
    DEBUGGER = "Debugger"
    REFACTORER = "Refactorer"
    PERFORMANCE_OPTIMIZER = "PerformanceOptimizer"
    SQL_OPTIMIZER = "SqlOptimizer"
    DOCS_WRITER = "DocsWriter"
    RELEASE_MANAGER = "ReleaseManager"
    INCIDENT_TRIAGE = "IncidentTriage"
    GIT_WORKTREE_MANAGER = "GitWorktreeManager"
    SIMPLIFIER = "Simplifier"

    @classmethod
    def parse(cls, value: str) -> "AgentRole":
        normalized = value.strip()
        for role in cls:
            if normalized.lower() == role.value.lower():
                return role
        raise HandoffValidationError(f"Invalid next_role: {value!r}")


@dataclass(frozen=True)
class HandoffEnvelope:
    next_role: AgentRole
    summary: str
    next_instructions: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "handoff",
            "next_role": self.next_role.value,
            "summary": self.summary,
            "next_instructions": self.next_instructions,
        }


class HandoffError(ValueError):
    pass


class HandoffValidationError(HandoffError):
    pass


class HandoffParseError(HandoffError):
    pass


def format_handoff(handoff: HandoffEnvelope) -> str:
    return json.dumps(handoff.to_dict(), indent=2, ensure_ascii=False, sort_keys=False)


def parse_handoff_from_text(text: str) -> HandoffEnvelope:
    try:
        extracted = extract_first_json_value(text)
    except JsonExtractionError as e:
        raise HandoffParseError(str(e)) from e

    if not isinstance(extracted.value, Mapping):
        raise HandoffValidationError("Extracted JSON value is not an object.")

    return parse_handoff_dict(extracted.value)


def parse_handoff_dict(obj: Mapping[str, Any]) -> HandoffEnvelope:
    if obj.get("type") != "handoff":
        raise HandoffValidationError('Missing or invalid "type": expected "handoff".')

    next_role_raw = obj.get("next_role")
    if not isinstance(next_role_raw, str) or not next_role_raw.strip():
        raise HandoffValidationError('Missing or invalid "next_role" (must be a non-empty string).')
    next_role = AgentRole.parse(next_role_raw)

    summary = obj.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        raise HandoffValidationError('Missing or invalid "summary" (must be a non-empty string).')

    next_instructions = obj.get("next_instructions")
    if not isinstance(next_instructions, str) or not next_instructions.strip():
        raise HandoffValidationError(
            'Missing or invalid "next_instructions" (must be a non-empty string).'
        )

    return HandoffEnvelope(
        next_role=next_role,
        summary=summary.strip(),
        next_instructions=next_instructions.strip(),
    )
