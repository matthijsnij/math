"""Whole-file integrity checks for data/cards.yaml (see docs/agents/card-writing.md)."""

from __future__ import annotations

import re
from pathlib import Path

from cardlib.categories import CATEGORIES, LEVELS
from cardlib.slugs import slugify
from cardlib.storage import CardStore
from cardlib.subtopics import SubtopicStore

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


def test_includegraphics_paths_point_to_existing_graph_files():
    pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}")
    for card in _cards():
        for path in pattern.findall(card.question + card.answer):
            assert path.startswith("graphs/"), f"{card.id}: image path '{path}' must start with graphs/"
            assert (DATA_DIR / path).is_file(), f"{card.id}: missing image file data/{path}"
