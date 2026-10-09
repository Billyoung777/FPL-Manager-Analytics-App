
from unittest.mock import patch

from tracker.rank_movements import calculate_rank_movements


mock_rankings = {
    1: [
        {"manager_id": 101, "team_name": "Team A", "rank": 1},
        {"manager_id": 102, "team_name": "Team B", "rank": 2},
        {"manager_id": 103, "team_name": "Team C", "rank": 3},
    ],
    2: [
        {"manager_id": 103, "team_name": "Team C", "rank": 1},
        {"manager_id": 101, "team_name": "Team A", "rank": 2},
        {"manager_id": 102, "team_name": "Team B", "rank": 3},
    ],
    3: [
        {"manager_id": 103, "team_name": "Team C", "rank": 1},
        {"manager_id": 102, "team_name": "Team B", "rank": 2},
        {"manager_id": 101, "team_name": "Team A", "rank": 3},
    ],
}


with patch(
    "tracker.rank_movements.calculate_historical_rankings",
    return_value=("Test League", mock_rankings)
):
    league_name, movements = calculate_rank_movements(123456)


assert league_name == "Test League"
assert sorted(movements.keys()) == [1, 2, 3]

# GW1: All managers appear for the first time.
assert all(
    manager["change"] is None
    for manager in movements[1]
)

# GW2: Team C climbs from 3rd to 1st.
team_c_gw2 = next(
    manager for manager in movements[2]
    if manager["manager_id"] == 103
)
assert team_c_gw2["change"] == 2

# GW3: Team C remains in 1st place.
team_c_gw3 = next(
    manager for manager in movements[3]
    if manager["manager_id"] == 103
)
assert team_c_gw3["change"] == 0

# GW3: Team A drops from 2nd to 3rd.
team_a_gw3 = next(
    manager for manager in movements[3]
    if manager["manager_id"] == 101
)
assert team_a_gw3["change"] == -1

print("=" * 60)
print("RANK MOVEMENTS VALIDATION")
print("=" * 60)
print("First gameweek handling: PASS")
print("Upward movement: PASS")
print("Unchanged position: PASS")
print("Downward movement: PASS")
print("RANK MOVEMENTS VALIDATION: PASS")
