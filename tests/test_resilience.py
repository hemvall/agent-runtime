import pytest
from runtime.resilience import with_retry

def test_transient_failure_recovers_with_bounded_retry():
    calls={"n":0}
    def flaky():
        calls["n"]+=1
        if calls["n"]<3: raise ConnectionError("temporary")
        return "ok"
    assert with_retry(flaky,sleep=lambda _:None)=="ok"
    assert calls["n"]==3

def test_permanent_failure_is_not_retried():
    calls={"n":0}
    def bad():
        calls["n"]+=1; raise ValueError("bad input")
    with pytest.raises(ValueError): with_retry(bad,sleep=lambda _:None)
    assert calls["n"]==1
