import yaml

from app.subtopics import SubtopicStore


def make_store(tmp_path, initial=None):
    path = tmp_path / "subtopics.yaml"
    path.write_text(yaml.safe_dump(initial or {}))
    return SubtopicStore(path)


def test_load_returns_existing_mapping(tmp_path):
    store = make_store(tmp_path, {"Mathematics": ["Limits", "Derivatives"]})

    assert store.load() == {"Mathematics": ["Limits", "Derivatives"]}


def test_ensure_subtopic_appends_new_and_persists(tmp_path):
    store = make_store(tmp_path, {"Mathematics": ["Limits"]})

    added = store.ensure_subtopic("Mathematics", "Taylor Expansion")

    assert added is True
    assert SubtopicStore(store.path).load()["Mathematics"] == ["Limits", "Taylor Expansion"]


def test_ensure_subtopic_is_noop_for_existing(tmp_path):
    store = make_store(tmp_path, {"Mathematics": ["Limits"]})

    added = store.ensure_subtopic("Mathematics", "Limits")

    assert added is False
    assert store.load()["Mathematics"] == ["Limits"]


def test_ensure_subtopic_creates_category_bucket_if_missing(tmp_path):
    store = make_store(tmp_path, {})

    store.ensure_subtopic("Brainteasers", "Game Theory")

    assert store.load()["Brainteasers"] == ["Game Theory"]
