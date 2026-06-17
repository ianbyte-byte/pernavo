from __future__ import annotations

import json
import pytest

from chung_agent_swarm.handoff import (
    AgentRole,
    HandoffValidationError,
    parse_handoff_from_text,
)

def test_parse_rejects_invalid_structured_summary() -> None:
    text = json.dumps(
        {
            "type": "handoff",
            "next_role": "Router",
            "summary": {"progress": 123, "remaining": "none", "risks": "none", "changes": "none"},
            "next_instructions": "go",
        }
    )
    with pytest.raises(HandoffValidationError, match="Summary field \"progress\" must be a string."):
        parse_handoff_from_text(text)

def test_parse_accepts_valid_structured_summary() -> None:
    text = json.dumps(
        {
            "type": "handoff",
            "next_role": "Router",
            "summary": {"progress": "done", "remaining": "none", "risks": "none", "changes": "none"},
            "next_instructions": "go",
        }
    )
    parsed = parse_handoff_from_text(text)
    assert parsed.summary["progress"] == "done"
