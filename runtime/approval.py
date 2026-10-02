from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Protocol
from runtime.contracts import ToolCall

class PolicyDecision(str, Enum):
    ALLOW="allow"
    DENY="deny"
    REQUIRE_APPROVAL="require_approval"

class Policy(Protocol):
    def evaluate(self, call: ToolCall) -> PolicyDecision: ...

@dataclass(frozen=True)
class PendingApproval:
    run_id: str
    call: ToolCall
    reason: str

class RiskyToolPolicy:
    def __init__(self, approval_tools: set[str], denied_tools: set[str] | None=None):
        self.approval_tools=approval_tools
        self.denied_tools=denied_tools or set()
    def evaluate(self, call: ToolCall) -> PolicyDecision:
        if call.name in self.denied_tools: return PolicyDecision.DENY
        if call.name in self.approval_tools: return PolicyDecision.REQUIRE_APPROVAL
        return PolicyDecision.ALLOW

def resolve_approval(pending: PendingApproval, approved: bool) -> tuple[ToolCall | None, str]:
    if approved: return pending.call, "human approved pending action"
    return None, f"human rejected {pending.call.name}"
