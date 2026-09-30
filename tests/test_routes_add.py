import yaml

from app.storage import CardStore


def test_get_add_page_renders_form(client):
    response = client.get("/add")

    assert response.status_code == 200
    assert b"cards_yaml" in response.data


def test_post_paste_with_valid_entry_adds_card(client, paths):
    response = client.post(
        "/add",
        data={
            "cards_yaml": (
                "- category: Mathematics\n"
                "  subtopic: Limits\n"
                "  level: 1\n"
                "  question: \"x\"\n"
                "  answer: \"y\"\n"
            )
        },
    )

    assert response.status_code == 200
    assert b"Added 1 card" in response.data
    cards = CardStore(paths["cards_path"]).load()
    assert len(cards) == 1
    assert cards[0].id == "mathematics-limits-1-01"


def test_post_paste_with_invalid_entry_reports_error_without_adding(client, paths):
    response = client.post(
        "/add",
        data={
            "cards_yaml": (
                "- category: NotACategory\n"
                "  subtopic: Limits\n"
                "  level: 1\n"
                "  question: \"x\"\n"
                "  answer: \"y\"\n"
            )
        },
    )

    assert response.status_code == 200
    assert b"invalid category" in response.data
    assert CardStore(paths["cards_path"]).load() == []


def test_post_single_card_form_adds_one_entry(client, paths):
    response = client.post(
        "/add",
        data={
            "category": "Mathematics",
            "subtopic": "Limits",
            "level": "1",
            "question": "x",
            "answer": "y",
        },
    )

    assert response.status_code == 200
    assert b"Added 1 card" in response.data
    cards = CardStore(paths["cards_path"]).load()
    assert len(cards) == 1
