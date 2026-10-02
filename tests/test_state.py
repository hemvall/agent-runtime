from datetime import timezone

import pytest

from runtime.state import InvalidStateTransition, RunState, RunStateMachine


def test_valid_transitions_are_recorded_with_reason_and_timestamp() -> None:
    machine = RunStateMachine()

    started = machine.transition(RunState.RUNNING, "worker started the run")
    waiting = machine.transition(RunState.WAITING_APPROVAL, "merge requires human approval")
    resumed = machine.transition(RunState.RUNNING, "human approved the merge")
    completed = machine.transition(RunState.COMPLETED, "goal completed")

    assert machine.state is RunState.COMPLETED
    assert machine.is_terminal is True
    assert machine.history == [started, waiting, resumed, completed]
    assert started.previous_state is RunState.PENDING
    assert started.next_state is RunState.RUNNING
    assert waiting.reason == "merge requires human approval"
    assert all(item.timestamp.tzinfo is timezone.utc for item in machine.history)


def test_illegal_transition_is_rejected_without_mutating_state() -> None:
    machine = RunStateMachine()

    with pytest.raises(InvalidStateTransition, match="pending to completed"):
        machine.transition(RunState.COMPLETED, "skip execution")

    assert machine.state is RunState.PENDING
    assert machine.history == []


@pytest.mark.parametrize("terminal_state", [RunState.COMPLETED, RunState.FAILED])
def test_terminal_run_cannot_restart(terminal_state: RunState) -> None:
    machine = RunStateMachine()
    machine.transition(RunState.RUNNING, "run started")
    machine.transition(terminal_state, "run ended")

    with pytest.raises(InvalidStateTransition):
        machine.transition(RunState.RUNNING, "try to restart")

    assert machine.state is terminal_state


def test_transition_requires_a_reason() -> None:
    machine = RunStateMachine()

    with pytest.raises(ValueError, match="require a reason"):
        machine.transition(RunState.RUNNING, "   ")
