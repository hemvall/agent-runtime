from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class SubtaskStatus(str, Enum):
    PENDING="pending"; RUNNING="running"; COMPLETED="completed"; FAILED="failed"; BLOCKED="blocked"

@dataclass
class Subtask:
    id: str
    description: str
    dependencies: set[str]=field(default_factory=set)
    status: SubtaskStatus=SubtaskStatus.PENDING

@dataclass
class Plan:
    version: int
    subtasks: dict[str,Subtask]

    def runnable(self) -> list[Subtask]:
        done={k for k,v in self.subtasks.items() if v.status is SubtaskStatus.COMPLETED}
        return [s for s in self.subtasks.values() if s.status is SubtaskStatus.PENDING and s.dependencies<=done]

    def set_status(self, subtask_id: str, status: SubtaskStatus) -> None:
        self.subtasks[subtask_id].status=status

    def replan(self, replacements: list[Subtask]) -> None:
        self.version+=1
        self.subtasks={s.id:s for s in replacements}
