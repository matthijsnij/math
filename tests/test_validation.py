import yaml

from app.storage import CardStore
from app.subtopics import SubtopicStore
from app.validation import process_paste


def make_stores(tmp_path, subtopics=None):
    cards_path = tmp_path / "cards.yaml"
    cards_path.write_text(yaml.safe_dump([]))
    subtopics_path = tmp_path / "subtopics.yaml"
    subtopics_path.write_text(yaml.safe_dump(subtopics or {"Mathematics": ["Limits"]}))
    return CardStore(cards_path), SubtopicStore(subtopics_path)


def test_valid_single_entry_is_added(tmp_path):
    card_store, subtopic_store = make_stores(tmp_path)
    text = """
- category: Mathematics
  subtopic: Limits
  level: 1
  question: "x"
  answer: "y"
"""

    added, errors = process_paste(text, card_store, subtopic_store)

    assert errors == []
    assert len(added) == 1
    assert added[0].id == "mathematics-limits-1-01"
    assert card_store.load() == added


def test_invalid_category_reports_entry_error_and_skips_it(tmp_path):
    card_store, subtopic_store = make_stores(tmp_path)
    text = """
- category: Stats
  subtopic: Limits
  level: 1
  question: "x"
  answer: "y"
"""

    added, errors = process_paste(text, card_store, subtopic_store)

    assert added == []
    assert errors == ["entry 1: invalid category 'Stats'"]


def test_invalid_level_reports_entry_error(tmp_path):
    card_store, subtopic_store = make_stores(tmp_path)
    text = """
- category: Mathematics
  subtopic: Limits
  level: 5
  question: "x"
  answer: "y"
"""

    added, errors = process_paste(text, card_store, subtopic_store)

    assert added == []
    assert errors == ["entry 1: invalid level '5' (must be 1-4)"]


def test_new_subtopic_is_accepted_and_appended(tmp_path):
    card_store, subtopic_store = make_stores(tmp_path)
    text = """
- category: Mathematics
  subtopic: Taylor Expansion
  level: 2
  question: "x"
  answer: "y"
"""

    added, errors = process_paste(text, card_store, subtopic_store)

    assert errors == []
    assert added[0].subtopic == "Taylor Expansion"
    assert "Taylor Expansion" in subtopic_store.load()["Mathematics"]


def test_valid_entries_kept_when_other_entries_in_same_paste_are_invalid(tmp_path):
    card_store, subtopic_store = make_stores(tmp_path)
    text = """
- category: Mathematics
  subtopic: Limits
  level: 1
  question: "x1"
  answer: "y1"
- category: Stats
  subtopic: Limits
  level: 1
  question: "x2"
  answer: "y2"
- category: Mathematics
  subtopic: Limits
  level: 1
  question: "x3"
  answer: "y3"
"""

    added, errors = process_paste(text, card_store, subtopic_store)

    assert len(added) == 2
    assert errors == ["entry 2: invalid category 'Stats'"]
    assert [c.question for c in added] == ["x1", "x3"]


def test_non_list_yaml_reports_single_error(tmp_path):
    card_store, subtopic_store = make_stores(tmp_path)

    added, errors = process_paste("just: a mapping", card_store, subtopic_store)

    assert added == []
    assert errors == ["pasted YAML must be a list of card entries"]
