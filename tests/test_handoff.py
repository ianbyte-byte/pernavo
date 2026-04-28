import json
import pytest
from chung_agent_swarm.handoff import (
    AgentRole,
    parse_handoff_from_text,
    format_handoff,
    HandoffValidationError,
    HandoffParseError
)

def test_parse_simple_handoff():
    text = """
    Some text before
    {
      "type": "handoff",
      "next_role": "Coder",
      "summary": "Done basic setup",
      "next_instructions": "Implement the feature"
    }
    Some text after
    """
    envelope = parse_handoff_from_text(text)
    assert envelope.next_role == AgentRole.CODER
    assert envelope.summary.progress == "Done basic setup"
    assert envelope.summary.remaining == "N/A"
    assert envelope.next_instructions == "Implement the feature"
    assert envelope.context.risk_level == "low"

def test_parse_enhanced_handoff():
    text = {
        "type": "handoff",
        "next_role": "Reviewer",
        "summary": {
            "progress": "Implemented auth",
            "remaining": "Testing",
            "risks": "None",
            "changes": "src/auth.py"
        },
        "acceptance_criteria": ["Code review passed", "Tests green"],
        "next_instructions": "Please review",
        "context": {
            "platform_api_needed": True,
            "session_config_updated": True,
            "test_coverage_required": "full",
            "risk_level": "medium"
        }
    }
    envelope = parse_handoff_from_text(json.dumps(text))
    assert envelope.next_role == AgentRole.REVIEWER
    assert envelope.summary.progress == "Implemented auth"
    assert envelope.summary.changes == "src/auth.py"
    assert "Code review passed" in envelope.acceptance_criteria
    assert envelope.context.platform_api_needed is True
    assert envelope.context.risk_level == "medium"

def test_parse_specialist_roles():
    roles = ["Architect", "SecurityReviewer", "Debugger", "Refactorer"]
    for role in roles:
        text = {
            "type": "handoff",
            "next_role": role,
            "summary": "Switching role",
            "next_instructions": "Proceed"
        }
        envelope = parse_handoff_from_text(json.dumps(text))
        assert envelope.next_role.value == role

def test_invalid_json():
    with pytest.raises(HandoffParseError):
        parse_handoff_from_text("Not a JSON")

def test_missing_fields():
    with pytest.raises(HandoffValidationError):
        parse_handoff_from_text(json.dumps({"type": "handoff"}))

def test_format_handoff():
    text = {
        "type": "handoff",
        "next_role": "Coder",
        "summary": "Test summary",
        "next_instructions": "Test instructions"
    }
    envelope = parse_handoff_from_text(json.dumps(text))
    formatted = format_handoff(envelope)
    data = json.loads(formatted)
    assert data["type"] == "handoff"
    assert data["next_role"] == "Coder"
    assert data["summary"]["progress"] == "Test summary"
    assert data["context"]["risk_level"] == "low"
