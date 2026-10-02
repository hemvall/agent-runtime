from __future__ import annotations
from dataclasses import asdict, dataclass
import json
from typing import Callable

@dataclass(frozen=True)
class GoldenTask:
    id:str; goal:str; expected:str

@dataclass(frozen=True)
class EvalResult:
    task_id:str; success:bool; steps:int; tool_calls:int; latency_ms:int; cost:float

def evaluate(task:GoldenTask, runner:Callable[[str],tuple[str,dict]])->EvalResult:
    answer,m=runner(task.goal)
    return EvalResult(task.id,task.expected in answer,int(m.get("steps",0)),int(m.get("tool_calls",0)),int(m.get("latency_ms",0)),float(m.get("cost",0)))

def to_json(results:list[EvalResult])->str:
    return json.dumps([asdict(r) for r in results],sort_keys=True)
