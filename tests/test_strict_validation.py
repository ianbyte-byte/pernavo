from __future__ import annotations

import json
import pytest

from chung_agent_swarm.handoff import (
    HandoffValidationError,
    parse_handoff_from_text,
)


def test_valid_enhanced_summary() -> None:
    text = json.dumps({
        "type": "handoff",
        "next_role": "Coder",
        "summary": {
            "progress": "Task A done",
            "remaining": "Task B pending",
            "risks": "None",
            "changes": "Modified src/handoff.py"
        },
        "next_instructions": "Implement strict validation"
    })
    # Should not raise
    parse_handoff_from_text(text)


def test_invalid_enhanced_summary_missing_key() -> None:
    text = json.dumps({
        "type": "handoff",
        "next_role": "Coder",
        "summary": {
            "progress": "Task A done",
            "remaining": "Task B pending",
            "risks": "None"
            # "changes" is missing
        },
        "next_instructions": "Implement strict validation"
    })
    with pytest.raises(HandoffValidationError, match='Summary object must contain "changes" as a string.'):
        parse_handoff_from_text(text)


def test_invalid_enhanced_summary_wrong_type() -> None:
    text = json.dumps({
        "type": "handoff",
        "next_role": "Coder",
        "summary": {
            "progress": "Task A done",
            "remaining": "Task B pending",
            "risks": "None",
            "changes": ["Modified src/handoff.py"] # Should be string
        },
        "next_instructions": "Implement strict validation"
    })
    with pytest.raises(HandoffValidationError, match='Summary object must contain "changes" as a string.'):
        parse_handoff_from_text(text)
