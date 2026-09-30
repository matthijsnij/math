from app.storage import CardStore


def seed_cards(paths, n=3):
    store = CardStore(paths["cards_path"])
    for i in range(n):
        store.add_card(
            category="Mathematics", subtopic="Limits", level=1, question=f"q{i}", answer=f"a{i}"
        )
    return store


def test_get_test_setup_renders_filters_and_count(client):
    response = client.get("/test")

    assert response.status_code == 200
    assert b"count" in response.data.lower()


def test_post_test_session_takes_first_n_of_filtered_pool(client, paths):
    seed_cards(paths, n=5)

    response = client.post("/test/session", data={"category": ["Mathematics"], "count": "3"})

    assert response.status_code == 200
    body = response.data.decode()
    # exactly 3 of the 5 seeded questions should appear embedded in the session data
    assert sum(body.count(f"q{i}") for i in range(5)) == 3


def test_post_test_session_uses_all_and_notices_when_pool_smaller_than_n(client, paths):
    seed_cards(paths, n=2)

    response = client.post("/test/session", data={"category": ["Mathematics"], "count": "10"})

    assert response.status_code == 200
    assert b"only 2" in response.data.lower()
