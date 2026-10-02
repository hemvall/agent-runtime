from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import shlex

class SandboxViolation(PermissionError): pass

@dataclass(frozen=True)
class SandboxPolicy:
    workspace:Path
    allowed_commands:frozenset[str]=frozenset({"pytest","python","git"})

    def path(self,requested:str)->Path:
        root=self.workspace.resolve(); target=(root/requested).resolve()
        if target!=root and root not in target.parents: raise SandboxViolation("path escapes workspace")
        return target

    def command(self,command:str)->list[str]:
        parts=shlex.split(command)
        if not parts or parts[0] not in self.allowed_commands: raise SandboxViolation("command not allowed")
        if any(token in {"&&","||",";","|"} for token in parts): raise SandboxViolation("shell chaining not allowed")
        return parts

def inject_secrets(names:set[str],vault:dict[str,str])->dict[str,str]:
    return {name:vault[name] for name in names}

def redact_secrets(text:str,secrets:dict[str,str])->str:
    for value in secrets.values(): text=text.replace(value,"[REDACTED]")
    return text
