"""Add-flow validation: pasted YAML list of card entries -> (added cards, per-entry errors)."""

from __future__ import annotations

import yaml

from app.categories import CATEGORIES, LEVELS
from app.storage import Card, CardStore
from app.subtopics import SubtopicStore

REQUIRED_FIELDS = ("category", "subtopic", "level", "question", "answer")


def _validate_entry(entry: object, index: int) -> str | None:
    if not isinstance(entry, dict):
        return f"entry {index}: must be a mapping of category/subtopic/level/question/answer"
    for field in REQUIRED_FIELDS:
        if field not in entry or entry[field] in (None, ""):
            return f"entry {index}: missing required field '{field}'"
    if entry["category"] not in CATEGORIES:
        return f"entry {index}: invalid category '{entry['category']}'"
    if entry["level"] not in LEVELS:
        return f"entry {index}: invalid level '{entry['level']}' (must be 1-4)"
    return None


def process_paste(
    yaml_text: str, card_store: CardStore, subtopic_store: SubtopicStore
) -> tuple[list[Card], list[str]]:
    try:
        parsed = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        return [], [f"could not parse YAML: {exc}"]

    if parsed is None:
        return [], ["no entries found in paste"]
    if not isinstance(parsed, list):
        return [], ["pasted YAML must be a list of card entries"]

    added: list[Card] = []
    errors: list[str] = []
    for index, entry in enumerate(parsed, start=1):
        error = _validate_entry(entry, index)
        if error:
            errors.append(error)
            continue
        subtopic_store.ensure_subtopic(entry["category"], entry["subtopic"])
        card = card_store.add_card(
            category=entry["category"],
            subtopic=entry["subtopic"],
            level=entry["level"],
            question=str(entry["question"]),
            answer=str(entry["answer"]),
        )
        added.append(card)
    return added, errors
