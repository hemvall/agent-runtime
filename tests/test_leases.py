from datetime import datetime,timedelta,timezone
from runtime.leases import LeaseRegistry

def test_one_worker_owns_run_and_dead_lease_recovers():
    now=datetime.now(timezone.utc); leases=LeaseRegistry()
    assert leases.acquire("r","a",timedelta(seconds=5),now)
    assert not leases.acquire("r","b",timedelta(seconds=5),now)
    assert leases.acquire("r","b",timedelta(seconds=5),now+timedelta(seconds=6))
