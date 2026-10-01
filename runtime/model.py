from __future__ import annotations

from abc import ABC, abstractmethod

from runtime.contracts import AgentDecision


class ModelAdapter(ABC):
    """Provider-independent boundary between the runtime and an LLM."""

    @abstractmethod
    def decide(self, goal: str) -> AgentDecision:
        """Return the next validated decision for a goal."""
        raise NotImplementedError


class DemoModelAdapter(ModelAdapter):
    """Deterministic adapter used for local smoke tests before wiring a real provider."""

    def decide(self, goal: str) -> AgentDecision:
        return AgentDecision(
            kind="complete",
            final_answer=f"Demo decision for: {goal}",
        )
