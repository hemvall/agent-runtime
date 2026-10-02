from __future__ import annotations
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, TypeVar

T=TypeVar("T")
class FailureKind(str, Enum):
    RETRYABLE="retryable"; PERMANENT="permanent"; POLICY="policy"; HUMAN_REQUIRED="human_required"

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int=3
    base_delay: float=0.05

def classify(exc: Exception) -> FailureKind:
    if isinstance(exc,(TimeoutError,ConnectionError)): return FailureKind.RETRYABLE
    if isinstance(exc,PermissionError): return FailureKind.POLICY
    return FailureKind.PERMANENT

def with_retry(fn: Callable[[],T], policy: RetryPolicy=RetryPolicy(), sleep: Callable[[float],None]=time.sleep) -> T:
    last: Exception | None=None
    for attempt in range(policy.max_attempts):
        try: return fn()
        except Exception as exc:
            last=exc
            if classify(exc) is not FailureKind.RETRYABLE or attempt+1>=policy.max_attempts: raise
            sleep(policy.base_delay*(2**attempt))
    raise last or RuntimeError("retry failed")
