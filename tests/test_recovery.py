from runtime.recovery import Checkpoint, ResumeAction, resume_from
from runtime.state import RunState

def test_resume_continues_after_last_safe_step():
    action, step = resume_from(Checkpoint("r1", 3, RunState.RUNNING))
    assert (action, step) == (ResumeAction.CONTINUE, 4)

def test_terminal_checkpoint_never_restarts():
    action, step = resume_from(Checkpoint("r1", 7, RunState.COMPLETED))
    assert action is ResumeAction.STOP
    assert step == 7
