from __future__ import annotations

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
        summary={"progress": "done: x"},
        acceptance_criteria=["y is reviewed"],
        next_instructions="review y",
        context={"risk_level": "low"},
    )
    text = f"hello\n\n{format_handoff(envelope)}\n"
    parsed = parse_handoff_from_text(text)
    assert parsed == envelope


def test_parse_handoff_case_insensitive_role() -> None:
    text = """
    {
      "type": "handoff",
      "next_role": "reviewer",
      "summary": {"progress": "ok"},
      "acceptance_criteria": [],
      "next_instructions": "go",
      "context": {}
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
