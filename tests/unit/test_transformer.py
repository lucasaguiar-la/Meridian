from core.transformer import ENGAGEMENT_WEIGHTS, calculate_engagement_score


def test_weights_sum_to_one():
    assert round(sum(ENGAGEMENT_WEIGHTS.values()), 6) == 1.0


def test_more_stars_increases_score():
    base = calculate_engagement_score(
        stars=100, forks=10, watchers=5, open_issues=2, repo_age_days=365
    )
    more_stars = calculate_engagement_score(
        stars=1000, forks=10, watchers=5, open_issues=2, repo_age_days=365
    )
    assert more_stars > base


def test_zero_inputs_do_not_raise():
    score = calculate_engagement_score(
        stars=0, forks=0, watchers=0, open_issues=0, repo_age_days=0
    )
    assert score == 0.0


def test_negative_stars_delta_does_not_raise():
    score = calculate_engagement_score(
        stars=100,
        forks=10,
        watchers=5,
        open_issues=2,
        repo_age_days=365,
        stars_delta_30d=-50,
    )
    assert isinstance(score, float)
