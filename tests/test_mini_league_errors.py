
from unittest.mock import patch, Mock
import requests

from tracker.mini_league_tracker import get_mini_league


print("=" * 60)
print("MINI-LEAGUE ERROR HANDLING VALIDATION")
print("=" * 60)


# TEST 1: Invalid league ID (HTTP 404)
mock_response = Mock()
mock_response.raise_for_status.side_effect = (
    requests.exceptions.HTTPError("404 Not Found")
)

with patch(
    "tracker.mini_league_tracker.requests.get",
    return_value=mock_response
):
    try:
        get_mini_league(999999999)
        raise AssertionError("Expected HTTPError")
    except requests.exceptions.HTTPError:
        print("Invalid league ID handling: PASS")


# TEST 2: API connection failure
with patch(
    "tracker.mini_league_tracker.requests.get",
    side_effect=requests.exceptions.ConnectionError(
        "Unable to connect to FPL API"
    )
):
    try:
        get_mini_league(1701837)
        raise AssertionError("Expected ConnectionError")
    except requests.exceptions.ConnectionError:
        print("API connection failure handling: PASS")


# TEST 3: API timeout
with patch(
    "tracker.mini_league_tracker.requests.get",
    side_effect=requests.exceptions.Timeout(
        "Request timed out"
    )
):
    try:
        get_mini_league(1701837)
        raise AssertionError("Expected Timeout")
    except requests.exceptions.Timeout:
        print("API timeout handling: PASS")


print("=" * 60)
print("MINI-LEAGUE ERROR HANDLING VALIDATION: PASS")