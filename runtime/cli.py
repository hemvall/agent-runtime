from __future__ import annotations

import argparse
import json

from pydantic import ValidationError

from runtime.loop import StepBudgetExceeded, run_agent
from runtime.model import DemoModelAdapter, ModelAdapter
from runtime.tools import ToolRegistry, default_registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-runtime")
    parser.add_argument("goal", help="Task goal to submit to the runtime")
    parser.add_argument("--max-steps", type=int, default=10)
    return parser


def run(
    goal: str,
    adapter: ModelAdapter | None = None,
    tools: ToolRegistry | None = None,
    max_steps: int = 10,
) -> int:
    model = adapter or DemoModelAdapter()
    registry = tools or default_registry()

    try:
        result = run_agent(goal, model, registry, max_steps=max_steps)
    except ValidationError as exc:
        print(json.dumps({"error": "invalid_model_output", "details": exc.errors()}))
        return 2
    except StepBudgetExceeded as exc:
        print(json.dumps({"error": "step_budget_exceeded", "details": str(exc)}))
        return 3

    print(json.dumps({"final_answer": result.final_answer, "steps": len(result.observations)}))
    return 0


def main() -> None:
    args = build_parser().parse_args()
    raise SystemExit(run(args.goal, max_steps=args.max_steps))


if __name__ == "__main__":
    main()
