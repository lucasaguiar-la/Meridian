from unittest.mock import MagicMock, patch

import pytest

from collector.market_client import AdzunaClient, AdzunaConfigError


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
