from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class Fault(str, Enum):
    WORKER_CRASH="worker_crash"; DATABASE_DOWN="database_down"; TOOL_TIMEOUT="tool_timeout"
    DUPLICATE_WEBHOOK="duplicate_webhook"; MALFORMED_MODEL="malformed_model"; EXTERNAL_429="external_429"; EXTERNAL_500="external_500"

@dataclass(frozen=True)
class Invariant:
    fault:Fault; protected_side_effects_not_duplicated:bool=True; state_inspectable:bool=True

RECOVERY_MATRIX={fault:Invariant(fault) for fault in Fault}

def inject(fault:Fault)->Exception:
    if fault is Fault.TOOL_TIMEOUT: return TimeoutError("injected tool timeout")
    if fault in {Fault.EXTERNAL_429,Fault.EXTERNAL_500,Fault.DATABASE_DOWN}: return ConnectionError(f"injected {fault.value}")
    return RuntimeError(f"injected {fault.value}")
