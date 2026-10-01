from __future__ import annotations

import argparse
import json

from pydantic import ValidationError

from runtime.model import DemoModelAdapter, ModelAdapter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-runtime")
    parser.add_argument("goal", help="Task goal to submit to the runtime")
    return parser


def run(goal: str, adapter: ModelAdapter | None = None) -> int:
    model = adapter or DemoModelAdapter()

    try:
        decision = model.decide(goal)
    except ValidationError as exc:
        print(json.dumps({"error": "invalid_model_output", "details": exc.errors()}))
        return 2

    print(decision.model_dump_json())
    return 0


def main() -> None:
    args = build_parser().parse_args()
    raise SystemExit(run(args.goal))


if __name__ == "__main__":
    main()
