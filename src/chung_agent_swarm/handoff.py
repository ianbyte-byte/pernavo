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
    DEPENDENCY_UPGRADER = "DependencyUpgrader"
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
    summary: str | Mapping[str, Any]
    next_instructions: str
    acceptance_criteria: list[str] | None = None
    context: Mapping[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        result = {
            "type": "handoff",
            "next_role": self.next_role.value,
            "summary": self.summary,
            "next_instructions": self.next_instructions,
        }
        if self.acceptance_criteria is not None:
            result["acceptance_criteria"] = self.acceptance_criteria
        if self.context is not None:
            result["context"] = self.context
        return result


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
    if isinstance(summary, str):
        if not summary.strip():
            raise HandoffValidationError('Missing or invalid "summary" (must be a non-empty string).')
        summary = summary.strip()
    elif isinstance(summary, Mapping):
        # Validate V2.2 mandatory summary fields
        required_fields = ["progress", "remaining", "risks", "changes"]
        missing = [f for f in required_fields if f not in summary]
        if missing:
            raise HandoffValidationError(
                f"Missing mandatory summary fields for V2.2: {', '.join(missing)}"
            )
        for field in required_fields:
            if not isinstance(summary[field], str):
                raise HandoffValidationError(f"Summary field {field!r} must be a string.")
    else:
        raise HandoffValidationError('Missing or invalid "summary" (must be a string or object).')

    next_instructions = obj.get("next_instructions")
    if not isinstance(next_instructions, str) or not next_instructions.strip():
        raise HandoffValidationError(
            'Missing or invalid "next_instructions" (must be a non-empty string).'
        )

    acceptance_criteria = obj.get("acceptance_criteria")
    if acceptance_criteria is not None:
        if not isinstance(acceptance_criteria, list) or not all(
            isinstance(i, str) for i in acceptance_criteria
        ):
            raise HandoffValidationError(
                'Invalid "acceptance_criteria" (must be a list of strings).'
            )

    context = obj.get("context")
    if context is not None:
        if not isinstance(context, Mapping):
            raise HandoffValidationError('Invalid "context" (must be an object).')

    return HandoffEnvelope(
        next_role=next_role,
        summary=summary,
        next_instructions=next_instructions.strip(),
        acceptance_criteria=acceptance_criteria,
        context=context,
    )
