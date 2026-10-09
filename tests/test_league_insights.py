
from unittest.mock import patch

from tracker.league_insights import calculate_league_insights


mock_movements = {
    1: [
        {"manager_id": 101, "team_name": "Team A", "change": None},
        {"manager_id": 102, "team_name": "Team B", "change": None},
        {"manager_id": 103, "team_name": "Team C", "change": None},
        {"manager_id": 104, "team_name": "Team D", "change": None},
    ],
    2: [
        {"manager_id": 101, "team_name": "Team A", "change": 2},
        {"manager_id": 102, "team_name": "Team B", "change": 2},
        {"manager_id": 103, "team_name": "Team C", "change": -3},
        {"manager_id": 104, "team_name": "Team D", "change": -1},
    ],
    3: [
        {"manager_id": 101, "team_name": "Team A", "change": 0},
        {"manager_id": 102, "team_name": "Team B", "change": 0},
        {"manager_id": 103, "team_name": "Team C", "change": 0},
        {"manager_id": 104, "team_name": "Team D", "change": 0},
    ],
}


with patch(
    "tracker.league_insights.calculate_rank_movements",
    return_value=("Test League", mock_movements)
):
    league_name, insights = calculate_league_insights(123456)


assert league_name == "Test League"

# GW1: No previous rankings.
assert insights[1]["biggest_climbers"] == []
assert insights[1]["biggest_fallers"] == []

# GW2: Both Team A and Team B climbed by 2.
assert {
    manager["team_name"]
    for manager in insights[2]["biggest_climbers"]
} == {"Team A", "Team B"}

# GW2: Team C dropped the most.
assert [
    manager["team_name"]
    for manager in insights[2]["biggest_fallers"]
] == ["Team C"]

# GW3: All positions unchanged.
assert insights[3]["biggest_climbers"] == []
assert insights[3]["biggest_fallers"] == []

print("=" * 60)
print("MINI-LEAGUE INSIGHTS VALIDATION")
print("=" * 60)
print("First gameweek handling: PASS")
print("Biggest climber detection: PASS")
print("Biggest faller detection: PASS")
print("Tied climbers: PASS")
print("Unchanged positions: PASS")
print("MINI-LEAGUE INSIGHTS VALIDATION: PASS")
