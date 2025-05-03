# tests/test_leak_checker.py
import pytest
from unittest.mock import patch, Mock
from src.api_client import HaveIBeenPwnedClient
from requests.exceptions import RequestException

@pytest.fixture
def client():
    """Fixture to initialize HaveIBeenPwnedClient with a dummy API key."""
    return HaveIBeenPwnedClient(api_key="dummy_key")

def test_check_breaches_breached_email(client):
    """Test check_breaches returns breaches for a breached email (HTTP 200)."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"Name": "Adobe", "Title": "Adobe Breach", "BreachDate": "2013-10-04"},
        {"Name": "LinkedIn", "Title": "LinkedIn Breach", "BreachDate": "2012-05-05"}
    ]
    with patch("requests.get", return_value=mock_response):
        result = client.check_breaches("test@example.com")
        assert isinstance(result, list), "Result should be a list"
        assert len(result) == 2, "Expected two breaches"
        assert result[0]["Name"] == "Adobe", "Expected Adobe breach"
        assert result[1]["Name"] == "LinkedIn", "Expected LinkedIn breach"

def test_check_breaches_no_breaches(client):
    """Test check_breaches returns empty list for non-breached email (HTTP 404)."""
    mock_response = Mock()
    mock_response.status_code = 404
    with patch("requests.get", return_value=mock_response):
        result = client.check_breaches("safe@example.com")
        assert isinstance(result, list), "Result should be a list"
        assert len(result) == 0, "Expected empty list for non-breached email"

def test_check_breaches_rate_limit(client):
    """Test check_breaches retries on rate limit (HTTP 429) and returns breaches."""
    mock_response_429 = Mock()
    mock_response_429.status_code = 429
    mock_response_200 = Mock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = [
        {"Name": "Adobe", "Title": "Adobe Breach", "BreachDate": "2013-10-04"}
    ]
    # Simulate 429 on first call, 200 on retry
    with patch("requests.get", side_effect=[mock_response_429, mock_response_200]) as mock_get:
        with patch("time.sleep") as mock_sleep:
            result = client.check_breaches("test@example.com")
            mock_sleep.assert_called_once_with(10)
            assert mock_get.call_count == 2, "Expected two API calls (retry after 429)"
            assert isinstance(result, list), "Result should be a list"
            assert len(result) == 1, "Expected one breach"
            assert result[0]["Name"] == "Adobe", "Expected Adobe breach"

def test_check_breaches_request_exception(client, capsys):
    """Test check_breaches handles request exceptions and returns empty list."""
    with patch("requests.get", side_effect=RequestException("Network error")):
        result = client.check_breaches("test@example.com")