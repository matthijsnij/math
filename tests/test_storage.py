import yaml

from app.storage import Card, CardStore


def make_store(tmp_path, initial=None):
    path = tmp_path / "cards.yaml"
    path.write_text(yaml.safe_dump(initial or []))
    return CardStore(path)


def test_add_card_assigns_computed_id_and_persists(tmp_path):
    store = make_store(tmp_path)

    card = store.add_card(
        category="Mathematics",
        subtopic="Limits",
        level=1,
        question=r"\lim_{x \to 0} \frac{\sin x}{x}",
        answer="1",
    )

    assert card.id == "mathematics-limits-1-01"
    reloaded = CardStore(store.path).load()
    assert reloaded == [card]


def test_add_card_increments_sequence_within_bucket(tmp_path):
    store = make_store(tmp_path)
    store.add_card(category="Mathematics", subtopic="Limits", level=1, question="q1", answer="a1")

    second = store.add_card(category="Mathematics", subtopic="Limits", level=1, question="q2", answer="a2")

    assert second.id == "mathematics-limits-1-02"


def test_remove_card_deletes_existing_and_reports_success(tmp_path):
    store = make_store(tmp_path)
    card = store.add_card(category="Mathematics", subtopic="Limits", level=1, question="q", answer="a")

    removed = store.remove_card(card.id)

    assert removed is True
    assert store.load() == []


def test_remove_card_returns_false_for_unknown_id(tmp_path):
    store = make_store(tmp_path)

    assert store.remove_card("does-not-exist-1-01") is False


def test_filter_cards_by_category_subtopic_and_level(tmp_path):
    store = make_store(tmp_path)
    a = store.add_card(category="Mathematics", subtopic="Limits", level=1, question="q", answer="a")
    store.add_card(category="Mathematics", subtopic="Derivatives", level=1, question="q", answer="a")
    store.add_card(category="Brainteasers", subtopic="Game Theory", level=4, question="q", answer="a")

    result = store.filter_cards(categories=["Mathematics"], subtopics=["Limits"], levels=[1])

    assert result == [a]


def test_filter_cards_with_no_filters_returns_all(tmp_path):
    store = make_store(tmp_path)
    a = store.add_card(category="Mathematics", subtopic="Limits", level=1, question="q", answer="a")
    b = store.add_card(category="Brainteasers", subtopic="Game Theory", level=4, question="q", answer="a")

    assert store.filter_cards() == [a, b]
