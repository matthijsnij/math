"""Card store: single YAML file (see docs/adr/0001-yaml-file-storage-over-sqlite.md)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Card:
    id: str
    category: str
    subtopic: str
    level: int
    question: str
    answer: str


class CardStore:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def load(self) -> list[Card]:
        if not self.path.exists():
            return []
        raw = yaml.safe_load(self.path.read_text(encoding="utf-8")) or []
        return [Card(**entry) for entry in raw]
