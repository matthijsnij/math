import yaml

from cardlib.subtopics import SubtopicStore


def test_load_returns_existing_mapping(tmp_path):
    path = tmp_path / "subtopics.yaml"
    path.write_text(yaml.safe_dump({"Mathematics": ["Limits", "Derivatives"]}))

    assert SubtopicStore(path).load() == {"Mathematics": ["Limits", "Derivatives"]}


def test_load_returns_empty_for_missing_file(tmp_path):
    assert SubtopicStore(tmp_path / "nope.yaml").load() == {}
