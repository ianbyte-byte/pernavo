import json
import pytest
from chung_agent_swarm.handoff import parse_handoff_from_text, HandoffValidationError

def test_strict_summary_validation_success():
    text = json.dumps({
        "type": "handoff",
        "next_role": "Coder",
        "summary": {
            "progress": "done",
            "remaining": "todo",
            "risks": "none",
            "changes": "none"
        },
        "next_instructions": "go"
    })
    # Should not raise
    parse_handoff_from_text(text)

def test_strict_summary_validation_missing_field():
    text = json.dumps({
        "type": "handoff",
        "next_role": "Coder",
        "summary": {
            "progress": "done",
            "remaining": "todo",
            "risks": "none"
            # missing changes
        },
        "next_instructions": "go"
    })
    with pytest.raises(HandoffValidationError, match="Missing or invalid summary field \"changes\""):
        parse_handoff_from_text(text)

def test_strict_summary_validation_invalid_type():
    text = json.dumps({
        "type": "handoff",
        "next_role": "Coder",
        "summary": {
            "progress": "done",
            "remaining": "todo",
            "risks": "none",
            "changes": 123 # invalid type
        },
        "next_instructions": "go"
    })
    with pytest.raises(HandoffValidationError, match="Missing or invalid summary field \"changes\""):
        parse_handoff_from_text(text)
