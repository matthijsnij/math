"""Per-category subtopic config (seeded from docs/other/subtopics.md)."""

from __future__ import annotations

from pathlib import Path

import yaml


class SubtopicStore:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def load(self) -> dict[str, list[str]]:
        if not self.path.exists():
            return {}
        return yaml.safe_load(self.path.read_text(encoding="utf-8")) or {}
