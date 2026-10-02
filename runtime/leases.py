from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

@dataclass
class Lease:
    run_id:str; owner:str; expires_at:datetime
    def expired(self,now:datetime)->bool: return now>=self.expires_at

class LeaseRegistry:
    def __init__(self): self._leases:dict[str,Lease]={}
    def acquire(self,run_id:str,owner:str,ttl:timedelta,now:datetime|None=None)->bool:
        now=now or datetime.now(timezone.utc); current=self._leases.get(run_id)
        if current and not current.expired(now) and current.owner!=owner: return False
        self._leases[run_id]=Lease(run_id,owner,now+ttl); return True
    def renew(self,run_id:str,owner:str,ttl:timedelta,now:datetime|None=None)->bool:
        now=now or datetime.now(timezone.utc); current=self._leases.get(run_id)
        if not current or current.owner!=owner or current.expired(now): return False
        current.expires_at=now+ttl; return True
