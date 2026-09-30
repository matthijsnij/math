from app.slugs import next_card_id, slugify


def test_slugify_lowercases_and_dashes_non_alnum():
    assert slugify("Probability & Statistics") == "probability-statistics"
    assert slugify("Mean, Median, Mode and Range") == "mean-median-mode-and-range"


def test_next_card_id_starts_at_01_when_bucket_empty():
    assert next_card_id([], "Mathematics", "Limits", 1) == "mathematics-limits-1-01"


def test_next_card_id_increments_within_same_bucket():
    existing = ["mathematics-limits-1-01", "mathematics-limits-1-02"]
    assert next_card_id(existing, "Mathematics", "Limits", 1) == "mathematics-limits-1-03"


def test_next_card_id_is_independent_per_bucket():
    existing = ["mathematics-limits-1-01", "mathematics-limits-2-01"]
    assert next_card_id(existing, "Mathematics", "Limits", 1) == "mathematics-limits-1-02"
    assert next_card_id(existing, "Mathematics", "Derivatives", 1) == "mathematics-derivatives-1-01"
