"""Math Flashcards Flask app package."""

from __future__ import annotations

from pathlib import Path

from flask import Flask

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def create_app(cards_path=None, subtopics_path=None, macros_path=None) -> Flask:
    app = Flask(__name__)
    app.config["CARDS_PATH"] = Path(cards_path) if cards_path else DATA_DIR / "cards.yaml"
    app.config["SUBTOPICS_PATH"] = (
        Path(subtopics_path) if subtopics_path else DATA_DIR / "subtopics.yaml"
    )
    app.config["MACROS_PATH"] = Path(macros_path) if macros_path else DATA_DIR / "katex_macros.yaml"

    from app.routes import main_bp

    app.register_blueprint(main_bp)
    return app
