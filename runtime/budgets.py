from __future__ import annotations
from collections import Counter
from dataclasses import dataclass, field
from time import monotonic

class BudgetExceeded(RuntimeError): pass

@dataclass(frozen=True)
class BudgetLimits:
    max_steps:int=50
    max_tool_calls:int=30
    max_tokens:int=100_000
    max_cost:float=10.0
    max_wall_seconds:float=900.0
    max_identical_actions:int=3

@dataclass
class Budget:
    limits:BudgetLimits
    started_at:float=field(default_factory=monotonic)
    steps:int=0; tool_calls:int=0; tokens:int=0; cost:float=0.0
    actions:Counter[str]=field(default_factory=Counter)

    def charge(self, *, steps=0, tool_calls=0, tokens=0, cost=0.0, action:str|None=None, now:float|None=None)->None:
        self.steps+=steps; self.tool_calls+=tool_calls; self.tokens+=tokens; self.cost+=cost
        if action: self.actions[action]+=1
        elapsed=(now if now is not None else monotonic())-self.started_at
        checks=[(self.steps>self.limits.max_steps,"steps"),(self.tool_calls>self.limits.max_tool_calls,"tool calls"),(self.tokens>self.limits.max_tokens,"tokens"),(self.cost>self.limits.max_cost,"cost"),(elapsed>self.limits.max_wall_seconds,"deadline")]
        if action: checks.append((self.actions[action]>self.limits.max_identical_actions,"repeated action"))
        for exceeded,name in checks:
            if exceeded: raise BudgetExceeded(f"{name} budget exceeded")
