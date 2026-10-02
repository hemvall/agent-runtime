from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol
from uuid import UUID

from runtime.state import RunState


SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id UUID PRIMARY KEY,
    goal TEXT NOT NULL,
    state TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS steps (
    run_id UUID NOT NULL REFERENCES runs(id),
    step INTEGER NOT NULL,
    observation JSONB NOT NULL,
    PRIMARY KEY (run_id, step)
);
CREATE TABLE IF NOT EXISTS state_transitions (
    run_id UUID NOT NULL REFERENCES runs(id),
    sequence BIGSERIAL,
    previous_state TEXT NOT NULL,
    next_state TEXT NOT NULL,
    reason TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (run_id, sequence)
);
CREATE TABLE IF NOT EXISTS tool_calls (
    id UUID PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES runs(id),
    step INTEGER NOT NULL,
    tool_name TEXT NOT NULL,
    arguments JSONB NOT NULL,
    result JSONB,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS artifacts (
    id UUID PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES runs(id),
    kind TEXT NOT NULL,
    reference TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);
"""


@dataclass(frozen=True)
class PersistedRun:
    id: UUID
    goal: str
    state: RunState


class RunStore(Protocol):
    def create_run(self, run: PersistedRun) -> None: ...
    def set_state(self, run_id: UUID, state: RunState) -> None: ...
    def append_step(self, run_id: UUID, step: int, observation: dict[str, Any]) -> None: ...
    def load_run(self, run_id: UUID) -> PersistedRun: ...
    def load_steps(self, run_id: UUID) -> list[dict[str, Any]]: ...


class PostgresRunStore:
    """Small synchronous PostgreSQL repository; runtime state is authoritative here."""

    def __init__(self, connection: Any) -> None:
        self.connection = connection

    def initialize(self) -> None:
        with self.connection.cursor() as cur:
            cur.execute(SCHEMA)
        self.connection.commit()

    def create_run(self, run: PersistedRun) -> None:
        with self.connection.cursor() as cur:
            cur.execute(
                "INSERT INTO runs (id, goal, state) VALUES (%s, %s, %s)",
                (run.id, run.goal, run.state.value),
            )
        self.connection.commit()

    def set_state(self, run_id: UUID, state: RunState) -> None:
        with self.connection.cursor() as cur:
            cur.execute(
                "UPDATE runs SET state=%s, updated_at=now() WHERE id=%s",
                (state.value, run_id),
            )
        self.connection.commit()

    def append_step(self, run_id: UUID, step: int, observation: dict[str, Any]) -> None:
        with self.connection.cursor() as cur:
            cur.execute(
                "INSERT INTO steps (run_id, step, observation) VALUES (%s, %s, %s::jsonb)",
                (run_id, step, json.dumps(observation)),
            )
        self.connection.commit()

    def load_run(self, run_id: UUID) -> PersistedRun:
        with self.connection.cursor() as cur:
            cur.execute("SELECT id, goal, state FROM runs WHERE id=%s", (run_id,))
            row = cur.fetchone()
        if row is None:
            raise KeyError(f"unknown run: {run_id}")
        return PersistedRun(id=row[0], goal=row[1], state=RunState(row[2]))

    def load_steps(self, run_id: UUID) -> list[dict[str, Any]]:
        with self.connection.cursor() as cur:
            cur.execute(
                "SELECT observation FROM steps WHERE run_id=%s ORDER BY step",
                (run_id,),
            )
            return [row[0] for row in cur.fetchall()]
