
from unittest.mock import patch

from tracker.historical_rankings import calculate_historical_rankings


mock_league = {
    "league": {"name": "Test League"},
    "standings": {
        "results": [
            {"entry": 101, "entry_name": "Team A"},
            {"entry": 102, "entry_name": "Team B"},
            {"entry": 103, "entry_name": "Team C"},
        ]
    }
}

mock_histories = {
    101: [
        {"event": 1, "points": 50, "event_transfers_cost": 0},
        {"event": 2, "points": 70, "event_transfers_cost": 4},
    ],
    102: [
        {"event": 1, "points": 60, "event_transfers_cost": 0},
        {"event": 2, "points": 56, "event_transfers_cost": 0},
    ],
    103: [
        {"event": 1, "points": 40, "event_transfers_cost": 0},
        {"event": 2, "points": 65, "event_transfers_cost": 0},
    ],
}

with patch(
    "tracker.historical_rankings.get_mini_league",
    return_value=mock_league
), patch(
    "tracker.historical_rankings.get_manager_history",
    side_effect=lambda manager_id: mock_histories[manager_id]
):
    league_name, rankings = calculate_historical_rankings(123456)


assert league_name == "Test League"
assert sorted(rankings.keys()) == [1, 2]

# GW1: Team B (60), Team A (50), Team C (40).
assert [m["team_name"] for m in rankings[1]] == [
    "Team B", "Team A", "Team C"
]

# GW2: Team A and Team B both finish on 116.
assert rankings[2][0]["cumulative_points"] == 116
assert rankings[2][1]["cumulative_points"] == 116
assert rankings[2][2]["cumulative_points"] == 105

# Current implementation assigns sequential ranks to ties.
assert [m["rank"] for m in rankings[2]] == [1, 2, 3]

print("=" * 60)
print("HISTORICAL RANKINGS VALIDATION")
print("=" * 60)
print("Gameweek ordering: PASS")
print("Cumulative scoring: PASS")
print("Ranking order: PASS")
print("Equal-points handling: PASS (sequential provisional ranks)")
print("HISTORICAL RANKINGS VALIDATION: PASS")
