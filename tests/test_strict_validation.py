from __future__ import annotations

import json
import pytest
from chung_agent_swarm.handoff import parse_handoff_from_text, HandoffValidationError

def test_enhanced_handoff_validation_missing_keys():
    text = json.dumps({
        "type": "handoff",
        "next_role": "Coder",
        "summary": {
            "progress": "done something",
            # missing remaining, risks, changes
        },
        "next_instructions": "go ahead"
    })
    with pytest.raises(HandoffValidationError, match="Missing mandatory keys in summary object"):
        parse_handoff_from_text(text)

def test_enhanced_handoff_validation_invalid_type():
    text = json.dumps({
        "type": "handoff",
        "next_role": "Coder",
        "summary": {
            "progress": "done something",
            "remaining": "do more",
            "risks": "none",
            "changes": 123  # should be string
        },
        "next_instructions": "go ahead"
    })
    with pytest.raises(HandoffValidationError, match="Summary key 'changes' must be a string"):
        parse_handoff_from_text(text)

def test_enhanced_handoff_validation_success():
    text = json.dumps({
        "type": "handoff",
        "next_role": "Coder",
        "summary": {
            "progress": "done something",
            "remaining": "do more",
            "risks": "none",
            "changes": "src/x.py"
        },
        "next_instructions": "go ahead"
    })
    parsed = parse_handoff_from_text(text)
    assert parsed.summary["progress"] == "done something"
