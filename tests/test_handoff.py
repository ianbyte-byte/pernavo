from __future__ import annotations

import json
import pytest

from chung_agent_swarm.handoff import (
    AgentRole,
    HandoffParseError,
    HandoffValidationError,
    HandoffEnvelope,
    format_handoff,
    parse_handoff_from_text,
)


def test_format_and_parse_roundtrip() -> None:
    envelope = HandoffEnvelope(
        next_role=AgentRole.REVIEWER,
        summary="done: x",
        next_instructions="review y",
    )
    text = f"hello\n\n{format_handoff(envelope)}\n"
    parsed = parse_handoff_from_text(text)
    assert parsed == envelope


def test_parse_handoff_case_insensitive_role() -> None:
    text = """
    {
      "type": "handoff",
      "next_role": "reviewer",
      "summary": "ok",
      "next_instructions": "go"
    }
    """
    parsed = parse_handoff_from_text(text)
    assert parsed.next_role == AgentRole.REVIEWER


def test_parse_rejects_non_object_json() -> None:
    with pytest.raises(HandoffValidationError):
        parse_handoff_from_text("[1, 2, 3]")


def test_parse_rejects_missing_json() -> None:
    with pytest.raises(HandoffParseError):
        parse_handoff_from_text("no json here")


def test_enhanced_schema_roundtrip() -> None:
    envelope = HandoffEnvelope(
        next_role=AgentRole.AI_NATIVE_ARCHITECT,
        summary={
            "progress": "done something",
            "remaining": "do more",
            "risks": "none",
            "changes": "src/x.py",
        },
        next_instructions="go ahead",
        acceptance_criteria=["criterion 1", "criterion 2"],
        context={"platform_api_needed": True},
    )
    text = format_handoff(envelope)
    parsed = parse_handoff_from_text(text)
    assert parsed == envelope


def test_parse_expanded_roles() -> None:
    for role in AgentRole:
        text = json.dumps(
            {
                "type": "handoff",
                "next_role": role.value,
                "summary": "ok",
                "next_instructions": "go",
            }
        )
        parsed = parse_handoff_from_text(text)
        assert parsed.next_role == role


def test_parse_rejects_invalid_acceptance_criteria() -> None:
    text = json.dumps(
        {
            "type": "handoff",
            "next_role": "Router",
            "summary": "ok",
            "next_instructions": "go",
            "acceptance_criteria": "not a list",
        }
    )
    with pytest.raises(HandoffValidationError, match="Invalid \"acceptance_criteria\""):
        parse_handoff_from_text(text)


def test_parse_rejects_invalid_context() -> None:
    text = json.dumps(
        {
            "type": "handoff",
            "next_role": "Router",
            "summary": "ok",
            "next_instructions": "go",
            "context": ["not", "an", "object"],
        }
    )
    with pytest.raises(HandoffValidationError, match="Invalid \"context\""):
        parse_handoff_from_text(text)
