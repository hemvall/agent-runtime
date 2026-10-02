import pytest
from runtime.replay import RecordedResult, ReplayDivergence, ReplayTape

def test_replay_returns_recorded_value_without_external_call():
    tape=ReplayTape([RecordedResult("tool","read_file",{"ok":True})])
    assert tape.next("tool","read_file")=={"ok":True}

def test_replay_reports_divergence():
    tape=ReplayTape([RecordedResult("model","step-1","x")])
    with pytest.raises(ReplayDivergence): tape.next("tool","step-1")
