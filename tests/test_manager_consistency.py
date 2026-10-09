
import statistics
from unittest.mock import patch

from tracker.manager_consistency import calculate_manager_consistency


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
        {"event": 3, "points": 40, "event_transfers_cost": 0},
    ],
    102: [
        {"event": 1, "points": 55, "event_transfers_cost": 0},
        {"event": 2, "points": 55, "event_transfers_cost": 0},
        {"event": 3, "points": 55, "event_transfers_cost": 0},
    ],
    103: []
}


with patch(
    "tracker.manager_consistency.get_mini_league",
    return_value=mock_league
), patch(
    "tracker.manager_consistency.get_manager_history",
    side_effect=lambda manager_id: mock_histories[manager_id]
):
    league_name, results = calculate_manager_consistency(123456)


assert league_name == "Test League"

# Managers with no completed gameweeks are excluded.
assert len(results) == 2

# Team B has identical scores every GW.
assert results[0]["team_name"] == "Team B"
assert results[0]["standard_deviation"] == 0

# Team A's net scores are 50, 66 and 40.
team_a = next(
    manager for manager in results
    if manager["manager_id"] == 101
)

assert team_a["gameweeks"] == 3
assert team_a["average_points"] == 52
assert team_a["best_gw"] == 66
assert team_a["worst_gw"] == 40

expected_std = statistics.pstdev([50, 66, 40])

assert abs(
    team_a["standard_deviation"] - expected_std
) < 0.000001

print("=" * 60)
print("MANAGER CONSISTENCY VALIDATION")
print("=" * 60)
print("Transfer deductions: PASS")
print("Average points: PASS")
print("Best and worst gameweeks: PASS")
print("Population standard deviation: PASS")
print("Consistency sorting: PASS")
print("Empty history handling: PASS")
print("MANAGER CONSISTENCY VALIDATION: PASS")
