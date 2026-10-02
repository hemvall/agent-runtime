from datetime import datetime, timedelta, timezone
from runtime.timers import DurableTimer, TimerQueue

def test_due_timer_is_claimed_once():
    q=TimerQueue()
    now=datetime.now(timezone.utc)
    q.schedule(DurableTimer("r1",now-timedelta(seconds=1),"t1"))
    assert q.claim_due(now)==["r1"]
    assert q.claim_due(now)==[]
