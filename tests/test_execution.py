from uuid import uuid4
from runtime.execution import ToolExecution, ToolExecutionState, should_execute

def test_success_is_not_executed_twice():
    e=ToolExecution.prepare(uuid4(),"increment_counter",2)
    e.mark_succeeded({"counter": 1})
    assert not should_execute(e)

def test_ambiguous_crash_is_explicit():
    e=ToolExecution.prepare(uuid4(),"increment_counter",2)
    e.mark_uncertain()
    assert e.state is ToolExecutionState.UNCERTAIN
    assert not should_execute(e)
