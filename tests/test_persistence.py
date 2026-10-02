from uuid import uuid4

from runtime.persistence import PersistedRun
from runtime.state import RunState


def test_persisted_run_keeps_authoritative_lifecycle_state() -> None:
    run_id = uuid4()
    run = PersistedRun(id=run_id, goal="fix tests", state=RunState.RUNNING)

    assert run.id == run_id
    assert run.goal == "fix tests"
    assert run.state is RunState.RUNNING
