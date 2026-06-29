from __future__ import annotations

import json
import pytest

from chung_agent_swarm.handoff import (
    HandoffValidationError,
    parse_handoff_from_text,
)

def test_strict_summary_object_validation() -> None:
    # Missing 'changes' field
    text = json.dumps(
        {
            "type": "handoff",
            "next_role": "Coder",
            "summary": {
                "progress": "done something",
                "remaining": "do more",
                "risks": "none"
            },
            "next_instructions": "go ahead"
        }
    )
    with pytest.raises(HandoffValidationError, match="Summary object missing or invalid field 'changes'"):
        parse_handoff_from_text(text)

def test_strict_summary_object_invalid_type() -> None:
    # 'progress' is not a string
    text = json.dumps(
        {
            "type": "handoff",
            "next_role": "Coder",
            "summary": {
                "progress": 123,
                "remaining": "do more",
                "risks": "none",
                "changes": "none"
            },
            "next_instructions": "go ahead"
        }
    )
    with pytest.raises(HandoffValidationError, match="Summary object missing or invalid field 'progress'"):
        parse_handoff_from_text(text)
