from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Sequence

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
class HandoffSummary:
    progress: str
    remaining: str
    risks: str
    changes: str

    def to_dict(self) -> dict[str, str]:
        return {
            "progress": self.progress,
            "remaining": self.remaining,
            "risks": self.risks,
            "changes": self.changes,
        }


@dataclass(frozen=True)
class HandoffContext:
    platform_api_needed: bool
    session_config_updated: bool
    test_coverage_required: str
    risk_level: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "platform_api_needed": self.platform_api_needed,
            "session_config_updated": self.session_config_updated,
            "test_coverage_required": self.test_coverage_required,
            "risk_level": self.risk_level,
        }


@dataclass(frozen=True)
class HandoffEnvelope:
    next_role: AgentRole
    summary: HandoffSummary
    acceptance_criteria: Sequence[str]
    next_instructions: str
    context: HandoffContext

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "handoff",
            "next_role": self.next_role.value,
            "summary": self.summary.to_dict(),
            "acceptance_criteria": list(self.acceptance_criteria),
            "next_instructions": self.next_instructions,
            "context": self.context.to_dict(),
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

    summary_raw = obj.get("summary")
    if isinstance(summary_raw, str):
        # Backward compatibility for simple string summary
        summary = HandoffSummary(
            progress=summary_raw.strip(),
            remaining="N/A",
            risks="N/A",
            changes="N/A"
        )
    elif isinstance(summary_raw, Mapping):
        summary = HandoffSummary(
            progress=str(summary_raw.get("progress", "")).strip(),
            remaining=str(summary_raw.get("remaining", "")).strip(),
            risks=str(summary_raw.get("risks", "")).strip(),
            changes=str(summary_raw.get("changes", "")).strip(),
        )
    else:
        raise HandoffValidationError('Missing or invalid "summary" (must be a string or object).')

    acceptance_criteria = obj.get("acceptance_criteria", [])
    if not isinstance(acceptance_criteria, (list, tuple)):
        raise HandoffValidationError('"acceptance_criteria" must be a list of strings.')
    acceptance_criteria = [str(c).strip() for c in acceptance_criteria]

    next_instructions = obj.get("next_instructions")
    if not isinstance(next_instructions, str) or not next_instructions.strip():
        raise HandoffValidationError(
            'Missing or invalid "next_instructions" (must be a non-empty string).'
        )

    context_raw = obj.get("context", {})
    if not isinstance(context_raw, Mapping):
        raise HandoffValidationError('"context" must be an object.')

    context = HandoffContext(
        platform_api_needed=bool(context_raw.get("platform_api_needed", False)),
        session_config_updated=bool(context_raw.get("session_config_updated", False)),
        test_coverage_required=str(context_raw.get("test_coverage_required", "minimal")),
        risk_level=str(context_raw.get("risk_level", "low")),
    )

    return HandoffEnvelope(
        next_role=next_role,
        summary=summary,
        acceptance_criteria=acceptance_criteria,
        next_instructions=next_instructions.strip(),
        context=context,
    )
