from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Iterable
from runtime.state import RunState

class ResumeAction(str, Enum):
    START = "start"
    CONTINUE = "continue"
    WAIT = "wait"
    STOP = "stop"

@dataclass(frozen=True)
class Checkpoint:
    run_id: str
    completed_step: int
    state: RunState

def resume_from(checkpoint: Checkpoint | None) -> tuple[ResumeAction, int]:
    if checkpoint is None:
        return ResumeAction.START, 1
    if checkpoint.state in {RunState.COMPLETED, RunState.FAILED}:
        return ResumeAction.STOP, checkpoint.completed_step
    if checkpoint.state in {RunState.WAITING_APPROVAL, RunState.WAITING_EVENT}:
        return ResumeAction.WAIT, checkpoint.completed_step + 1
    return ResumeAction.CONTINUE, checkpoint.completed_step + 1

def unfinished(checkpoints: Iterable[Checkpoint]) -> list[Checkpoint]:
    return [c for c in checkpoints if c.state not in {RunState.COMPLETED, RunState.FAILED}]
