from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class WaitSubscription:
    run_id: str
    correlation_key: str

@dataclass(frozen=True)
class RuntimeEvent:
    event_id: str
    correlation_key: str
    payload: dict[str, Any]

@dataclass
class EventInbox:
    subscriptions: dict[str, WaitSubscription] = field(default_factory=dict)
    consumed_event_ids: set[str] = field(default_factory=set)

    def subscribe(self, subscription: WaitSubscription) -> None:
        self.subscriptions[subscription.correlation_key] = subscription

    def deliver(self, event: RuntimeEvent) -> str | None:
        if event.event_id in self.consumed_event_ids:
            return None
        subscription=self.subscriptions.get(event.correlation_key)
        if subscription is None:
            return None
        self.consumed_event_ids.add(event.event_id)
        del self.subscriptions[event.correlation_key]
        return subscription.run_id
