from app.storage import CardStore


def seed_cards(paths):
    store = CardStore(paths["cards_path"])
    store.add_card(category="Mathematics", subtopic="Limits", level=1, question="q1", answer="a1")
    store.add_card(category="Mathematics", subtopic="Derivatives", level=2, question="q2", answer="a2")
    store.add_card(category="Brainteasers", subtopic="Game Theory", level=4, question="q3", answer="a3")
    return store


def test_get_remove_lists_all_cards_without_filters(client, paths):
    seed_cards(paths)

    response = client.get("/remove")

    assert response.status_code == 200
    assert response.data.count(b"delete") >= 3


def test_get_remove_filters_by_category(client, paths):
    seed_cards(paths)

    response = client.get("/remove?category=Brainteasers")

    body = response.data.decode()
    assert "q3" in body
    assert "q1" not in body


def test_post_delete_removes_card(client, paths):
    store = seed_cards(paths)
    card_id = store.load()[0].id

    response = client.post(f"/remove/{card_id}/delete", follow_redirects=True)

    assert response.status_code == 200
    remaining_ids = [c.id for c in CardStore(paths["cards_path"]).load()]
    assert card_id not in remaining_ids
