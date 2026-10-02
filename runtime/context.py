from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class ContextItem:
    key: str
    text: str
    tokens: int
    priority: int = 0

@dataclass(frozen=True)
class ModelContext:
    items: tuple[ContextItem, ...]
    token_count: int

class ContextBuilder:
    def __init__(self, token_budget: int):
        self.token_budget=token_budget

    def build(self, durable: Iterable[ContextItem], recent: Iterable[ContextItem]) -> ModelContext:
        candidates=list(durable)+list(recent)
        candidates.sort(key=lambda x:(-x.priority,x.key))
        selected=[]; used=0
        for item in candidates:
            if used+item.tokens <= self.token_budget:
                selected.append(item); used+=item.tokens
        return ModelContext(tuple(selected),used)
