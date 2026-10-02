import pytest

from runtime.contracts import AgentDecision, Observation, ToolCall
from runtime.loop import StepBudgetExceeded, run_agent
from runtime.model import ModelAdapter
from runtime.tools import ToolRegistry


class ScriptedModel(ModelAdapter):
    def __init__(self, decisions: list[AgentDecision]) -> None:
        self.decisions = iter(decisions)

    def decide(self, goal: str, observations: list[Observation]) -> AgentDecision:
        return next(self.decisions)


def test_agent_executes_tool_then_completes() -> None:
    tools = ToolRegistry()
    tools.register("echo", lambda value: value)
    model = ScriptedModel([
        AgentDecision(kind="tool", tool_call=ToolCall(name="echo", arguments={"value": "hello"})),
        AgentDecision(kind="complete", final_answer="done"),
    ])

    result = run_agent("test", model, tools)

    assert result.final_answer == "done"
    assert result.observations[0].result.output == "hello"


def test_unknown_tool_becomes_observation_and_agent_can_recover() -> None:
    model = ScriptedModel([
        AgentDecision(kind="tool", tool_call=ToolCall(name="missing")),
        AgentDecision(kind="complete", final_answer="recovered"),
    ])

    result = run_agent("test", model, ToolRegistry())

    assert result.final_answer == "recovered"
    assert result.observations[0].result.ok is False
    assert "unknown tool" in result.observations[0].result.error


def test_tool_exception_becomes_observation() -> None:
    tools = ToolRegistry()

    def fail() -> None:
        raise RuntimeError("boom")

    tools.register("fail", fail)
    model = ScriptedModel([
        AgentDecision(kind="tool", tool_call=ToolCall(name="fail")),
        AgentDecision(kind="complete", final_answer="handled"),
    ])

    result = run_agent("test", model, tools)

    assert result.observations[0].result.error == "boom"


def test_step_budget_stops_infinite_loop() -> None:
    class LoopModel(ModelAdapter):
        def decide(self, goal: str, observations: list[Observation]) -> AgentDecision:
            return AgentDecision(kind="tool", tool_call=ToolCall(name="noop"))

    tools = ToolRegistry()
    tools.register("noop", lambda: None)

    with pytest.raises(StepBudgetExceeded):
        run_agent("loop forever", LoopModel(), tools, max_steps=3)
