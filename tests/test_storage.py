import yaml

from cardlib.storage import Card, CardStore


def test_load_reads_cards_from_yaml(tmp_path):
    path = tmp_path / "cards.yaml"
    entry = dict(id="mathematics-limits-1-01", category="Mathematics", subtopic="Limits",
                 level=1, question="q", answer="a")
    path.write_text(yaml.safe_dump([entry]))

    assert CardStore(path).load() == [Card(**entry)]


def test_load_returns_empty_for_missing_file(tmp_path):
    assert CardStore(tmp_path / "nope.yaml").load() == []
