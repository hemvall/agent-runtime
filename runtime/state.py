from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class RunState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    WAITING_EVENT = "waiting_event"
    FAILED = "failed"
    COMPLETED = "completed"


TERMINAL_STATES = frozenset({RunState.FAILED, RunState.COMPLETED})

ALLOWED_TRANSITIONS: dict[RunState, frozenset[RunState]] = {
    RunState.PENDING: frozenset({RunState.RUNNING, RunState.FAILED}),
    RunState.RUNNING: frozenset({
        RunState.WAITING_APPROVAL,
        RunState.WAITING_EVENT,
        RunState.FAILED,
        RunState.COMPLETED,
    }),
    RunState.WAITING_APPROVAL: frozenset({RunState.RUNNING, RunState.FAILED}),
    RunState.WAITING_EVENT: frozenset({RunState.RUNNING, RunState.FAILED}),
    RunState.FAILED: frozenset(),
    RunState.COMPLETED: frozenset(),
}


class InvalidStateTransition(ValueError):
    pass


@dataclass(frozen=True)
class StateTransition:
    previous_state: RunState
    next_state: RunState
    reason: str
    timestamp: datetime


@dataclass
class RunStateMachine:
    state: RunState = RunState.PENDING
    history: list[StateTransition] = field(default_factory=list)

    @property
    def is_terminal(self) -> bool:
        return self.state in TERMINAL_STATES

    def transition(self, next_state: RunState, reason: str) -> StateTransition:
        if not reason.strip():
            raise ValueError("state transitions require a reason")

        if next_state not in ALLOWED_TRANSITIONS[self.state]:
            raise InvalidStateTransition(
                f"cannot transition run from {self.state.value} to {next_state.value}"
            )

        transition = StateTransition(
            previous_state=self.state,
            next_state=next_state,
            reason=reason,
            timestamp=datetime.now(timezone.utc),
        )
        self.state = next_state
        self.history.append(transition)
        return transition
