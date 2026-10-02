"""Whole-file integrity checks for data/cards.yaml (see docs/agents/card-writing.md)."""

from __future__ import annotations

from pathlib import Path

from app.categories import CATEGORIES, LEVELS
from app.slugs import slugify
from app.storage import CardStore
from app.subtopics import SubtopicStore

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _cards():
    return CardStore(DATA_DIR / "cards.yaml").load()


def _subtopics():
    return SubtopicStore(DATA_DIR / "subtopics.yaml").load()


def test_card_ids_are_unique():
    cards = _cards()
    ids = [card.id for card in cards]
    duplicates = {card_id for card_id in ids if ids.count(card_id) > 1}
    assert not duplicates, f"duplicate card ids: {sorted(duplicates)}"


def test_card_category_and_level_are_valid():
    for card in _cards():
        assert card.category in CATEGORIES, f"{card.id}: invalid category '{card.category}'"
        assert card.level in LEVELS, f"{card.id}: invalid level '{card.level}'"


def test_card_subtopic_is_registered():
    subtopics = _subtopics()
    for card in _cards():
        bucket = subtopics.get(card.category, [])
        assert card.subtopic in bucket, (
            f"{card.id}: subtopic '{card.subtopic}' not registered under "
            f"'{card.category}' in data/subtopics.yaml"
        )


def test_card_id_matches_category_subtopic_level():
    for card in _cards():
        prefix = f"{slugify(card.category)}-{slugify(card.subtopic)}-{card.level}-"
        assert card.id.startswith(prefix), (
            f"{card.id}: id doesn't match its category/subtopic/level (expected prefix '{prefix}')"
        )


def test_card_question_and_answer_are_non_empty():
    for card in _cards():
        assert card.question.strip(), f"{card.id}: empty question"
        assert card.answer.strip(), f"{card.id}: empty answer"
