
from unittest.mock import patch

from tracker.season_summary import generate_season_summary


mock_leaderboard = [
    {
        "manager_id": 101,
        "team_name": "Team A",
        "total_points": 150,
        "average_points": 75.0
    }
]

mock_winners = {
    1: [
        {"team_name": "Team A", "points": 80}
    ]
}

mock_movements = {
    2: [
        {
            "manager_id": 101,
            "team_name": "Team A",
            "rank": 1,
            "change": 1
        }
    ]
}

mock_consistency = [
    {
        "manager_id": 101,
        "team_name": "Team A",
        "average_points": 75.0,
        "best_gw": 80,
        "worst_gw": 70,
        "standard_deviation": 5.0
    }
]


with (
    patch(
        "tracker.season_summary.build_leaderboard",
        return_value=("Test League", mock_leaderboard)
    ),
    patch(
        "tracker.season_summary.find_gameweek_winners",
        return_value=("Test League", mock_winners)
    ),
    patch(
        "tracker.season_summary.calculate_rank_movements",
        return_value=("Test League", mock_movements)
    ),
    patch(
        "tracker.season_summary.calculate_manager_consistency",
        return_value=("Test League", mock_consistency)
    )
):
    summary = generate_season_summary(123456)


assert summary["league_id"] == 123456
assert summary["league_name"] == "Test League"

assert summary["leaderboard"] == mock_leaderboard
assert summary["gameweek_winners"] == mock_winners
assert summary["rank_movements"] == mock_movements
assert summary["consistency"] == mock_consistency

assert summary["leaderboard"][0]["total_points"] == 150
assert summary["gameweek_winners"][1][0]["points"] == 80
assert summary["rank_movements"][2][0]["change"] == 1
assert summary["consistency"][0]["standard_deviation"] == 5.0

print("=" * 60)
print("UNIFIED SEASON SUMMARY VALIDATION")
print("=" * 60)
print("League information: PASS")
print("Leaderboard integration: PASS")
print("Gameweek winners integration: PASS")
print("Rank movements integration: PASS")
print("Consistency integration: PASS")
print("UNIFIED SEASON SUMMARY VALIDATION: PASS")
