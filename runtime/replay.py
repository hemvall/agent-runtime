from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class RecordedResult:
    kind:str
    key:str
    value:Any

class ReplayDivergence(RuntimeError): pass

class ReplayTape:
    def __init__(self, recorded:list[RecordedResult]):
        self.recorded=iter(recorded)
    def next(self,kind:str,key:str)->Any:
        try: item=next(self.recorded)
        except StopIteration as exc: raise ReplayDivergence("replay exhausted") from exc
        if (item.kind,item.key)!=(kind,key):
            raise ReplayDivergence(f"expected {item.kind}:{item.key}, got {kind}:{key}")
        return item.value
