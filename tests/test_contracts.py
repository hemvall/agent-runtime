import pytest
from pydantic import ValidationError

from runtime.contracts import AgentDecision, ToolCall, ToolResult


def test_tool_call_defaults_arguments() -> None:
    call = ToolCall(name="read_file")
    assert call.arguments == {}


def test_tool_result_accepts_success() -> None:
    result = ToolResult(tool_name="read_file", ok=True, output="hello")
    assert result.ok is True
    assert result.error is None


def test_tool_decision_requires_tool_call() -> None:
    with pytest.raises(ValidationError):
        AgentDecision(kind="tool")


def test_complete_decision_requires_final_answer() -> None:
    with pytest.raises(ValidationError):
        AgentDecision(kind="complete")


def test_complete_decision_rejects_tool_call() -> None:
    with pytest.raises(ValidationError):
        AgentDecision(
            kind="complete",
            final_answer="done",
            tool_call=ToolCall(name="read_file"),
        )


def test_extra_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        ToolCall(name="read_file", unexpected=True)
