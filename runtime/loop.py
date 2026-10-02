from __future__ import annotations

from dataclasses import dataclass, field

from runtime.contracts import Observation, ToolResult
from runtime.model import ModelAdapter
from runtime.tools import ToolRegistry


class StepBudgetExceeded(RuntimeError):
    pass


@dataclass
class RunResult:
    final_answer: str
    observations: list[Observation] = field(default_factory=list)


def run_agent(goal: str, model: ModelAdapter, tools: ToolRegistry, max_steps: int = 10) -> RunResult:
    observations: list[Observation] = []

    for step in range(1, max_steps + 1):
        decision = model.decide(goal, observations)
        if decision.kind == "complete":
            return RunResult(final_answer=decision.final_answer or "", observations=observations)

        call = decision.tool_call
        if call is None:
            raise ValueError("validated tool decision has no tool call")

        try:
            output = tools.execute(call.name, call.arguments)
            result = ToolResult(tool_name=call.name, ok=True, output=output)
        except Exception as exc:
            result = ToolResult(tool_name=call.name, ok=False, error=str(exc))

        observations.append(Observation(step=step, result=result))

    raise StepBudgetExceeded(f"agent exceeded max_steps={max_steps}")
