from app.storage import CardStore


def seed_cards(paths):
    store = CardStore(paths["cards_path"])
    store.add_card(category="Mathematics", subtopic="Limits", level=1, question="q1", answer="a1")
    store.add_card(category="Mathematics", subtopic="Derivatives", level=2, question="q2", answer="a2")
    return store


def test_get_practice_setup_renders_filters(client):
    response = client.get("/practice")

    assert response.status_code == 200
    assert b"category" in response.data.lower()


def test_post_practice_session_embeds_filtered_cards(client, paths):
    seed_cards(paths)

    response = client.post("/practice/session", data={"category": ["Mathematics"], "subtopic": ["Limits"], "level": ["1"]})

    assert response.status_code == 200
    body = response.data.decode()
    assert "q1" in body
    assert "q2" not in body


def test_post_practice_session_with_no_matches_shows_message(client, paths):
    seed_cards(paths)

    response = client.post("/practice/session", data={"category": ["Brainteasers"]})

    assert response.status_code == 200
    assert b"No cards match" in response.data
