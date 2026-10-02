from runtime.tracing import RunTrace, redact

def test_trace_correlates_events_and_redacts_secret():
    t=RunTrace("r1"); t.record("model",duration=.2); t.record("tool",duration=.4,error="boom")
    assert all(e.run_id=="r1" for e in t.events)
    assert t.duration_by_kind()["tool"]==.4
    assert redact("token=abc",{"abc"})=="token=[REDACTED]"
