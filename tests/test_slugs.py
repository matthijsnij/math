from cardlib.slugs import slugify


def test_slugify_lowercases_and_dashes_non_alnum():
    assert slugify("Probability & Statistics") == "probability-statistics"
    assert slugify("Mean, Median, Mode and Range") == "mean-median-mode-and-range"
