from runtime.events import EventInbox, RuntimeEvent, WaitSubscription

def test_only_matching_event_wakes_run_once():
    inbox=EventInbox()
    inbox.subscribe(WaitSubscription("run-1","payment:42"))
    assert inbox.deliver(RuntimeEvent("e0","other",{})) is None
    event=RuntimeEvent("e1","payment:42",{"paid":True})
    assert inbox.deliver(event)=="run-1"
    assert inbox.deliver(event) is None
