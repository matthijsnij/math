import yaml
import pytest

from app import create_app


@pytest.fixture
def paths(tmp_path):
    cards_path = tmp_path / "cards.yaml"
    cards_path.write_text(yaml.safe_dump([]))
    subtopics_path = tmp_path / "subtopics.yaml"
    subtopics_path.write_text(yaml.safe_dump({"Mathematics": ["Limits", "Derivatives"]}))
    macros_path = tmp_path / "katex_macros.yaml"
    macros_path.write_text(yaml.safe_dump({}))
    return {"cards_path": cards_path, "subtopics_path": subtopics_path, "macros_path": macros_path}


@pytest.fixture
def app(paths):
    application = create_app(**paths)
    application.config.update(TESTING=True)
    return application


@pytest.fixture
def client(app):
    return app.test_client()
