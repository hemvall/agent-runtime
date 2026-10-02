from runtime.benchmark import engineering_agent_chaos_benchmark

def test_graduation_chaos_invariants():
    r=engineering_agent_chaos_benchmark()
    assert r.completed
    assert r.duplicate_protected_side_effects==0
    assert r.waiting_used_worker is False
    assert r.faults_recovered>=2
    assert {e.kind for e in r.trace.events}>={"crash","retry","waiting_approval","approval","complete"}
