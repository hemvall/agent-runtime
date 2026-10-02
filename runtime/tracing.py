from __future__ import annotations
from dataclasses import dataclass, field
from time import time
from typing import Any

REDACTED="[REDACTED]"

def redact(value: Any, secrets: set[str]) -> Any:
    text=str(value)
    for secret in secrets:
        if secret: text=text.replace(secret,REDACTED)
    return text

@dataclass(frozen=True)
class TraceEvent:
    run_id:str; kind:str; timestamp:float; data:dict[str,Any]

@dataclass
class RunTrace:
    run_id:str
    events:list[TraceEvent]=field(default_factory=list)
    def record(self,kind:str,**data:Any)->None:
        self.events.append(TraceEvent(self.run_id,kind,time(),data))
    def duration_by_kind(self)->dict[str,float]:
        totals:dict[str,float]={}
        for e in self.events: totals[e.kind]=totals.get(e.kind,0.0)+float(e.data.get("duration",0))
        return totals
