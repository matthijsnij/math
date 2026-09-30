"""Flask routes: add / remove / practice / test (see docs/agents/domain.md, CONTEXT.md)."""

from __future__ import annotations

import random
from dataclasses import asdict

import yaml
from flask import Blueprint, current_app, redirect, render_template, request, url_for

from app.categories import CATEGORIES, LEVELS
from app.storage import CardStore
from app.subtopics import SubtopicStore
from app.validation import process_paste

main_bp = Blueprint("main", __name__)


def _card_store() -> CardStore:
    return CardStore(current_app.config["CARDS_PATH"])


def _subtopic_store() -> SubtopicStore:
    return SubtopicStore(current_app.config["SUBTOPICS_PATH"])


def _macros() -> dict:
    path = current_app.config["MACROS_PATH"]
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _all_subtopics() -> list[str]:
    subtopics = _subtopic_store().load()
    return sorted({name for names in subtopics.values() for name in names})


def _filtered_cards(source) -> list:
    """Apply the category/subtopic/level multi-select filters from a request's args or form."""
    categories = source.getlist("category")
    subtopics = source.getlist("subtopic")
    levels = [int(value) for value in source.getlist("level") if value.isdigit()]
    return _card_store().filter_cards(
        categories=categories or None, subtopics=subtopics or None, levels=levels or None
    )


@main_bp.route("/")
def index():
    return render_template("index.html", card_count=len(_card_store().load()))


@main_bp.route("/add", methods=["GET", "POST"])
def add_cards():
    added: list | None = None
    errors: list[str] = []
    if request.method == "POST":
        if "cards_yaml" in request.form:
            cards_yaml = request.form.get("cards_yaml", "")
        else:
            level = request.form.get("level", "")
            entry = {
                "category": request.form.get("category", ""),
                "subtopic": request.form.get("subtopic", ""),
                "level": int(level) if level.isdigit() else level,
                "question": request.form.get("question", ""),
                "answer": request.form.get("answer", ""),
            }
            cards_yaml = yaml.safe_dump([entry], sort_keys=False, allow_unicode=True)
        added, errors = process_paste(cards_yaml, _card_store(), _subtopic_store())
    return render_template(
        "add.html",
        categories=CATEGORIES,
        levels=LEVELS,
        subtopics=_all_subtopics(),
        added=added,
        errors=errors,
    )


@main_bp.route("/remove")
def remove_cards():
    cards = _filtered_cards(request.args)
    return render_template(
        "remove.html",
        cards=cards,
        categories=CATEGORIES,
        levels=LEVELS,
        subtopics=_all_subtopics(),
        selected_categories=request.args.getlist("category"),
        selected_subtopics=request.args.getlist("subtopic"),
        selected_levels=[int(value) for value in request.args.getlist("level") if value.isdigit()],
        macros=_macros(),
    )


@main_bp.route("/remove/<card_id>/delete", methods=["POST"])
def delete_card(card_id: str):
    _card_store().remove_card(card_id)
    return redirect(
        url_for(
            "main.remove_cards",
            category=request.args.getlist("category"),
            subtopic=request.args.getlist("subtopic"),
            level=request.args.getlist("level"),
        )
    )


@main_bp.route("/practice")
def practice_setup():
    return render_template(
        "practice_setup.html", categories=CATEGORIES, levels=LEVELS, subtopics=_all_subtopics()
    )


@main_bp.route("/practice/session", methods=["POST"])
def practice_session():
    cards = _filtered_cards(request.form)
    return render_template(
        "practice_session.html", cards_json=[asdict(c) for c in cards], macros=_macros()
    )


@main_bp.route("/test")
def test_setup():
    return render_template(
        "test_setup.html", categories=CATEGORIES, levels=LEVELS, subtopics=_all_subtopics()
    )


@main_bp.route("/test/session", methods=["POST"])
def test_session():
    count = int(request.form.get("count") or 0)
    pool = _filtered_cards(request.form)
    random.shuffle(pool)
    notice = None
    if count > 0 and len(pool) < count:
        notice = f"Only {len(pool)} card(s) matched the filters; running the test on all of them."
    selected = pool[:count] if count > 0 else pool
    return render_template(
        "test_session.html", cards_json=[asdict(c) for c in selected], notice=notice, macros=_macros()
    )
