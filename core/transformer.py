import numpy as np


# Engagement score weights (must sum to 1.0)
ENGAGEMENT_WEIGHTS = {
    "stars_norm": 0.35,
    "forks_norm": 0.20,
    "watchers_norm": 0.10,
    "issues_norm": 0.10,
    "fork_rate": 0.15,
    "recency_bonus": 0.10,
}


def calculate_engagement_score(
    stars: int,
    forks: int,
    watchers: int,
    open_issues: int,
    repo_age_days: int,
    stars_delta_30d: int = 0,
) -> float:
    """
    Compute a normalized engagement score in the range [0, ~10].
    Uses log1p to handle outliers without discarding data.
    """
    age = max(repo_age_days, 1)

    stars_norm = np.log1p(stars)
    forks_norm = np.log1p(forks)
    watchers_norm = np.log1p(watchers)
    issues_norm = np.log1p(open_issues)

    fork_rate = (forks / age) * 365  # annualized forks
    fork_rate_norm = np.log1p(fork_rate)

    # Recency bonus: repos trending recently score higher
    recency_norm = np.log1p(max(stars_delta_30d, 0))

    score = (
        stars_norm * ENGAGEMENT_WEIGHTS["stars_norm"]
        + forks_norm * ENGAGEMENT_WEIGHTS["forks_norm"]
        + watchers_norm * ENGAGEMENT_WEIGHTS["watchers_norm"]
        + issues_norm * ENGAGEMENT_WEIGHTS["issues_norm"]
        + fork_rate_norm * ENGAGEMENT_WEIGHTS["fork_rate"]
        + recency_norm * ENGAGEMENT_WEIGHTS["recency_bonus"]
    )
    return round(float(score), 4)
