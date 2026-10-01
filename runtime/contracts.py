from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tool_name: str = Field(min_length=1)
    ok: bool
    output: Any | None = None
    error: str | None = None


class AgentDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["tool", "complete"]
    tool_call: ToolCall | None = None
    final_answer: str | None = None

    def model_post_init(self, __context: Any) -> None:
        if self.kind == "tool":
            if self.tool_call is None:
                raise ValueError("tool decisions require tool_call")
            if self.final_answer is not None:
                raise ValueError("tool decisions cannot include final_answer")
        if self.kind == "complete":
            if self.final_answer is None:
                raise ValueError("complete decisions require final_answer")
            if self.tool_call is not None:
                raise ValueError("complete decisions cannot include tool_call")
