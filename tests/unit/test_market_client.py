from unittest.mock import MagicMock, patch

import pytest

from collector.market_client import AdzunaClient, AdzunaConfigError, RemoteOKClient


def test_missing_credentials_raise_config_error():
    client = AdzunaClient(app_id="", app_key="", country="br")
    with pytest.raises(AdzunaConfigError):
        client.count_job_postings("python")


def test_count_job_postings_returns_total_count():
    client = AdzunaClient(app_id="id", app_key="key", country="br")

    mock_response = MagicMock()
    mock_response.json.return_value = {"count": 1234, "results": []}
    mock_response.raise_for_status.return_value = None

    with patch.object(client._session, "get", return_value=mock_response) as mock_get:
        count = client.count_job_postings("python")

    assert count == 1234
    called_params = mock_get.call_args.kwargs["params"]
    assert called_params["what"] == "python"
    assert called_params["app_id"] == "id"
    assert called_params["app_key"] == "key"


def test_count_job_postings_defaults_to_zero_when_count_missing():
    client = AdzunaClient(app_id="id", app_key="key", country="br")

    mock_response = MagicMock()
    mock_response.json.return_value = {"results": []}
    mock_response.raise_for_status.return_value = None

    with patch.object(client._session, "get", return_value=mock_response):
        count = client.count_job_postings("rust")

    assert count == 0


def test_go_keyword_is_mapped_to_golang():
    """"go" is too ambiguous for a free-text search (matches "go-getter", etc.);
    confirmed empirically that "golang" is the term real postings actually use."""
    client = AdzunaClient(app_id="id", app_key="key", country="br")

    mock_response = MagicMock()
    mock_response.json.return_value = {"count": 42}
    mock_response.raise_for_status.return_value = None

    with patch.object(client._session, "get", return_value=mock_response) as mock_get:
        client.count_job_postings("go")

    assert mock_get.call_args.kwargs["params"]["what"] == "golang"


def test_other_keywords_are_not_remapped():
    client = AdzunaClient(app_id="id", app_key="key", country="br")

    mock_response = MagicMock()
    mock_response.json.return_value = {"count": 1}
    mock_response.raise_for_status.return_value = None

    with patch.object(client._session, "get", return_value=mock_response) as mock_get:
        client.count_job_postings("python")

    assert mock_get.call_args.kwargs["params"]["what"] == "python"


def test_remoteok_fetch_listings_filters_out_legal_notice():
    client = RemoteOKClient()

    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"legal": "https://remoteok.com/legal"},
        {"position": "Backend Engineer", "tags": ["python", "django"]},
        {"position": "Frontend Engineer", "tags": ["javascript", "react"]},
    ]
    mock_response.raise_for_status.return_value = None

    with patch.object(client._session, "get", return_value=mock_response):
        listings = client.fetch_listings()

    assert len(listings) == 2
    assert all("tags" in job for job in listings)


def test_remoteok_count_by_tag_matches_case_insensitively():
    listings = [
        {"tags": ["Python", "Django"]},
        {"tags": ["javascript"]},
        {"tags": ["golang"]},
    ]

    assert RemoteOKClient.count_by_tag(listings, "python") == 1
    assert RemoteOKClient.count_by_tag(listings, "PYTHON") == 1
    assert RemoteOKClient.count_by_tag(listings, "javascript") == 1
    assert RemoteOKClient.count_by_tag(listings, "rust") == 0


def test_remoteok_count_by_tag_maps_go_to_golang():
    listings = [{"tags": ["golang"]}, {"tags": ["python"]}]

    assert RemoteOKClient.count_by_tag(listings, "go") == 1
