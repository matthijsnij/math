"""Card store: single YAML file (see docs/adr/0001-yaml-file-storage-over-sqlite.md)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

from app.slugs import next_card_id


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

    def save(self, cards: list[Card]) -> None:
        raw = [asdict(card) for card in cards]
        self.path.write_text(
            yaml.safe_dump(raw, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )

    def add_card(self, category: str, subtopic: str, level: int, question: str, answer: str) -> Card:
        cards = self.load()
        card_id = next_card_id([c.id for c in cards], category, subtopic, level)
        card = Card(
            id=card_id,
            category=category,
            subtopic=subtopic,
            level=level,
            question=question,
            answer=answer,
        )
        cards.append(card)
        self.save(cards)
        return card

    def remove_card(self, card_id: str) -> bool:
        cards = self.load()
        remaining = [c for c in cards if c.id != card_id]
        removed = len(remaining) != len(cards)
        if removed:
            self.save(remaining)
        return removed

    def filter_cards(
        self,
        categories: list[str] | None = None,
        subtopics: list[str] | None = None,
        levels: list[int] | None = None,
    ) -> list[Card]:
        cards = self.load()
        if categories:
            cards = [c for c in cards if c.category in categories]
        if subtopics:
            cards = [c for c in cards if c.subtopic in subtopics]
        if levels:
            cards = [c for c in cards if c.level in levels]
        return cards
