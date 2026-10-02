from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable

@dataclass(frozen=True)
class Compaction:
    version: int
    summary: str
    source_digest: str

def compact(texts: Iterable[str], version: int=1, max_chars: int=1000) -> Compaction:
    original=list(texts)
    joined="\n".join(original)
    digest=sha256(joined.encode()).hexdigest()
    summary=joined if len(joined)<=max_chars else joined[:max_chars-3]+"..."
    return Compaction(version,summary,digest)

def authoritative_fact(structured_state: dict[str, object], key: str) -> object:
    if key not in structured_state:
        raise KeyError(key)
    return structured_state[key]
