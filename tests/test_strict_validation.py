from __future__ import annotations

import json
import pytest

from chung_agent_swarm.handoff import (
    parse_handoff_from_text,
    HandoffValidationError,
)

def test_parse_strict_validation_enhanced_summary() -> None:
    text = json.dumps({
        "type": "handoff",
        "next_role": "Router",
        "summary": {
            "progress": "A",
            "remaining": "B",
            "risks": "C",
            "changes": "D"
        },
        "next_instructions": "go"
    })
    parsed = parse_handoff_from_text(text)
    assert parsed.summary["progress"] == "A"

def test_parse_rejects_missing_enhanced_summary_fields() -> None:
    text = json.dumps({
        "type": "handoff",
        "next_role": "Router",
        "summary": {
            "progress": "A",
            "remaining": "B"
            # risks and changes missing
        },
        "next_instructions": "go"
    })
    with pytest.raises(HandoffValidationError, match="Missing or invalid summary field 'risks'"):
        parse_handoff_from_text(text)

def test_parse_rejects_invalid_type_enhanced_summary_fields() -> None:
    text = json.dumps({
        "type": "handoff",
        "next_role": "Router",
        "summary": {
            "progress": "A",
            "remaining": "B",
            "risks": 123, # Not a string
            "changes": "D"
        },
        "next_instructions": "go"
    })
    with pytest.raises(HandoffValidationError, match="Missing or invalid summary field 'risks'"):
        parse_handoff_from_text(text)
