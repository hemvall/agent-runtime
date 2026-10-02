from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass(frozen=True)
class DurableTimer:
    run_id: str
    wake_at: datetime
    timer_id: str

@dataclass
class TimerQueue:
    timers: dict[str, DurableTimer] = field(default_factory=dict)
    claimed: set[str] = field(default_factory=set)

    def schedule(self, timer: DurableTimer) -> None:
        self.timers[timer.timer_id]=timer

    def claim_due(self, now: datetime | None=None) -> list[str]:
        now=now or datetime.now(timezone.utc)
        due=[]
        for timer_id,timer in self.timers.items():
            if timer.wake_at <= now and timer_id not in self.claimed:
                self.claimed.add(timer_id)
                due.append(timer.run_id)
        return due
