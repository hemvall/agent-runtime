from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4

class ToolExecutionState(str, Enum):
    PREPARED="prepared"
    SUCCEEDED="succeeded"
    FAILED="failed"
    UNCERTAIN="uncertain"

@dataclass
class ToolExecution:
    run_id: UUID
    tool_name: str
    idempotency_key: str
    state: ToolExecutionState = ToolExecutionState.PREPARED
    result: object | None = None

    @classmethod
    def prepare(cls, run_id: UUID, tool_name: str, step: int) -> "ToolExecution":
        return cls(run_id, tool_name, f"{run_id}:{step}:{tool_name}")

    def mark_succeeded(self, result: object) -> None:
        self.state, self.result = ToolExecutionState.SUCCEEDED, result

    def mark_uncertain(self) -> None:
        self.state = ToolExecutionState.UNCERTAIN

def should_execute(execution: ToolExecution) -> bool:
    return execution.state in {ToolExecutionState.PREPARED, ToolExecutionState.FAILED}
