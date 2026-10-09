
from unittest.mock import patch, Mock

from tracker.mini_league_tracker import get_mini_league


def mock_response(data):
    response = Mock()
    response.json.return_value = data
    response.raise_for_status.return_value = None
    return response


page_1 = {
    "league": {"name": "Test Mini-League"},
    "standings": {
        "results": [
            {"entry": 101, "rank": 1},
            {"entry": 102, "rank": 2},
        ],
        "has_next": True,
    },
}

page_2 = {
    "league": {"name": "Test Mini-League"},
    "standings": {
        "results": [
            {"entry": 103, "rank": 3},
        ],
        "has_next": False,
    },
}


with patch("tracker.mini_league_tracker.requests.get") as mock_get:
    mock_get.side_effect = [
        mock_response(page_1),
        mock_response(page_2),
    ]

    result = get_mini_league(123456)

    managers = result["standings"]["results"]
    manager_ids = [manager["entry"] for manager in managers]

    assert manager_ids == [101, 102, 103]
    assert result["league"]["name"] == "Test Mini-League"
    assert mock_get.call_count == 2

    requested_pages = [
        call.kwargs["params"]["page_standings"]
        for call in mock_get.call_args_list
    ]

    assert requested_pages == [1, 2]

print("=" * 60)
print("MINI-LEAGUE PAGINATION VALIDATION")
print("=" * 60)
print("Page 1: 2 managers")
print("Page 2: 1 manager")
print("Total retrieved: 3 managers")
print("API requests: 2")
print("PAGINATION VALIDATION: PASS")
