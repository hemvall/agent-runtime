from __future__ import annotations

import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

Tool = Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, name: str, tool: Tool) -> None:
        self._tools[name] = tool

    def execute(self, name: str, arguments: dict[str, Any]) -> Any:
        tool = self._tools.get(name)
        if tool is None:
            raise KeyError(f"unknown tool: {name}")
        return tool(**arguments)


def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_file(path: str, content: str) -> str:
    Path(path).write_text(content, encoding="utf-8")
    return path


def shell(command: str) -> str:
    completed = subprocess.run(command, shell=True, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"command exited {completed.returncode}")
    return completed.stdout


def default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("read_file", read_file)
    registry.register("write_file", write_file)
    registry.register("shell", shell)
    return registry
