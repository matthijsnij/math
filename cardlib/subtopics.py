"""Per-category subtopic config (seeded from docs/other/subtopics.md); extensible via Add flow."""

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

    def save(self, data: dict[str, list[str]]) -> None:
        self.path.write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )

    def ensure_subtopic(self, category: str, subtopic: str) -> bool:
        data = self.load()
        bucket = data.setdefault(category, [])
        if subtopic in bucket:
            return False
        bucket.append(subtopic)
        self.save(data)
        return True
